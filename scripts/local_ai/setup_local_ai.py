#!/usr/bin/env python3
"""Set up local AI: detect hardware, pick a model, download it, configure Hermes.

    python3 scripts/local_ai/setup_local_ai.py              interactive
    python3 scripts/local_ai/setup_local_ai.py --dry-run    show the plan only
    python3 scripts/local_ai/setup_local_ai.py --yes        skip the download prompt
    python3 scripts/local_ai/setup_local_ai.py --model ID   download one model by id
    python3 scripts/local_ai/setup_local_ai.py --list       show downloaded models
    python3 scripts/local_ai/setup_local_ai.py --remove ID  delete a downloaded model

Model weights go to local_data/models/, which is gitignored. They are never
committed. Nothing downloads without you approving the size first.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from miniyaml import load_file  # noqa: E402
from hardware import detect  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST = ROOT / "local-ai" / "models.manifest.yaml"
CONFIG = ROOT / "config" / "local-ai.yaml"
CONFIG_EXAMPLE = ROOT / "config" / "local-ai.example.yaml"
MODELS_DIR = ROOT / "local_data" / "models"
HF_BASE = "https://huggingface.co/{repo}/resolve/main/{file}"


def human(gb: float) -> str:
    return f"{gb:.2f} GB"


def manifest() -> dict:
    return load_file(MANIFEST)


def model_by_id(model_id: str) -> dict | None:
    return next((m for m in manifest()["models"] if m["id"] == model_id), None)


def local_path(model: dict, which: str = "gguf") -> Path:
    filename = model["gguf_file"] if which == "gguf" else model["mmproj_file"]
    return MODELS_DIR / model["id"] / filename


def is_downloaded(model: dict) -> bool:
    return local_path(model, "gguf").exists() and local_path(model, "mmproj").exists()


def download_file(repo: str, filename: str, dest: Path) -> bool:
    """Stream one file from the Hugging Face Hub with a progress line."""
    url = HF_BASE.format(repo=repo, file=filename)
    dest.parent.mkdir(parents=True, exist_ok=True)
    partial = dest.with_suffix(dest.suffix + ".partial")

    if dest.exists():
        print(f"    already present: {dest.name}")
        return True

    print(f"    downloading {filename}")
    request = urllib.request.Request(url, headers={"User-Agent": "team-leader-os/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            total = int(response.headers.get("Content-Length") or 0)
            done = 0
            chunk_size = 1 << 20
            with partial.open("wb") as handle:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    handle.write(chunk)
                    done += len(chunk)
                    if total:
                        pct = done / total * 100
                        bar = "#" * int(pct / 2.5)
                        print(f"\r      [{bar:<40}] {pct:5.1f}%  "
                              f"{done/1e9:.2f}/{total/1e9:.2f} GB", end="", flush=True)
            print()
        partial.rename(dest)
        return True
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
        print(f"\n    FAILED: {exc}")
        partial.unlink(missing_ok=True)
        return False


def download_model(model: dict) -> bool:
    print(f"\n  {model['display_name']}")
    print(f"    repo: {model['hf_repo']}")
    ok = download_file(model["hf_repo"], model["gguf_file"], local_path(model, "gguf"))
    if ok and model.get("mmproj_file"):
        ok = download_file(model["hf_repo"], model["mmproj_file"], local_path(model, "mmproj"))
    return ok


def write_config(report: dict) -> None:
    """Create config/local-ai.yaml from the template, pinning the detected tier."""
    if not CONFIG.exists():
        shutil.copyfile(CONFIG_EXAMPLE, CONFIG)
        print(f"  created {CONFIG.relative_to(ROOT)}")

    text = CONFIG.read_text(encoding="utf-8")
    rec = report.get("recommended") or {}
    swaps = {
        "  tier: auto": f"  tier: {report['tier']}",
        "  reasoning_model: auto": f"  reasoning_model: {rec.get('reasoning_model', {}).get('id', 'auto')}",
        "  extraction_model: auto": f"  extraction_model: {rec.get('extraction_model', {}).get('id', 'auto')}",
    }
    for old, new in swaps.items():
        text = text.replace(old, new)
    CONFIG.write_text(text, encoding="utf-8")
    print(f"  pinned tier {report['tier']} in {CONFIG.relative_to(ROOT)}")


def list_models() -> int:
    data = manifest()
    print("\n  Local models\n  " + "-" * 62)
    for model in data["models"]:
        state = "downloaded" if is_downloaded(model) else "not downloaded"
        print(f"  [{state:>14}]  {model['id']:22} {human(model['download_size_gb']):>9}  "
              f"{model['status']}")
    used = 0.0
    if MODELS_DIR.exists():
        used = sum(f.stat().st_size for f in MODELS_DIR.rglob("*") if f.is_file()) / 1e9
    print(f"\n  Directory : {MODELS_DIR.relative_to(ROOT)}  (gitignored)")
    print(f"  Disk used : {used:.2f} GB\n")
    return 0


def remove_model(model_id: str) -> int:
    model = model_by_id(model_id)
    if not model:
        print(f"Unknown model id {model_id!r}. See --list.")
        return 1
    target = MODELS_DIR / model["id"]
    if not target.exists():
        print(f"{model_id} is not downloaded.")
        return 0
    size = sum(f.stat().st_size for f in target.rglob("*") if f.is_file()) / 1e9
    shutil.rmtree(target)
    print(f"Removed {model_id} and freed {size:.2f} GB.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Set up local AI for mortgage document review.")
    parser.add_argument("--dry-run", action="store_true", help="show the plan, download nothing")
    parser.add_argument("--yes", action="store_true", help="approve the download without asking")
    parser.add_argument("--model", help="download one specific model id")
    parser.add_argument("--list", action="store_true", help="list models and disk usage")
    parser.add_argument("--remove", help="delete a downloaded model by id")
    args = parser.parse_args()

    if args.list:
        return list_models()
    if args.remove:
        return remove_model(args.remove)

    print("\n  Local AI setup\n  " + "=" * 62)
    report = detect()

    print(f"\n  Detected : {report['os']} / {report['arch']} / {report['ram_gb']} GB RAM")
    print(f"             {report['accelerator']['name']} "
          f"(llama.cpp backend: {report['accelerator']['llama_cpp_backend']})")

    if not report.get("tier"):
        print(f"\n  {report['tier_reason']}")
        return 1

    print(f"\n  Tier     : {report['tier_name']}")
    print(f"  Why      : {report['tier_reason']}")

    if not report["runtime"]["installed"]:
        print("\n  llama.cpp is NOT installed. Install it first:")
        print("      macOS:   brew install llama.cpp")
        print("      Windows: winget install llama.cpp    (or download a release build)")
        print("      Linux:   see docs/local-ai/advanced.md")
        print("\n  Then run this again.")
        return 1
    print(f"  Runtime  : {report['runtime']['llama_server']}")

    if args.model:
        model = model_by_id(args.model)
        if not model:
            print(f"\n  Unknown model id {args.model!r}. See --list.")
            return 1
        targets = [model]
    else:
        rec = report["recommended"]
        targets = [model_by_id(rec["reasoning_model"]["id"]),
                   model_by_id(rec["extraction_model"]["id"])]

    pending = [m for m in targets if not is_downloaded(m)]
    total_gb = sum(m["download_size_gb"] for m in pending)

    print("\n  Models\n  " + "-" * 62)
    for model in targets:
        state = "already downloaded" if is_downloaded(model) else "will download"
        print(f"    {model['display_name']}")
        print(f"      role: {model['role']}   size: {human(model['download_size_gb'])}   "
              f"needs ~{model['ram_required_gb']} GB RAM   [{state}]")
        if model["status"] != "recommended":
            print(f"      NOTE: status is '{model['status']}'")

    if not pending:
        print("\n  Everything is already downloaded.")
    else:
        print(f"\n  Total to download: {human(total_gb)}")
        if args.dry_run:
            print("  --dry-run: stopping here.\n")
            return 0
        if not args.yes:
            print("\n  This downloads several gigabytes to local_data/models/ (gitignored).")
            try:
                reply = input("  Proceed? [y/N]: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\n  Cancelled.")
                return 1
            if reply not in ("y", "yes"):
                print("  Cancelled. Nothing was downloaded.")
                return 1

        for model in pending:
            if not download_model(model):
                print(f"\n  Download failed for {model['id']}. Nothing was configured.")
                return 1

    print("\n  Configuring\n  " + "-" * 62)
    write_config(report)

    print("""
  Done.

  Next:
    python3 scripts/local_ai/server.py start     start the local model
    python3 scripts/local_ai/server.py health    confirm it is running
    python3 scripts/local_ai/privacy.py status   confirm privacy mode

  Then try a fictional document:
    python3 scripts/local_ai/review.py examples/synthetic-documents/synthetic-paystub.pdf
""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
