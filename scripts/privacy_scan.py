#!/usr/bin/env python3
"""Scan for secrets and private information before anything reaches GitHub.

This repository is public. Run this before every commit and every push.

    python3 scripts/privacy_scan.py            scan files git would commit
    python3 scripts/privacy_scan.py --staged   scan only what is staged
    python3 scripts/privacy_scan.py --all      scan everything, ignored files too

Two severities:
  BLOCK  — a credential, key, or personal identifier. Do not commit.
  WARN   — worth a human look. Often a false positive in documentation.

This is a safety net, not a guarantee. It cannot recognize every possible
secret. The real protection is keeping private information in team-data/ and
never putting a real borrower, employee, or candidate into a tracked file.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (severity, label, pattern)
PATTERNS: list[tuple[str, str, re.Pattern]] = [
    # --- credentials -------------------------------------------------------
    ("BLOCK", "AWS access key id",      re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("BLOCK", "GitHub token",           re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("BLOCK", "GitHub fine-grained PAT",re.compile(r"\bgithub_pat_[A-Za-z0-9_]{60,}\b")),
    ("BLOCK", "Anthropic API key",      re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}")),
    ("BLOCK", "OpenAI API key",         re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_\-]{32,}")),
    ("BLOCK", "Slack token",            re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("BLOCK", "Google API key",         re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("BLOCK", "Stripe secret key",      re.compile(r"\b[sr]k_live_[A-Za-z0-9]{20,}\b")),
    ("BLOCK", "private key block",      re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("BLOCK", "JSON web token",         re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("BLOCK", "assigned secret",        re.compile(
        r"(?i)\b(?:api[_-]?key|secret|password|passwd|token|client[_-]?secret)\b\s*[:=]\s*"
        r"['\"]?(?!\s*$)(?!\$\{)(?!<)(?!your[_-])(?!例)[A-Za-z0-9/+_\-]{16,}")),

    # --- personal identifiers ---------------------------------------------
    ("BLOCK", "Social Security number", re.compile(r"\b(?!000|666|9\d\d)\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b")),
    ("BLOCK", "credit card number",     re.compile(r"\b(?:4\d{3}|5[1-5]\d{2}|3[47]\d{2}|6011)[ -]?\d{4}[ -]?\d{4}[ -]?\d{2,4}\b")),
    ("WARN",  "bank account-like number", re.compile(r"(?i)\b(?:account|acct|routing)\s*(?:number|no\.?|#)\s*[:=]?\s*\d{6,}")),

    # --- contact details ---------------------------------------------------
    ("WARN",  "email address",          re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("WARN",  "phone number",           re.compile(r"(?<![\d.-])(?:\+1[ -]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?![\d-])")),

    # --- mortgage-specific -------------------------------------------------
    ("WARN",  "loan number",            re.compile(r"(?i)\bloan\s*(?:number|no\.?|#)\s*[:=]?\s*\d{6,}")),
    ("WARN",  "credit score reference", re.compile(r"(?i)\b(?:fico|credit\s*score)\b\s*[:=]?\s*\d{3}\b")),
]

# Text that is fine to match because it is obviously an example or a template.
SAFE_MARKERS = (
    "example.com", "example.test", "@example", "example-northstar",
    "555-0", "0000000", "0000001", "0000100", "0000101", "0000102",
    "your-", "your_", "<your", "changeme", "xxxx", "redacted",
    "noreply@", "fictional",
)

# Files whose whole job is to describe these patterns.
SELF_REFERENTIAL = {
    "scripts/privacy_scan.py",
    "scripts/validate.py",
    ".env.example",
    "docs/privacy.md",
    "SECURITY.md",
}

SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".docx", ".xlsx",
                 ".zip", ".mp4", ".mov", ".db", ".sqlite", ".sqlite3", ".ico"}


def file_list(mode: str) -> list[Path]:
    if mode == "staged":
        args = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"]
    elif mode == "all":
        return [p for p in ROOT.rglob("*")
                if p.is_file() and ".git" not in p.parts and "vendor" not in p.parts]
    else:
        args = ["git", "ls-files", "--cached", "--others", "--exclude-standard"]
    try:
        out = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("warning: git not available; scanning the whole tree instead\n")
        return file_list("all")
    return [ROOT / line for line in out.splitlines() if line and (ROOT / line).is_file()]


def is_safe(line: str, match: str) -> bool:
    blob = (line + match).lower()
    return any(marker in blob for marker in SAFE_MARKERS)


def scan(paths: list[Path]):
    blocks, warns = [], []
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in SKIP_SUFFIXES or rel in SELF_REFERENTIAL:
            continue
        try:
            body = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(body.splitlines(), start=1):
            if len(line) > 4000:
                continue
            for severity, label, pattern in PATTERNS:
                for match in pattern.findall(line):
                    text = match if isinstance(match, str) else match[0]
                    if is_safe(line, text):
                        continue
                    snippet = line.strip()[:100]
                    record = (rel, number, label, snippet)
                    (blocks if severity == "BLOCK" else warns).append(record)
    return blocks, warns


def report(title: str, rows: list) -> None:
    if not rows:
        return
    print(f"\n{title}")
    for rel, number, label, snippet in rows[:40]:
        print(f"  {rel}:{number}")
        print(f"    {label}: {snippet}")
    if len(rows) > 40:
        print(f"  ... and {len(rows) - 40} more")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--staged", action="store_true", help="scan only staged changes")
    parser.add_argument("--all", action="store_true", help="scan every file, including ignored")
    args = parser.parse_args()

    mode = "staged" if args.staged else "all" if args.all else "tracked"
    paths = file_list(mode)
    print(f"Privacy scan — {len(paths)} file(s), mode: {mode}")

    blocks, warns = scan(paths)
    report("BLOCK — do not commit these:", blocks)
    report("WARN — check these are intentional:", warns)

    print()
    if blocks:
        print(f"FAILED: {len(blocks)} blocking finding(s), {len(warns)} warning(s).")
        print("Remove the secret or private data, then run this again.")
        print("Private information belongs in team-data/, which is gitignored.")
        return 1
    if warns:
        print(f"PASSED with {len(warns)} warning(s). Confirm each is an intentional example.")
        return 0
    print("PASSED: no secrets or personal information found in scanned files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
