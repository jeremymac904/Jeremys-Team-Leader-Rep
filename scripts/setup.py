#!/usr/bin/env python3
"""Set up your Team Leader OS.

Asks you a short set of questions and writes your configuration files. Nothing
leaves your machine and nothing is sent anywhere.

    python3 scripts/setup.py              # interactive
    python3 scripts/setup.py --demo       # fictional sample team, no questions
    python3 scripts/setup.py --check      # report what is configured, change nothing

Files it creates (all gitignored — none of this is ever uploaded anywhere):
    config/team-leader.yaml   who you are, your goals, how you lead
    config/coaching.yaml      how you coach
    config/marketing.yaml     marketing defaults and per-LO profiles
    config/integrations.yaml  what is connected
    team-data/team.yaml       your roster  (private)
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (destination, template, description)
TARGETS = [
    (ROOT / "config/team-leader.yaml", ROOT / "config/team-leader.example.yaml",
     "your identity, market, goals, KPIs, schedule, and permissions"),
    (ROOT / "config/coaching.yaml", ROOT / "config/coaching.example.yaml",
     "how you run coaching and when to escalate"),
    (ROOT / "config/integrations.yaml", ROOT / "config/integrations.example.yaml",
     "which services are connected (none, by default)"),
    (ROOT / "config/marketing.yaml", ROOT / "config/marketing.example.yaml",
     "marketing defaults and per-Loan-Officer profiles"),
    (ROOT / "team-data/team.yaml", ROOT / "config/team.example.yaml",
     "your roster — PRIVATE, never committed"),
]

# Interview questions -> dotted path in team-leader.yaml, with a default.
QUESTIONS = [
    ("identity.team_leader_name", "Your name", "Avery Sample"),
    ("identity.team_name", "Your team's name", "Northstar Lending Team"),
    ("identity.email", "Your work email", ""),
    ("identity.phone", "Your phone", ""),
    ("identity.team_leader_nmls", "Your NMLS ID", ""),
    ("identity.company_nmls", "Company NMLS ID", ""),
    ("identity.timezone", "Your timezone (e.g. America/New_York)", "America/New_York"),
    ("identity.working_hours", "Your working hours", "8:00am - 5:00pm, Mon-Fri"),
    ("market.primary_market", "Your primary market", ""),
    ("market.team_states", "States you lend in (comma separated)", "FL"),
    ("goals.production_goals.team_units_per_month", "Team units per month goal", "30"),
    ("goals.production_goals.personal_units_per_month", "YOUR OWN units per month goal", "6"),
    ("goals.recruiting_goals.hires_per_quarter", "Hires per quarter goal", "2"),
    ("leadership.coaching_style",
     "Coaching style (direct-supportive / socratic / structured / hands-off)",
     "direct-supportive"),
    ("leadership.preferred_communication_style",
     "How you want the agent to talk to you",
     "short, specific, no filler; lead with the number"),
]

BANNER = """
  Loan Factory Team Leader OS — setup
  ------------------------------------
  A few questions. Press Enter to accept the default in [brackets].
  Nothing is sent anywhere; this only writes files on your machine.
"""


# --------------------------------------------------------------------------

def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def check() -> int:
    print("Configuration status\n")
    missing = 0
    for dest, _, description in TARGETS:
        mark = "OK     " if dest.exists() else "MISSING"
        if not dest.exists():
            missing += 1
        print(f"  [{mark}] {relative(dest):<32} {description}")
    print()
    if missing:
        print(f"{missing} file(s) not yet created. Run:  python3 scripts/setup.py")
        return 1
    print("All configuration files exist. Next: python3 scripts/validate.py")
    return 0


def copy_templates(force: bool) -> list[Path]:
    written = []
    for dest, template, _ in TARGETS:
        if dest.exists() and not force:
            print(f"  keeping existing {relative(dest)}")
            continue
        if not template.exists():
            raise SystemExit(f"template missing: {relative(template)}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(template, dest)
        written.append(dest)
        print(f"  wrote {relative(dest)}")
    return written


def set_scalar(text: str, dotted: str, value: str) -> str:
    """Replace the value of a dotted key path in a simple YAML document.

    Deliberately line-based rather than a parse/re-emit round trip: that keeps
    every comment in the template intact, which is most of what makes these
    files usable by a non-engineer.
    """
    parts = dotted.split(".")
    lines = text.split("\n")
    depth = 0
    start = 0
    for level, part in enumerate(parts):
        want_indent = level * 2
        prefix = " " * want_indent + part + ":"
        found = None
        for i in range(start, len(lines)):
            line = lines[i]
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            indent = len(line) - len(line.lstrip(" "))
            if level > 0 and indent < want_indent:
                break
            if line.startswith(prefix):
                found = i
                break
        if found is None:
            return text  # key not present in this template; leave it alone
        if level == len(parts) - 1:
            lines[found] = f"{' ' * want_indent}{part}: {value}"
            return "\n".join(lines)
        start, depth = found + 1, want_indent
    return "\n".join(lines)


def quote(value: str) -> str:
    return '"' + value.replace('"', "'") + '"'


def as_yaml_value(dotted: str, raw: str) -> str:
    raw = raw.strip()
    if dotted.endswith("team_states"):
        items = [quote(s.strip().upper()) for s in raw.split(",") if s.strip()]
        return "[" + ", ".join(items) + "]"
    if raw.isdigit():
        return raw
    return quote(raw)


def interview() -> dict:
    answers = {}
    for dotted, question, default in QUESTIONS:
        suffix = f" [{default}]" if default else ""
        try:
            reply = input(f"  {question}{suffix}: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  (stopping — using defaults for the rest)")
            break
        answers[dotted] = reply or default
    return answers


def apply_answers(answers: dict) -> None:
    profile = ROOT / "config/team-leader.yaml"
    text = profile.read_text(encoding="utf-8")
    for dotted, raw in answers.items():
        if raw == "":
            continue
        text = set_scalar(text, dotted, as_yaml_value(dotted, raw))
    profile.write_text(text, encoding="utf-8")
    print(f"  personalized {relative(profile)}")


def check_skills_trusted() -> bool:
    """Report whether Hermes has been told to trust this project's skills."""
    import subprocess
    try:
        out = subprocess.run(["hermes", "skills", "list"], cwd=ROOT,
                             capture_output=True, text=True, timeout=90).stdout
    except (OSError, subprocess.SubprocessError):
        return False
    return " local" in out and "0 hub-installed, 0 builtin, 0 local" not in out


def ensure_team_data() -> None:
    for sub in ("coaching", "scorecards", "notes"):
        (ROOT / "team-data" / sub).mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Set up your Team Leader OS.")
    parser.add_argument("--demo", action="store_true",
                        help="use the fictional sample team; ask nothing")
    parser.add_argument("--check", action="store_true",
                        help="report what is configured and exit")
    parser.add_argument("--force", action="store_true",
                        help="overwrite configuration files that already exist")
    args = parser.parse_args()

    if args.check:
        return check()

    print(BANNER)
    print("Creating configuration files:")
    copy_templates(force=args.force)
    ensure_team_data()

    if args.demo:
        print("\n  --demo: keeping the fictional Northstar Lending Team as-is.")
    else:
        print("\nTell me about you and your team:\n")
        apply_answers(interview())


    print("""
Done. Your answers are saved on this computer only.

  NEXT: put your real team in       team-data/team.yaml
        (open it and replace the fictional Northstar team)

        The two fields that matter most for each person:
          experience_level  new | developing | established | top-producer
          development_areas what they actually struggle with, specifically
""")

    if not check_skills_trusted():
        print("""  ONE MORE STEP: Hermes has not been told to trust this folder's skills yet.

        hermes skills trust

        You should see "35 project skill(s) will load".
""")

    print("""  THEN: start your agent from inside this folder

        hermes

        and ask:  Give me my Team Leader morning briefing.
""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
