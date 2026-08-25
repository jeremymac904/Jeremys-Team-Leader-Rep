#!/usr/bin/env python3
"""Local Privacy Mode — routing decisions and enforcement.

This module answers one question: *is this workflow allowed to leave the
machine?* Everything else in the local AI stack asks it before doing anything.

    python3 scripts/local_ai/privacy.py status
    python3 scripts/local_ai/privacy.py check paystub
    python3 scripts/local_ai/privacy.py check "marketing content"
    python3 scripts/local_ai/privacy.py on | off

Design rule: **fail closed**. Anything unrecognized is treated as
LOCAL_REQUIRED while privacy mode is on. Getting this wrong in the permissive
direction means a borrower's tax return goes to a cloud API, so the default
for "I do not know what this is" has to be "keep it here".

What this does and does not guarantee
-------------------------------------
This enforces *application-level* routing: the code will not call a cloud
endpoint for a LOCAL_REQUIRED workflow, and it verifies the inference endpoint
resolves to loopback. That is not the same as operating-system network
isolation. A hardened offline mode (firewall rules, a network namespace) is
documented as a future enhancement in docs/local-ai/privacy-mode.md, not
something this claims to already do.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from miniyaml import load_file  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG = ROOT / "config" / "local-ai.yaml"
CONFIG_EXAMPLE = ROOT / "config" / "local-ai.example.yaml"
AUDIT_DIR = ROOT / "local_data" / "audit"

LOCAL_REQUIRED = "LOCAL_REQUIRED"
LOCAL_PREFERRED = "LOCAL_PREFERRED"
CLOUD_ACCEPTABLE = "CLOUD_ACCEPTABLE"

# Substrings that mark a workflow as borrower data. Deliberately broad.
BORROWER_MARKERS = (
    "paystub", "pay stub", "payslip", "w2", "w-2", "1099", "tax return", "1040",
    "schedule c", "schedule e", "k1", "k-1", "bank statement", "asset",
    "credit report", "credit score", "tri-merge", "purchase contract",
    "sales contract", "loan estimate", "closing disclosure", "mortgage statement",
    "insurance", "hoa", "letter of explanation", "loe", "1003", "borrower",
    "application", "appraisal", "title", "payoff", "income", "deposit",
    "ssn", "social security", "account number", "document", "pdf", "scan",
)

TEAM_MARKERS = (
    "coaching note", "one-on-one", "one on one", "performance review",
    "production review", "scorecard", "candidate", "recruit", "team member",
    "loan officer note", "development plan", "accountability",
)

PUBLIC_MARKERS = (
    "guideline research", "marketing", "content", "training creation",
    "curriculum", "market research", "public", "social media", "blog",
    "general question", "automation design", "prompt",
)


class PrivacyViolation(RuntimeError):
    """Raised when something tries to send LOCAL_REQUIRED data to the cloud."""


def load_config() -> dict:
    path = CONFIG if CONFIG.exists() else CONFIG_EXAMPLE
    return load_file(path) or {}


def privacy_enabled(config: dict | None = None) -> bool:
    config = config or load_config()
    return bool((config.get("privacy_mode") or {}).get("enabled", True))


def classify(workflow: str, config: dict | None = None) -> tuple[str, str]:
    """Classify *workflow*. Returns (category, why)."""
    config = config or load_config()
    text = (workflow or "").strip().lower()

    if not text:
        return LOCAL_REQUIRED, "Empty description — failing closed."

    for marker in BORROWER_MARKERS:
        if marker in text:
            return LOCAL_REQUIRED, f"Matches borrower-data marker {marker!r}."

    for marker in TEAM_MARKERS:
        if marker in text:
            return LOCAL_PREFERRED, f"Matches internal-team marker {marker!r}."

    for marker in PUBLIC_MARKERS:
        if marker in text:
            return CLOUD_ACCEPTABLE, f"Matches public-work marker {marker!r}."

    if privacy_enabled(config):
        return LOCAL_REQUIRED, (
            "Unrecognized workflow and privacy mode is on — failing closed. "
            "Say explicitly what this is if it should be allowed to use the cloud."
        )
    return CLOUD_ACCEPTABLE, "Unrecognized, and privacy mode is off."


def is_loopback(url: str) -> bool:
    """True only if *url* points at this machine."""
    try:
        host = urllib.parse.urlparse(url).hostname
    except ValueError:
        return False
    if not host:
        return False
    if host in ("localhost", "localhost.localdomain"):
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def assert_local_allowed(workflow: str, endpoint_url: str, config: dict | None = None) -> None:
    """Raise PrivacyViolation if this call would breach Local Privacy Mode."""
    config = config or load_config()
    category, why = classify(workflow, config)
    if category != LOCAL_REQUIRED:
        return
    if not privacy_enabled(config):
        return
    if not is_loopback(endpoint_url):
        raise PrivacyViolation(
            f"BLOCKED. '{workflow}' is {LOCAL_REQUIRED} ({why})\n"
            f"The endpoint {endpoint_url!r} is not on this machine.\n\n"
            f"Local Privacy Mode is on, so this will not be sent. Nothing has left "
            f"your computer.\n\n"
            f"If you genuinely want to use a cloud model for this, turn privacy mode "
            f"off deliberately:\n"
            f"    python3 scripts/local_ai/privacy.py off"
        )


def explain_local_failure(step: str, detail: str, config: dict | None = None) -> str:
    """The message shown when a local step fails on a LOCAL_REQUIRED workflow.

    This is the no-silent-fallback path. It never proceeds on its own.
    """
    config = config or load_config()
    behavior = (config.get("privacy_mode") or {}).get("on_local_failure", "stop_and_ask")
    lines = [
        f"LOCAL STEP FAILED: {step}",
        f"  {detail}",
        "",
        "Local Privacy Mode is on, so nothing was sent anywhere. This document "
        "has not left your computer.",
        "",
    ]
    if behavior == "stop":
        lines.append("Configured behavior is 'stop': no cloud option is offered. "
                     "Fix the local problem and try again.")
    else:
        lines += [
            "Your options:",
            "  1. Fix the local problem and retry (see docs/local-ai/troubleshooting.md)",
            "  2. Do this step by hand",
            "  3. Explicitly approve a cloud model for THIS document only — which "
            "means its contents leave your computer",
            "",
            "Nothing happens until you choose. There is no automatic fallback.",
        ]
    return "\n".join(lines)


def audit(event: str, detail: dict, config: dict | None = None) -> None:
    """Append a local audit line. Never records document content."""
    config = config or load_config()
    if not (config.get("privacy_mode") or {}).get("audit_log", True):
        return
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    safe = {k: v for k, v in detail.items() if k not in ("text", "content", "body")}
    record = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "event": event, **safe}
    with (AUDIT_DIR / "privacy-audit.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


# --------------------------------------------------------------------------

def set_enabled(value: bool) -> int:
    if not CONFIG.exists():
        print("config/local-ai.yaml does not exist yet. Create it with:")
        print("  python3 scripts/local_ai/setup_local_ai.py")
        return 1
    text = CONFIG.read_text(encoding="utf-8")
    updated, done = [], False
    for line in text.split("\n"):
        if not done and line.strip().startswith("enabled:") and line.startswith("  "):
            updated.append(f"  enabled: {'true' if value else 'false'}")
            done = True
        else:
            updated.append(line)
    CONFIG.write_text("\n".join(updated), encoding="utf-8")
    print(f"Local Privacy Mode is now {'ON' if value else 'OFF'}.")
    if not value:
        print("\n  WARNING: borrower documents may now be sent to cloud models.")
        print("  Turn it back on with: python3 scripts/local_ai/privacy.py on")
    return 0


def status() -> int:
    config = load_config()
    on = privacy_enabled(config)
    using = CONFIG if CONFIG.exists() else CONFIG_EXAMPLE
    print("\n  Local Privacy Mode\n  " + "-" * 44)
    print(f"  Status        : {'ON' if on else 'OFF'}")
    print(f"  Config        : {using.relative_to(ROOT)}")
    print(f"  On failure    : {(config.get('privacy_mode') or {}).get('on_local_failure')}")
    print(f"  Audit log     : {(config.get('privacy_mode') or {}).get('audit_log')}")
    hybrid = (config.get("routing") or {}).get("hybrid") or {}
    print(f"  Hybrid mode   : {'enabled' if hybrid.get('enabled') else 'disabled'}"
          f" (approval always required: {hybrid.get('require_approval')})")
    print()
    if on:
        print("  Borrower documents are processed only on this machine.")
        print("  There is no silent cloud fallback.")
    else:
        print("  WARNING: privacy mode is OFF. Borrower data may reach cloud models.")
    print()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Local Privacy Mode controls.")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("status")
    sub.add_parser("on")
    sub.add_parser("off")
    check = sub.add_parser("check")
    check.add_argument("workflow", nargs="+")
    args = parser.parse_args()

    if args.command == "on":
        return set_enabled(True)
    if args.command == "off":
        return set_enabled(False)
    if args.command == "check":
        workflow = " ".join(args.workflow)
        category, why = classify(workflow)
        print(f"\n  Workflow : {workflow}")
        print(f"  Category : {category}")
        print(f"  Why      : {why}")
        if category == LOCAL_REQUIRED:
            print("  Result   : must be processed locally; will not be sent to a cloud model\n")
        elif category == LOCAL_PREFERRED:
            print("  Result   : local when available; you are asked before any cloud use\n")
        else:
            print("  Result   : cloud is acceptable — no borrower or employee data involved\n")
        return 0
    return status()


if __name__ == "__main__":
    raise SystemExit(main())
