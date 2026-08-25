#!/usr/bin/env python3
"""Make the Team Leader skills available in Hermes from any directory.

Adds this repository's .hermes/skills/ to skills.external_dirs in your Hermes
config, which Hermes loads globally. Nothing is copied, so `git pull` updates
your skills. Safe to run repeatedly.

    python3 scripts/install_global_skills.py
    python3 scripts/install_global_skills.py --check
"""
from __future__ import annotations
import argparse, os, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".hermes" / "skills"


def hermes_home() -> Path:
    env = os.environ.get("HERMES_HOME", "").strip()
    return Path(env) if env else Path.home() / ".hermes"


def config_path() -> Path:
    return hermes_home() / "config.yaml"


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def already_listed(text: str, target: str) -> bool:
    return target in text


def add_external_dir(text: str, target: str) -> str:
    """Insert target under skills.external_dirs, preserving everything else."""
    lines = text.split("\n") if text else []
    entry = f'    - "{target}"'

    # Find a top-level `skills:` block.
    idx = next((i for i, l in enumerate(lines) if l.rstrip() == "skills:"), None)
    if idx is None:
        block = ["skills:", "  external_dirs:", entry]
        if lines and lines[-1].strip() != "":
            lines.append("")
        return "\n".join(lines + block) + "\n"

    # Inside skills:, look for external_dirs.
    end = len(lines)
    for i in range(idx + 1, len(lines)):
        l = lines[i]
        if l.strip() and not l.startswith((" ", "\t")):
            end = i
            break
    ext = next((i for i in range(idx + 1, end)
                if lines[i].strip().startswith("external_dirs:")), None)
    if ext is None:
        lines.insert(idx + 1, entry)
        lines.insert(idx + 1, "  external_dirs:")
        return "\n".join(lines)

    # Append after the last list item of external_dirs.
    last = ext
    for i in range(ext + 1, end):
        if lines[i].strip().startswith("- "):
            last = i
        elif lines[i].strip():
            break
    if lines[ext].strip() == "external_dirs:" or lines[ext].strip() == "external_dirs: []":
        lines[ext] = "  external_dirs:"
    lines.insert(last + 1, entry)
    return "\n".join(lines)


def skill_count() -> int:
    return len(list(SKILLS.rglob("SKILL.md")))


def verify_global() -> tuple[bool, str]:
    """Ask Hermes, from OUTSIDE the repo, whether the skills are visible."""
    exe = shutil.which("hermes") or str(ROOT / "vendor" / "hermes-venv" / "bin" / "hermes")
    if not Path(exe).exists() and not shutil.which("hermes"):
        return False, "hermes command not found — install Hermes, then re-run this."
    try:
        out = subprocess.run([exe, "skills", "list"], cwd=str(Path.home()),
                             capture_output=True, text=True, timeout=180).stdout
    except (OSError, subprocess.SubprocessError) as exc:
        return False, f"could not run `hermes skills list`: {exc}"
    expected = len(list(SKILLS.rglob("SKILL.md")))
    # Hermes prints e.g. "0 hub-installed, 0 builtin, 35 local — 35 enabled".
    m = re.search(r"(\d+)\s+local", out)
    found = int(m.group(1)) if m else 0
    return found >= expected, (f"{found} skills visible from {Path.home()} "
                               f"(expected at least {expected})")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="report status, change nothing")
    args = ap.parse_args()

    cfg = config_path()
    target = str(SKILLS)
    text = read(cfg)
    listed = already_listed(text, target)

    print(f"\n  Hermes config : {cfg}")
    print(f"  Skills folder : {target}")
    print(f"  Skills found  : {skill_count()}")
    print(f"  Registered    : {'yes' if listed else 'no'}")

    if args.check:
        ok, detail = verify_global()
        print(f"  Global check  : {detail}\n")
        return 0 if (listed and ok) else 1

    if not SKILLS.is_dir():
        print("\n  ERROR: .hermes/skills/ not found. Is this the repository root?\n")
        return 1

    if listed:
        print("\n  Already registered — nothing to change.")
    else:
        cfg.parent.mkdir(parents=True, exist_ok=True)
        if text:
            backup = cfg.with_suffix(".yaml.bak")
            backup.write_text(text, encoding="utf-8")
            print(f"  Backup        : {backup}")
        cfg.write_text(add_external_dir(text, target), encoding="utf-8")
        print("\n  Registered the Team Leader skills globally.")

    # Old project-local trust entry is now redundant but harmless; leave team
    # data and every other setting untouched.
    ok, detail = verify_global()
    print(f"  Verified      : {detail}")
    if not ok:
        print("\n  If the count is 0, restart Hermes Desktop so it reloads the config.")
    print("""
  Done. Your Team Leader skills now load in any Hermes session, from any folder.
  `git pull` in this repository updates them — nothing to reinstall.
""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
