#!/usr/bin/env python3
"""End-to-end local mortgage document review.

    python3 scripts/local_ai/review.py <file>
    python3 scripts/local_ai/review.py <file> --json
    python3 scripts/local_ai/review.py <file> --extract-only

The pipeline, in order, cheapest method first:

    file -> type detection -> native text / tables / local OCR
         -> document classification -> schema selection
         -> structured extraction by the local model
         -> validation -> structured output with page references

Every step runs on this machine. With Local Privacy Mode on, this refuses to
use a cloud endpoint, and when a local step fails it says so and stops rather
than quietly falling back.
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "lib"))
sys.path.insert(0, str(HERE))

from miniyaml import load_file  # noqa: E402
import privacy  # noqa: E402
import extract as extractor  # noqa: E402
import server as srv  # noqa: E402

ROOT = HERE.parent.parent
SCHEMA_DIR = ROOT / "schemas"

SCHEMA_FOR_TYPE = {
    "paystub": "paystub", "w2": "w2", "bank_statement": "bank_statement",
    "tax_return": "tax_return", "purchase_contract": "purchase_contract",
    "loan_estimate": "loan_estimate", "closing_disclosure": "closing_disclosure",
    "mortgage_statement": "mortgage_statement",
}

SKILL_FOR_TYPE = {
    "paystub": "paystub-review", "w2": "w2-review",
    "bank_statement": "bank-statement-review", "tax_return": "tax-return-review",
    "purchase_contract": "purchase-contract-review",
    "loan_estimate": "loan-estimate-review",
    "closing_disclosure": "closing-disclosure-review",
    "mortgage_statement": "mortgage-statement-review",
}

SYSTEM_PROMPT = (
    "You extract fields from mortgage documents. You are NOT an underwriter and you "
    "make no lending, credit, pricing, or eligibility decision.\n"
    "Rules:\n"
    "- Return ONLY a JSON object matching the requested schema. No prose, no markdown.\n"
    "- Copy values EXACTLY as they appear in the document, including commas.\n"
    "- Use null for anything not present. Never invent or infer a value.\n"
    "- Mask account numbers and any SSN.\n"
    "- Put anything uncertain into human_verification_items."
)


def load_schema(name: str) -> dict | None:
    path = SCHEMA_DIR / f"{name}.schema.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def encode_image(path: str) -> str | None:
    """Read a local image into a data URI for the multimodal endpoint.

    The image is read from disk and sent to 127.0.0.1 only. Nothing here
    reaches a network beyond loopback.
    """
    try:
        raw = Path(path).read_bytes()
    except OSError:
        return None
    suffix = Path(path).suffix.lower().lstrip(".") or "png"
    mime = "jpeg" if suffix in ("jpg", "jpeg") else suffix
    return f"data:image/{mime};base64," + base64.b64encode(raw).decode()


def call_local_model(prompt: str, url: str, timeout: int = 600,
                     images: list[str] | None = None) -> tuple[str | None, str]:
    """Call the local OpenAI-compatible endpoint. Returns (content, error).

    When *images* are supplied the request uses the multimodal content-parts
    form, which llama-server accepts when started with --mmproj.
    """
    if images:
        parts: list[dict] = [{"type": "text", "text": prompt}]
        for image in images:
            encoded = encode_image(image)
            if encoded:
                parts.append({"type": "image_url", "image_url": {"url": encoded}})
        user_content: object = parts
    else:
        user_content = prompt

    payload = {
        "messages": [{"role": "system", "content": SYSTEM_PROMPT},
                     {"role": "user", "content": user_content}],
        # Reasoning models emit a chain of thought before the answer, so this
        # budget has to cover both. Too low and content comes back empty.
        "temperature": 0, "max_tokens": 4096, "stream": False,
    }
    request = urllib.request.Request(
        url + "/chat/completions", data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode())
        message = data["choices"][0]["message"]
        content = message.get("content") or ""
        # Some models put the JSON in reasoning_content when they run out of
        # room for a separate answer. Fall back to it rather than reporting
        # a failure the model did not actually have.
        if not content.strip():
            content = message.get("reasoning_content") or ""
        return content, ""
    except urllib.error.HTTPError as exc:
        return None, f"HTTP {exc.code} from the local model: {exc.reason}"
    except (urllib.error.URLError, OSError) as exc:
        return None, f"Could not reach the local model at {url}: {exc}"
    except (KeyError, ValueError) as exc:
        return None, f"Unexpected response from the local model: {exc}"


def parse_json_object(text: str) -> dict | None:
    """Pull the first JSON object out of a model response."""
    if not text:
        return None
    body = text.strip()
    if "```" in body:
        parts = body.split("```")
        for part in parts:
            candidate = part.strip()
            if candidate.startswith("json"):
                candidate = candidate[4:].strip()
            if candidate.startswith("{"):
                body = candidate
                break
    start, depth, in_string, escape = body.find("{"), 0, False, False
    if start < 0:
        return None
    for index in range(start, len(body)):
        char = body[index]
        if escape:
            escape = False
            continue
        if char == "\\":
            escape = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(body[start:index + 1])
                except ValueError:
                    return None
    return None


def validate(fields: dict, schema: dict) -> list[str]:
    """Report schema fields that came back empty. Not a hard failure."""
    missing = []
    for name in schema.get("properties", {}):
        if name in ("confidence", "source_references", "potential_inconsistencies",
                    "missing_information", "human_verification_items"):
            continue
        value = fields.get(name)
        if value in (None, "", [], {}):
            missing.append(name)
    return missing


def field_spec(schema: dict) -> list[str]:
    """Describe each field with its TYPE, not just its name.

    Sending bare field names lets the model guess types, and it guesses wrong:
    a field declared as an array of schedule names came back as the boolean
    `true`. Stating the expected type per field fixes that, and it costs only a
    few tokens.
    """
    lines = []
    for name, spec in schema.get("properties", {}).items():
        if name == "source_references":
            continue
        kind = spec.get("type", "string")
        if kind == "array":
            item = (spec.get("items") or {}).get("type", "string")
            if item == "object":
                keys = list(((spec.get("items") or {}).get("properties") or {}).keys())
                hint = f"array of objects with keys {keys}" if keys else "array of objects"
            else:
                hint = f"array of {item}s — return [] if none apply, never true/false"
        elif kind == "boolean":
            hint = "true or false"
        else:
            hint = kind
        desc = (spec.get("description") or "").split(".")[0][:70]
        enum = spec.get("enum")
        if enum:
            hint = f"one of {enum}"
        lines.append(f'  "{name}": <{hint}>' + (f"   # {desc}" if desc else ""))
    return lines


def build_prompt(schema: dict, extraction) -> str:
    return (
        f"Extract these fields from the {extraction.document_type} below.\n\n"
        f"Return ONE JSON object with exactly these keys and these types:\n"
        + "\n".join(field_spec(schema))
        + "\n\nRules:\n"
        "- Respect the type of every field. A field described as an array must be a "
        "JSON array, never true/false and never a sentence.\n"
        "- Copy values exactly as written, including commas in numbers.\n"
        "- Use null for anything not present. Never invent a value.\n"
        "- Mask account numbers and any SSN.\n"
        "- List anything uncertain, unusual, or requiring a human in "
        "human_verification_items. An empty list means you are certain about "
        "every field, which is rare — say so only if true.\n\n"
        f"DOCUMENT:\n{extraction.full_text[:12000]}"
    )


def review(path: Path, extract_only: bool) -> dict:
    result: dict = {"file": path.name, "processed_locally": True, "steps": []}

    def step(name: str, status: str, detail: str = "") -> None:
        result["steps"].append({"step": name, "status": status, "detail": detail})

    # 1. Routing
    config = privacy.load_config()
    category, why = privacy.classify(f"{path.suffix} document {path.stem}", config)
    result["privacy"] = {
        "mode_enabled": privacy.privacy_enabled(config),
        "category": category, "reason": why,
    }
    step("privacy routing", "ok", f"{category}: {why}")

    # 2. Local extraction
    try:
        extraction = extractor.extract(path)
    except SystemExit as exc:
        step("extraction", "failed", str(exc))
        result["error"] = privacy.explain_local_failure("document extraction", str(exc), config)
        return result

    result["extraction"] = {
        "document_type": extraction.document_type,
        "classification_confidence": extraction.classification_confidence,
        "page_count": extraction.page_count,
        "methods_used": extraction.methods_used,
        "tables_found": len(extraction.tables),
        "characters": len(extraction.full_text),
        "warnings": extraction.warnings,
    }
    step("local extraction", "ok",
         f"{extraction.document_type} via {', '.join(extraction.methods_used)}")

    if extract_only:
        result["extracted_text"] = extraction.full_text
        return result

    vision_pages = [pg for pg in extraction.pages
                    if getattr(pg, "needs_vision", False) and getattr(pg, "image_path", "")]

    if not extraction.full_text.strip() and not vision_pages:
        detail = "No text could be read from this document, and no page image is available."
        step("extraction", "failed", detail)
        result["error"] = privacy.explain_local_failure("text extraction", detail, config)
        return result

    # 2b. A scanned page has no text to classify from. Ask the vision model.
    url = srv.base_url()
    if extraction.document_type == "unknown" and vision_pages:
        try:
            privacy.assert_local_allowed("scanned mortgage document", url, config)
        except privacy.PrivacyViolation as exc:
            step("privacy gate", "blocked", str(exc))
            result["error"] = str(exc)
            return result
        if not srv.server_pid():
            detail = ("This page needs the local vision model, which is not running.\n"
                      "    python3 scripts/local_ai/server.py start")
            step("vision classification", "failed", detail)
            result["error"] = privacy.explain_local_failure(
                "local vision classification", detail, config)
            return result

        known = ", ".join(sorted(SCHEMA_FOR_TYPE))
        guess, err = call_local_model(
            "Identify this mortgage document. Reply with ONLY one of these exact "
            f"labels and nothing else: {known}, unknown",
            url, images=[pg.image_path for pg in vision_pages][:1], timeout=300,
        )
        label = (guess or "").strip().lower()
        matched = next((k for k in SCHEMA_FOR_TYPE if k in label), None)
        if matched:
            extraction.document_type = matched
            extraction.classification_confidence = "moderate"
            result["extraction"]["document_type"] = matched
            result["extraction"]["classification_confidence"] = "moderate (via vision)"
            step("vision classification", "ok", f"identified as {matched}")
        else:
            step("vision classification", "failed",
                 f"could not identify the document type (model said: {label[:60]!r})")

    # 3. Schema
    schema_name = SCHEMA_FOR_TYPE.get(extraction.document_type)
    if not schema_name:
        step("schema selection", "skipped",
             f"No schema for document type '{extraction.document_type}'.")
        result["extracted_text"] = extraction.full_text
        return result
    schema = load_schema(schema_name)
    result["schema"] = schema_name
    result["suggested_skill"] = SKILL_FOR_TYPE.get(extraction.document_type)
    step("schema selection", "ok", f"schemas/{schema_name}.schema.json")

    # 4. Local model, with the privacy gate in front of it
    try:
        privacy.assert_local_allowed(f"{extraction.document_type} document", url, config)
    except privacy.PrivacyViolation as exc:
        step("privacy gate", "blocked", str(exc))
        result["error"] = str(exc)
        return result
    step("privacy gate", "ok", f"endpoint {url} is loopback")

    if not srv.server_pid():
        detail = ("The local model server is not running. Start it with:\n"
                  "    python3 scripts/local_ai/server.py start")
        step("local model", "failed", detail)
        result["error"] = privacy.explain_local_failure("local model inference", detail, config)
        return result

    prompt = build_prompt(schema, extraction)

    # Pages with no readable text layer are handed to the local vision model.
    images = [pg.image_path for pg in vision_pages]
    if images:
        step("vision extraction", "ok",
             f"page(s) {[pg.page for pg in vision_pages]} read by the local vision model")
        prompt = (
            "The page image(s) below could not be read as text. Read them visually and "
            "extract the fields.\n\n" + prompt
        )

    started = time.time()
    content, error = call_local_model(prompt, url, images=images or None)
    elapsed = time.time() - started

    if error:
        step("local model", "failed", error)
        result["error"] = privacy.explain_local_failure("local model inference", error, config)
        return result

    fields = parse_json_object(content or "")
    if fields is None:
        detail = "The local model did not return parseable JSON."
        step("structured extraction", "failed", detail)
        result["raw_model_output"] = (content or "")[:1500]
        result["error"] = privacy.explain_local_failure("structured extraction", detail, config)
        return result

    result["fields"] = fields
    result["empty_fields"] = validate(fields, schema)
    result["inference"] = {"endpoint": url, "loopback": privacy.is_loopback(url),
                           "seconds": round(elapsed, 1),
                           "vision_used": bool(images),
                           "vision_pages": [pg.page for pg in vision_pages]}
    step("structured extraction", "ok",
         f"{len(fields)} keys in {elapsed:.1f}s via {url}")

    privacy.audit("document_review", {
        "file": path.name, "document_type": extraction.document_type,
        "category": category, "endpoint": url, "loopback": privacy.is_loopback(url),
        "methods": extraction.methods_used,
    }, config)
    return result


def print_report(r: dict) -> None:
    print(f"\n  LOCAL DOCUMENT REVIEW — {r['file']}")
    print("  " + "=" * 62)

    p = r["privacy"]
    print(f"  Privacy mode : {'ON' if p['mode_enabled'] else 'OFF'}   "
          f"Routing: {p['category']}")

    if "extraction" in r:
        e = r["extraction"]
        print(f"  Document     : {e['document_type']} "
              f"(confidence: {e['classification_confidence']})")
        print(f"  Pages        : {e['page_count']}   read via: {', '.join(e['methods_used'])}")
        print(f"  Tables       : {e['tables_found']}   characters: {e['characters']}")

    if "inference" in r:
        i = r["inference"]
        print(f"  Inference    : {i['endpoint']}  loopback={i['loopback']}  {i['seconds']}s")
        if i.get("vision_used"):
            print(f"  Vision       : local vision model read page(s) {i['vision_pages']}")

    print("\n  Pipeline")
    for s in r["steps"]:
        mark = {"ok": "OK", "failed": "FAILED", "blocked": "BLOCKED", "skipped": "SKIP"}[s["status"]]
        print(f"    [{mark:>7}] {s['step']}")
        if s["detail"] and s["status"] != "ok":
            for line in s["detail"].splitlines()[:6]:
                print(f"              {line}")

    if r["extraction"]["warnings"] if "extraction" in r else None:
        print("\n  Extraction warnings")
        for w in r["extraction"]["warnings"]:
            print(f"    - {w}")

    if "fields" in r:
        print(f"\n  Extracted fields (schema: {r['schema']})")
        for key, value in r["fields"].items():
            if value in (None, "", [], {}):
                continue
            if isinstance(value, (list, dict)):
                rendered = json.dumps(value)
                rendered = rendered[:90] + ("..." if len(rendered) > 90 else "")
            else:
                rendered = str(value)[:90]
            print(f"    {key:34} {rendered}")
        if r.get("empty_fields"):
            print(f"\n  Not found in this document ({len(r['empty_fields'])}):")
            print("    " + ", ".join(r["empty_fields"][:14]))
        if r.get("suggested_skill"):
            print(f"\n  Next: interpret with the '{r['suggested_skill']}' skill.")

    if "error" in r:
        print("\n  " + "-" * 62)
        for line in r["error"].splitlines():
            print(f"  {line}")

    print("\n  NOT AN UNDERWRITING DECISION")
    print("  Extracted information and observations only. Not an approval, denial,")
    print("  income calculation, or eligibility determination. Verify every figure.\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Review a mortgage document locally.")
    parser.add_argument("file")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--extract-only", action="store_true")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"No such file: {path}")
        return 1

    result = review(path, args.extract_only)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)
    return 1 if "error" in result else 0


if __name__ == "__main__":
    raise SystemExit(main())
