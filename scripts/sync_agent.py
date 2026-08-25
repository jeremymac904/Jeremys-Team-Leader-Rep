#!/usr/bin/env python3
"""Load the Team Leader agent into this repository's isolated Hermes home.

Copies three things into ``hermes-home/``:

    SOUL.md                    the agent's identity, built from
                               agent/team-leader/SOUL.template.md with your
                               name and team filled in
    config.yaml                the Hermes profile, with ${REPO_PATH} resolved

Skills are NOT copied. The profile registers this repository's skills/ folder
as a Hermes external skills directory, so Hermes reads them in place and a
`git pull` updates them with no further action.

``hermes-home/`` is this repository's private HERMES_HOME. Nothing here reads
or writes ``~/.hermes`` or any other Hermes install on the machine.

    python3 scripts/sync_agent.py            sync
    python3 scripts/sync_agent.py --check    report drift, change nothing

Re-run it whenever you edit the SOUL template or the profile config.
Editing a skill needs no sync at all.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from miniyaml import load_file  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
HERMES_HOME = ROOT / "hermes-home"
SKILLS_SRC = ROOT / "skills"
SOUL_TEMPLATE = ROOT / "agent" / "team-leader" / "SOUL.template.md"
PROFILE_TEMPLATE = ROOT / "agent" / "team-leader" / "config.example.yaml"

# Fallbacks used when config/team-leader.yaml has not been created yet.
FALLBACKS = {
    "TEAM_LEADER_NAME": "your Team Leader",
    "TEAM_NAME": "your team",
    "REPO_PATH": str(ROOT),
}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def substitutions() -> dict[str, str]:
    values = dict(FALLBACKS)
    profile = ROOT / "config" / "team-leader.yaml"
    if profile.exists():
        try:
            identity = (load_file(profile) or {}).get("identity") or {}
        except Exception as exc:  # noqa: BLE001 - report, do not crash the sync
            print(f"  warning: could not read {rel(profile)}: {exc}")
            return values
        if identity.get("team_leader_name"):
            values["TEAM_LEADER_NAME"] = str(identity["team_leader_name"])
        if identity.get("team_name"):
            values["TEAM_NAME"] = str(identity["team_name"])
    return values


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("${" + key + "}", value)
    return text


def write_if_changed(dest: Path, content: str, check: bool) -> bool:
    """Return True if dest differs from content (and write it unless check)."""
    current = dest.read_text(encoding="utf-8") if dest.exists() else None
    if current == content:
        return False
    if not check:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
    return True




def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="report what would change and exit non-zero if anything would")
    args = parser.parse_args()

    for required in (SOUL_TEMPLATE, PROFILE_TEMPLATE, SKILLS_SRC):
        if not required.exists():
            raise SystemExit(f"missing {rel(required)} — is this the repository root?")

    values = substitutions()
    print(f"Syncing the Team Leader agent into {rel(HERMES_HOME)}/\n")
    print(f"  Team Leader: {values['TEAM_LEADER_NAME']}")
    print(f"  Team:        {values['TEAM_NAME']}\n")

    changed = 0

    soul = render(SOUL_TEMPLATE.read_text(encoding="utf-8"), values)
    if write_if_changed(HERMES_HOME / "SOUL.md", soul, args.check):
        changed += 1
        print(f"  {'stale' if args.check else 'wrote'}  hermes-home/SOUL.md")

    profile = render(PROFILE_TEMPLATE.read_text(encoding="utf-8"), values)
    if write_if_changed(HERMES_HOME / "config.yaml", profile, args.check):
        changed += 1
        print(f"  {'stale' if args.check else 'wrote'}  hermes-home/config.yaml")

    count = sum(1 for _ in SKILLS_SRC.rglob("SKILL.md"))
    print(f"  linked {count} skills from skills/ (read in place via "
          f"skills.external_dirs — not copied)")

    if args.check:
        if changed:
            print(f"\n{changed} item(s) out of date. Run: python3 scripts/sync_agent.py")
            return 1
        print("\nhermes-home/ is in sync.")
        return 0

    if changed == 0:
        print("\nAlready in sync — nothing to do.")
    else:
        print(f"\nDone. {changed} item(s) updated.")
    print("\n  Start the agent:  bash scripts/hermes.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
