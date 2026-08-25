#!/usr/bin/env python3
"""Detect just enough hardware to choose a local model. Nothing more.

This reads: operating system, CPU architecture, total RAM, and — where it can
be determined reliably — the accelerator (Apple Silicon GPU, NVIDIA, AMD, or
CPU only). It does not inspect files, serial numbers, or anything unrelated to
picking a model size.

    python3 scripts/local_ai/hardware.py           human-readable report
    python3 scripts/local_ai/hardware.py --json    machine-readable

Tier rule: memory rounds DOWN to the nearest supported tier. A 12 GB machine
gets the 8 GB tier, 18 GB gets 16 GB, 28 GB gets 24 GB. Guessing upward on a
non-standard configuration is how you end up swapping to disk mid-review.
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from miniyaml import load_file  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST = ROOT / "local-ai" / "models.manifest.yaml"

# Below the smallest tier we do not recommend local inference at all.
ABSOLUTE_MINIMUM_GB = 8


def _run(cmd: list[str]) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=10).stdout.strip()
    except (subprocess.SubprocessError, OSError):
        return ""


def total_ram_gb() -> float | None:
    system = platform.system()
    if system == "Darwin":
        raw = _run(["sysctl", "-n", "hw.memsize"])
        return round(int(raw) / (1024 ** 3), 1) if raw.isdigit() else None
    if system == "Linux":
        try:
            for line in Path("/proc/meminfo").read_text().splitlines():
                if line.startswith("MemTotal:"):
                    return round(int(line.split()[1]) / (1024 ** 2), 1)
        except (OSError, ValueError, IndexError):
            return None
        return None
    if system == "Windows":
        raw = _run(["wmic", "computersystem", "get", "TotalPhysicalMemory"])
        digits = [p for p in raw.split() if p.isdigit()]
        return round(int(digits[0]) / (1024 ** 3), 1) if digits else None
    return None


def accelerator() -> dict:
    """Identify the accelerator, and be explicit when we cannot."""
    system, machine = platform.system(), platform.machine()

    if system == "Darwin" and machine == "arm64":
        chip = _run(["sysctl", "-n", "machdep.cpu.brand_string"]) or "Apple Silicon"
        cores = ""
        profile = _run(["system_profiler", "SPDisplaysDataType"])
        for line in profile.splitlines():
            if "Total Number of Cores" in line:
                cores = line.split(":")[-1].strip()
                break
        return {
            "kind": "apple-silicon",
            "name": chip,
            "gpu_cores": cores or "unknown",
            "unified_memory": True,
            "llama_cpp_backend": "Metal",
            "detection_confidence": "high",
        }

    if system == "Darwin":
        return {"kind": "intel-mac", "name": _run(["sysctl", "-n", "machdep.cpu.brand_string"]) or "Intel Mac",
                "unified_memory": False, "llama_cpp_backend": "CPU (Metal limited on Intel Macs)",
                "detection_confidence": "high"}

    if shutil.which("nvidia-smi"):
        out = _run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"])
        if out:
            first = out.splitlines()[0]
            name, _, vram = first.partition(",")
            return {"kind": "nvidia", "name": name.strip(), "vram": vram.strip(),
                    "unified_memory": False, "llama_cpp_backend": "CUDA",
                    "detection_confidence": "high"}

    if system == "Linux" and shutil.which("rocm-smi"):
        return {"kind": "amd", "name": "AMD GPU (ROCm detected)", "unified_memory": False,
                "llama_cpp_backend": "ROCm", "detection_confidence": "medium"}

    return {"kind": "cpu", "name": platform.processor() or machine, "unified_memory": False,
            "llama_cpp_backend": "CPU",
            "detection_confidence": "low — no GPU detected, assuming CPU only"}


def select_tier(ram_gb: float | None, tiers: list[dict]) -> tuple[dict | None, str]:
    """Round DOWN to the largest tier this machine can actually support."""
    if ram_gb is None:
        return None, "Could not read total memory. Choose a tier manually in config/local-ai.yaml."
    if ram_gb < ABSOLUTE_MINIMUM_GB:
        return None, (f"{ram_gb} GB is below the {ABSOLUTE_MINIMUM_GB} GB minimum for local "
                      f"inference. Use a cloud model, or use local extraction only.")

    ordered = sorted(tiers, key=lambda t: t["min_ram_gb"])
    chosen = None
    for tier in ordered:
        if ram_gb >= tier["min_ram_gb"]:
            chosen = tier
    exact = chosen and abs(ram_gb - chosen["min_ram_gb"]) < 0.5
    if exact:
        reason = f"{ram_gb} GB matches the {chosen['min_ram_gb']} GB tier."
    else:
        reason = (f"{ram_gb} GB is not a standard tier size, so it rounds DOWN to the "
                  f"{chosen['min_ram_gb']} GB tier. Rounding up would leave too little "
                  f"memory for the OS, Hermes, and document extraction.")
    return chosen, reason


def runtime_status() -> dict:
    return {
        "llama_server": shutil.which("llama-server"),
        "llama_mtmd_cli": shutil.which("llama-mtmd-cli"),
        "installed": bool(shutil.which("llama-server")),
    }


def detect() -> dict:
    manifest = load_file(MANIFEST)
    ram = total_ram_gb()
    tier, reason = select_tier(ram, manifest["tiers"])
    models = {m["id"]: m for m in manifest["models"]}

    report = {
        "os": platform.system(),
        "os_release": platform.release(),
        "arch": platform.machine(),
        "cpu_count": _run(["sysctl", "-n", "hw.ncpu"]) or str(__import__("os").cpu_count() or "unknown"),
        "ram_gb": ram,
        "accelerator": accelerator(),
        "runtime": runtime_status(),
        "tier": tier["id"] if tier else None,
        "tier_name": tier["name"] if tier else None,
        "tier_reason": reason,
    }
    if tier:
        reasoning = models[tier["reasoning_model"]]
        extraction = models[tier["extraction_model"]]
        report["recommended"] = {
            "reasoning_model": {
                "id": reasoning["id"], "display_name": reasoning["display_name"],
                "hf_repo": reasoning["hf_repo"], "gguf_file": reasoning["gguf_file"],
                "mmproj_file": reasoning["mmproj_file"],
                "download_size_gb": reasoning["download_size_gb"],
                "ram_required_gb": reasoning["ram_required_gb"],
                "status": reasoning["status"],
            },
            "extraction_model": {
                "id": extraction["id"], "display_name": extraction["display_name"],
                "hf_repo": extraction["hf_repo"], "gguf_file": extraction["gguf_file"],
                "mmproj_file": extraction["mmproj_file"],
                "download_size_gb": extraction["download_size_gb"],
            },
            "total_download_gb": round(reasoning["download_size_gb"] + extraction["download_size_gb"], 2),
            "max_context": tier["max_context"],
            "headroom_note": tier["headroom_note"],
        }
    return report


def print_report(r: dict) -> None:
    print("\n  Hardware detection\n  " + "-" * 46)
    print(f"  Operating system : {r['os']} {r['os_release']}")
    print(f"  Architecture     : {r['arch']}")
    print(f"  CPU cores        : {r['cpu_count']}")
    print(f"  Total memory     : {r['ram_gb']} GB" if r["ram_gb"] else "  Total memory     : could not detect")

    acc = r["accelerator"]
    print(f"  Accelerator      : {acc['name']}")
    print(f"                     type: {acc['kind']}, llama.cpp backend: {acc['llama_cpp_backend']}")
    if acc.get("gpu_cores") and acc["gpu_cores"] != "unknown":
        print(f"                     GPU cores: {acc['gpu_cores']}")
    print(f"                     confidence: {acc['detection_confidence']}")

    rt = r["runtime"]
    print(f"  llama.cpp        : {rt['llama_server'] if rt['installed'] else 'NOT INSTALLED'}")

    print("\n  Recommendation\n  " + "-" * 46)
    if not r.get("tier"):
        print(f"  No supported tier. {r['tier_reason']}")
        return
    print(f"  Tier             : {r['tier_name']}")
    print(f"  Why              : {r['tier_reason']}")
    rec = r["recommended"]
    print(f"\n  Reasoning model  : {rec['reasoning_model']['display_name']}")
    print(f"                     {rec['reasoning_model']['hf_repo']}")
    print(f"                     {rec['reasoning_model']['download_size_gb']} GB download, "
          f"~{rec['reasoning_model']['ram_required_gb']} GB RAM to run")
    if rec["reasoning_model"]["status"] != "recommended":
        print(f"                     STATUS: {rec['reasoning_model']['status']}")
    print(f"  Extraction model : {rec['extraction_model']['display_name']}")
    print(f"                     {rec['extraction_model']['download_size_gb']} GB download")
    print(f"\n  Total download   : {rec['total_download_gb']} GB")
    print(f"  Context          : up to {rec['max_context']:,} tokens")
    print(f"  Note             : {rec['headroom_note']}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect hardware and recommend a local model tier.")
    parser.add_argument("--json", action="store_true", help="output JSON")
    args = parser.parse_args()
    report = detect()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)
    return 0 if report.get("tier") else 1


if __name__ == "__main__":
    raise SystemExit(main())
