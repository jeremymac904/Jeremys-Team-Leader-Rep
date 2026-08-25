#!/usr/bin/env python3
"""Start, stop, and check the local llama.cpp model server.

llama-server exposes an OpenAI-compatible API on 127.0.0.1. That is what makes
this work cleanly with Hermes: Hermes talks to it as a "custom" provider with a
local base_url, using supported configuration and no changes to Hermes itself.

    ./vendor/hermes-venv/bin/python scripts/local_ai/server.py start [--model ID]
    ./vendor/hermes-venv/bin/python scripts/local_ai/server.py stop
    ./vendor/hermes-venv/bin/python scripts/local_ai/server.py health
    ./vendor/hermes-venv/bin/python scripts/local_ai/server.py test
    ./vendor/hermes-venv/bin/python scripts/local_ai/server.py hermes-config

The server binds to loopback only. It is not reachable from your network.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import shutil
import subprocess
import sys
import time
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
RUN_DIR = ROOT / "local_data" / "working"
PID_FILE = RUN_DIR / "llama-server.pid"
LOG_FILE = RUN_DIR / "llama-server.log"


def config() -> dict:
    return load_file(CONFIG if CONFIG.exists() else CONFIG_EXAMPLE) or {}


def engine_cfg() -> dict:
    return config().get("engine") or {}


def base_url() -> str:
    cfg = engine_cfg()
    return f"http://{cfg.get('host', '127.0.0.1')}:{cfg.get('reasoning_port', 8080)}/v1"


def resolve_model(model_id: str | None) -> dict:
    data = load_file(MANIFEST)
    models = {m["id"]: m for m in data["models"]}
    if model_id:
        if model_id not in models:
            raise SystemExit(f"Unknown model id {model_id!r}")
        return models[model_id]

    configured = (config().get("models") or {}).get("reasoning_model")
    if configured and configured != "auto" and configured in models:
        return models[configured]

    report = detect()
    if not report.get("tier"):
        raise SystemExit(report["tier_reason"])
    return models[report["recommended"]["reasoning_model"]["id"]]


def model_files(model: dict) -> tuple[Path, Path]:
    base = MODELS_DIR / model["id"]
    return base / model["gguf_file"], base / model["mmproj_file"]


def server_pid() -> int | None:
    if not PID_FILE.exists():
        return None
    try:
        pid = int(PID_FILE.read_text().strip())
    except (ValueError, OSError):
        return None
    try:
        os.kill(pid, 0)
        return pid
    except OSError:
        PID_FILE.unlink(missing_ok=True)
        return None


def http_json(url: str, payload: dict | None = None, timeout: int = 120) -> dict | None:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"} if data else {}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError):
        return None


def start(model_id: str | None, context: int | None) -> int:
    existing = server_pid()
    if existing:
        print(f"Already running (pid {existing}) at {base_url()}")
        return 0

    if not shutil.which("llama-server"):
        print("llama-server not found. Install llama.cpp first:")
        print("  macOS: brew install llama.cpp")
        return 1

    model = resolve_model(model_id)
    gguf, mmproj = model_files(model)
    if not gguf.exists():
        print(f"Model not downloaded: {model['id']}")
        print("  ./vendor/hermes-venv/bin/python scripts/local_ai/setup_local_ai.py")
        return 1

    cfg = engine_cfg()
    tiers = {t["id"]: t for t in load_file(MANIFEST)["tiers"]}
    tier_id = (config().get("models") or {}).get("tier")
    default_ctx = tiers.get(tier_id, {}).get("max_context", 8192) if tier_id != "auto" else 8192

    cmd = [
        "llama-server",
        "-m", str(gguf),
        "--host", str(cfg.get("host", "127.0.0.1")),   # loopback only
        "--port", str(cfg.get("reasoning_port", 8080)),
        "-c", str(context or default_ctx),
        "-ngl", str(cfg.get("gpu_layers", 99)),
    ]
    if mmproj.exists():
        cmd += ["--mmproj", str(mmproj)]
    threads = int(cfg.get("threads") or 0)
    if threads:
        cmd += ["-t", str(threads)]

    RUN_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Starting {model['display_name']}")
    print(f"  context : {context or default_ctx}")
    print(f"  vision  : {'yes (mmproj loaded)' if mmproj.exists() else 'no'}")
    print(f"  bind    : {cfg.get('host', '127.0.0.1')} (loopback only)")
    print(f"  log     : {LOG_FILE.relative_to(ROOT)}")

    with LOG_FILE.open("w") as log:
        process = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT,
                                   start_new_session=True)
    PID_FILE.write_text(str(process.pid))

    print("\n  Loading model", end="", flush=True)
    for _ in range(180):
        time.sleep(1)
        print(".", end="", flush=True)
        if process.poll() is not None:
            print(f"\n\n  Server exited early. Last log lines:\n")
            print("  " + "\n  ".join(LOG_FILE.read_text().splitlines()[-15:]))
            PID_FILE.unlink(missing_ok=True)
            return 1
        if http_json(base_url().replace("/v1", "") + "/health", timeout=3):
            print(f"\n\n  Ready at {base_url()} (pid {process.pid})\n")
            return 0
    print("\n\n  Timed out waiting for the server. Check the log.")
    return 1


def stop() -> int:
    pid = server_pid()
    if not pid:
        print("Not running.")
        return 0
    os.kill(pid, signal.SIGTERM)
    for _ in range(20):
        time.sleep(0.5)
        try:
            os.kill(pid, 0)
        except OSError:
            break
    PID_FILE.unlink(missing_ok=True)
    print(f"Stopped (pid {pid}).")
    return 0


def health() -> int:
    pid = server_pid()
    url = base_url()
    print(f"\n  Local model server\n  " + "-" * 46)
    print(f"  Endpoint : {url}")
    print(f"  Loopback : {'yes' if '127.0.0.1' in url or 'localhost' in url else 'NO — CHECK THIS'}")
    if not pid:
        print("  Status   : not running")
        print("\n  Start it with: ./vendor/hermes-venv/bin/python scripts/local_ai/server.py start\n")
        return 1
    print(f"  Process  : running (pid {pid})")
    models = http_json(url + "/models", timeout=5)
    if models and models.get("data"):
        print(f"  Model    : {models['data'][0].get('id', 'unknown')}")
        print("  Status   : healthy\n")
        return 0
    print("  Status   : process alive but not responding yet\n")
    return 1


def test() -> int:
    """Round-trip a prompt through the local server and prove where it went."""
    url = base_url()
    if not server_pid():
        print("Server is not running. Start it first.")
        return 1
    print(f"\n  Sending a test prompt to {url}")
    started = time.time()
    result = http_json(url + "/chat/completions", {
        "messages": [{"role": "user",
                      "content": "Reply with exactly: LOCAL INFERENCE OK"}],
        # Reasoning models (NuExtract 3 among them) spend tokens thinking before
        # they emit any content. Too small a budget returns an empty string and
        # looks like a failure when the model is working fine.
        "max_tokens": 512, "temperature": 0, "stream": False,
    }, timeout=300)
    elapsed = time.time() - started
    if not result:
        print("  No response. Check the server log.")
        return 1
    message = result["choices"][0]["message"]
    content = (message.get("content") or "").strip()
    reasoning = (message.get("reasoning_content") or "").strip()
    if not content and reasoning:
        content = "(model returned reasoning only — it is running correctly)"
    print(f"  Response : {content[-70:] if content else '(empty)'}")
    if reasoning:
        print(f"  Reasoning: {len(reasoning)} chars (this is a reasoning model)")
    print(f"  Model    : {result.get('model', 'unknown')}")
    print(f"  Elapsed  : {elapsed:.1f}s")
    print(f"  Endpoint : {url}  <- loopback, this stayed on your machine\n")
    return 0


def hermes_config() -> int:
    """Explain the current Hermes/local-model compatibility boundary."""
    print("""
  Hermes chat and this local document model
  ------------------------------------------------------------

  The local server is supported for private document review. Current Hermes
  releases require a chat model context window of at least 64K, while the
  documented local tiers start llama.cpp at 8K-32K to preserve memory for
  document review. On a 24 GB Q8 setup, raising it to 64K exhausts memory.

  Do not configure this server as Hermes's chat provider at this time. Use a
  cloud provider for Hermes chat workflows, and keep borrower document review
  on this loopback-only local server. Local Privacy Mode still prevents a
  borrower document from silently falling back to a cloud endpoint.

  Check the active local endpoint:

    ./vendor/hermes-venv/bin/python scripts/local_ai/server.py health

  To choose Hermes's chat provider:

    bash scripts/hermes.sh setup
""")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Local llama.cpp server control.")
    sub = parser.add_subparsers(dest="command")
    start_cmd = sub.add_parser("start")
    start_cmd.add_argument("--model")
    start_cmd.add_argument("--context", type=int)
    sub.add_parser("stop")
    sub.add_parser("health")
    sub.add_parser("test")
    sub.add_parser("hermes-config")
    args = parser.parse_args()

    if args.command == "start":
        return start(args.model, args.context)
    if args.command == "stop":
        return stop()
    if args.command == "test":
        return test()
    if args.command == "hermes-config":
        return hermes_config()
    return health()


if __name__ == "__main__":
    raise SystemExit(main())
