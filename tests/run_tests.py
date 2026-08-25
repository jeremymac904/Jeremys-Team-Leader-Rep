#!/usr/bin/env python3
"""Test suite for the Team Leader OS.

    python3 tests/run_tests.py            everything that needs no model
    python3 tests/run_tests.py --local-ai adds tests that need a running model

Tests marked [needs model] are skipped unless --local-ai is passed and the local
server is running, so the default run stays fast and works on a fresh clone.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
sys.path.insert(0, str(ROOT / "scripts" / "local_ai"))

PASSED, FAILED, SKIPPED = [], [], []


def check(name: str, condition: bool, detail: str = "") -> None:
    (PASSED if condition else FAILED).append((name, detail))


def skip(name: str, why: str) -> None:
    SKIPPED.append((name, why))


# ---------------------------------------------------------------- yaml reader
def test_miniyaml():
    from miniyaml import loads_subset, MiniYamlError

    data = loads_subset("a: 1\nb: two\nc: [x, y]\nd:\n  e: true\n  f: null\n")
    check("miniyaml scalars", data == {"a": 1, "b": "two", "c": ["x", "y"],
                                       "d": {"e": True, "f": None}}, str(data))

    data = loads_subset("items:\n  - id: one\n    v: 1\n  - id: two\n    v: 2\n")
    check("miniyaml list of maps",
          data == {"items": [{"id": "one", "v": 1}, {"id": "two", "v": 2}]}, str(data))

    data = loads_subset("lit: |\n  a\n  b # not a comment\nfold: >-\n  x\n  y\n")
    check("miniyaml literal block", data["lit"] == "a\nb # not a comment", repr(data["lit"]))
    check("miniyaml folded block", data["fold"] == "x y", repr(data["fold"]))

    try:
        loads_subset("a: &anchor\n")
        check("miniyaml rejects anchors", False, "should have raised")
    except MiniYamlError:
        check("miniyaml rejects anchors", True)


# ------------------------------------------------------------------ manifest
def test_manifest():
    from miniyaml import load_file

    manifest = load_file(ROOT / "local-ai" / "models.manifest.yaml")
    ids = {m["id"] for m in manifest["models"]}
    check("manifest has 4 tiers", len(manifest["tiers"]) == 4, str(len(manifest["tiers"])))
    check("manifest models present", len(manifest["models"]) >= 5)

    for tier in manifest["tiers"]:
        check(f"tier {tier['id']} reasoning model exists",
              tier["reasoning_model"] in ids, tier["reasoning_model"])
        check(f"tier {tier['id']} extraction model exists",
              tier["extraction_model"] in ids, tier["extraction_model"])

    required = ["display_name", "family", "hf_repo", "gguf_file", "role", "quantization",
                "download_size_gb", "ram_required_gb", "license", "status", "date_reviewed",
                "context_guidance", "vision", "llama_cpp_compatible", "limitations"]
    for model in manifest["models"]:
        missing = [f for f in required if model.get(f) in (None, "")]
        check(f"manifest {model['id']} complete", not missing, str(missing))
        check(f"manifest {model['id']} license permits commercial use",
              model["license"] in ("apache-2.0", "mit"), model["license"])


# ---------------------------------------------------------------------- tiers
def test_tier_selection():
    from miniyaml import load_file
    from hardware import select_tier

    tiers = load_file(ROOT / "local-ai" / "models.manifest.yaml")["tiers"]
    cases = [(4, None), (8, "tier-8gb"), (12, "tier-8gb"), (16, "tier-16gb"),
             (18, "tier-16gb"), (24, "tier-24gb"), (28, "tier-24gb"),
             (32, "tier-32gb"), (64, "tier-32gb")]
    for ram, expected in cases:
        tier, _ = select_tier(float(ram), tiers)
        got = tier["id"] if tier else None
        check(f"{ram} GB -> {expected}", got == expected, f"got {got}")


# -------------------------------------------------------------------- privacy
def test_privacy():
    import privacy as pv

    borrower = ["paystub", "bank statement", "tax return", "w2", "purchase contract",
                "closing disclosure", "credit report", "borrower letter"]
    for item in borrower:
        category, _ = pv.classify(item)
        check(f"'{item}' is LOCAL_REQUIRED", category == pv.LOCAL_REQUIRED, category)

    for item in ["coaching note", "candidate screening"]:
        category, _ = pv.classify(item)
        check(f"'{item}' is LOCAL_PREFERRED", category == pv.LOCAL_PREFERRED, category)

    for item in ["guideline research", "marketing content"]:
        category, _ = pv.classify(item)
        check(f"'{item}' is CLOUD_ACCEPTABLE", category == pv.CLOUD_ACCEPTABLE, category)

    category, _ = pv.classify("zzz unknown thing")
    check("unknown workflow fails closed", category == pv.LOCAL_REQUIRED, category)

    for url in ["http://127.0.0.1:8080/v1", "http://localhost:8080", "http://[::1]:8080"]:
        check(f"loopback: {url}", pv.is_loopback(url))
    for url in ["https://api.openai.com/v1", "https://api.anthropic.com",
                "http://192.168.1.5:8080"]:
        check(f"not loopback: {url}", not pv.is_loopback(url))

    try:
        pv.assert_local_allowed("paystub", "https://api.openai.com/v1")
        check("cloud blocked for borrower doc", False, "was not blocked")
    except pv.PrivacyViolation:
        check("cloud blocked for borrower doc", True)

    try:
        pv.assert_local_allowed("paystub", "http://127.0.0.1:8080/v1")
        check("local allowed for borrower doc", True)
    except pv.PrivacyViolation as exc:
        check("local allowed for borrower doc", False, str(exc))


# --------------------------------------------------------------------- skills
def test_skills():
    from miniyaml import loads_subset

    required = ["## Purpose", "## Workflow", "## Expected output"]
    doc_required = ["## When Hermes should use it", "## Required information",
                    "## Safety boundaries", "## Human approval requirements",
                    "## Related skills", "## What this skill must not assume"]

    skills = sorted(ROOT.joinpath("skills").rglob("SKILL.md"))
    check("skills found", len(skills) >= 20, f"{len(skills)} found")

    for path in skills:
        name = path.parent.name
        body = path.read_text(encoding="utf-8")
        check(f"{name}: frontmatter", body.startswith("---\n"))
        meta = loads_subset(body.split("---", 2)[1]) if body.startswith("---\n") else {}
        check(f"{name}: name matches directory", meta.get("name") == name, str(meta.get("name")))
        check(f"{name}: has description", bool(meta.get("description")))
        for section in required:
            check(f"{name}: {section}", section in body)
        if "mortgage-documents" in str(path):
            for section in doc_required:
                check(f"{name}: {section}", section in body)
            check(f"{name}: states it is not the underwriter",
                  "underwrit" in body.lower())


# -------------------------------------------------------------------- schemas
def test_schemas():
    schemas = sorted(ROOT.joinpath("schemas").glob("*.schema.json"))
    check("schemas found", len(schemas) >= 8, f"{len(schemas)} found")
    for path in schemas:
        data = json.loads(path.read_text(encoding="utf-8"))
        name = path.stem.replace(".schema", "")
        props = data.get("properties", {})
        for field in ("confidence", "human_verification_items",
                      "potential_inconsistencies", "source_references"):
            check(f"{name}: has {field}", field in props)
        check(f"{name}: disclaims underwriting",
              "underwriting" in data.get("description", "").lower())


# ------------------------------------------------------------------ synthetic
def test_synthetic_documents():
    docs = sorted(ROOT.joinpath("examples", "synthetic-documents").glob("*.pdf"))
    check("synthetic documents exist", len(docs) >= 6, f"{len(docs)} found")
    try:
        import pymupdf
    except ImportError:
        skip("synthetic documents labelled fictional", "pymupdf not installed")
        return
    for path in docs:
        doc = pymupdf.open(path)
        text = "".join(page.get_text() for page in doc)
        doc.close()
        check(f"{path.name}: labelled FICTIONAL", "FICTIONAL TEST DATA" in text)


# ----------------------------------------------------------------- extraction
def test_extraction():
    try:
        import pymupdf  # noqa: F401
    except ImportError:
        skip("extraction pipeline", "pymupdf not installed (use vendor/hermes-venv)")
        return
    import extract as extractor

    expected = {
        "synthetic-paystub.pdf": "paystub",
        "synthetic-w2.pdf": "w2",
        "synthetic-bank-statement.pdf": "bank_statement",
        "synthetic-purchase-contract.pdf": "purchase_contract",
        "synthetic-loan-estimate.pdf": "loan_estimate",
        "synthetic-mortgage-statement.pdf": "mortgage_statement",
        "synthetic-appraisal-excerpt.pdf": "appraisal",
    }
    base = ROOT / "examples" / "synthetic-documents"
    for filename, want in expected.items():
        path = base / filename
        if not path.exists():
            check(f"classify {filename}", False, "file missing")
            continue
        result = extractor.extract(path)
        check(f"classify {filename} -> {want}", result.document_type == want,
              f"got {result.document_type}")
        check(f"{filename}: extracted text", len(result.full_text) > 200,
              f"{len(result.full_text)} chars")


# ---------------------------------------------------------------- gitignore
def test_gitignore_protection():
    dangerous = [
        "local_data/borrower_documents/paystub.pdf",
        "local_data/models/model.gguf",
        "anywhere/model.gguf",
        "anywhere/weights.safetensors",
        "config/local-ai.yaml",
        "config/team-leader.yaml",
        "team-data/team.yaml",
        ".env",
        "hermes-home/config.yaml",
        "vendor/hermes-agent/README.md",
    ]
    for rel in dangerous:
        result = subprocess.run(["git", "check-ignore", "-q", rel], cwd=ROOT)
        check(f"gitignored: {rel}", result.returncode == 0)

    must_track = ["README.md", "local_data/README.md",
                  "examples/synthetic-documents/synthetic-paystub.pdf",
                  "skills/mortgage-documents/paystub-review/SKILL.md"]
    for rel in must_track:
        result = subprocess.run(["git", "check-ignore", "-q", rel], cwd=ROOT)
        check(f"tracked: {rel}", result.returncode != 0)


# ------------------------------------------------------------ needs the model
def test_local_inference(enabled: bool):
    if not enabled:
        skip("local inference round trip", "pass --local-ai to run")
        skip("local document review end to end", "pass --local-ai to run")
        return
    import server as srv

    if not srv.server_pid():
        skip("local inference round trip", "server not running")
        skip("local document review end to end", "server not running")
        return

    url = srv.base_url()
    check("server endpoint is loopback", "127.0.0.1" in url or "localhost" in url, url)

    result = srv.http_json(url + "/chat/completions", {
        "messages": [{"role": "user", "content": "Reply with exactly: OK"}],
        "max_tokens": 512, "temperature": 0, "stream": False}, timeout=300)
    check("local inference responds", bool(result))

    import review as rv
    path = ROOT / "examples" / "synthetic-documents" / "synthetic-paystub.pdf"
    outcome = rv.review(path, extract_only=False)
    check("review completed without error", "error" not in outcome,
          outcome.get("error", "")[:120])
    fields = outcome.get("fields") or {}
    check("review extracted employee name",
          "Testcase" in str(fields.get("employee_name", "")), str(fields.get("employee_name")))
    check("review extracted gross pay",
          "3109" in str(fields.get("gross_pay_current", "")).replace(",", ""),
          str(fields.get("gross_pay_current")))
    check("review used loopback",
          (outcome.get("inference") or {}).get("loopback") is True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local-ai", action="store_true",
                        help="also run tests that need a running local model")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    print("Team Leader OS — test suite\n")
    for fn in (test_miniyaml, test_manifest, test_tier_selection, test_privacy,
               test_skills, test_schemas, test_synthetic_documents,
               test_extraction, test_gitignore_protection):
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            FAILED.append((f"{fn.__name__} raised", repr(exc)))
    try:
        test_local_inference(args.local_ai)
    except Exception as exc:  # noqa: BLE001
        FAILED.append(("test_local_inference raised", repr(exc)))

    if args.verbose:
        for name, _ in PASSED:
            print(f"  PASS  {name}")
    for name, why in SKIPPED:
        print(f"  SKIP  {name} — {why}")
    for name, detail in FAILED:
        print(f"  FAIL  {name}" + (f" — {detail}" if detail else ""))

    total = len(PASSED) + len(FAILED)
    print(f"\n{len(PASSED)}/{total} passed, {len(SKIPPED)} skipped")
    if FAILED:
        print(f"{len(FAILED)} FAILED")
        return 1
    print("All tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
