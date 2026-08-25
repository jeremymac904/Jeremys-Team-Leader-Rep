#!/usr/bin/env python3
"""Check that this repository is well-formed.

Runs a series of independent checks and prints a pass/fail line for each.
Exit code is 0 only when every check passes.

    python3 scripts/validate.py

What it checks:
  * the files the system depends on exist
  * every SKILL.md has valid frontmatter and all required sections
  * every automation card has all required fields, and none is active
  * automations/README.md matches catalog.yaml
  * every config template parses and has the expected shape
  * hermes-home/ is in sync with agent/ (if it exists)
  * the Hermes profile uses real config keys and real toolset names
  * no absolute machine paths leaked into tracked files
  * relative Markdown links point at files that exist
  * example data is labelled as fictional
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from miniyaml import loads_subset  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".hermes" / "skills"

REQUIRED_FILES = [
    "README.md", "LICENSE", ".gitignore", ".env.example", "AGENTS.md",
    "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", "PROJECT_STATUS.md",
    "agent/team-leader/SOUL.template.md",
    "agent/team-leader/config.example.yaml",
    ".hermes/skills/README.md",
    "config/local-ai.example.yaml",
    "local-ai/models.manifest.yaml",
    "local-ai/VALIDATION.md",
    "scripts/local_ai/hardware.py",
    "scripts/local_ai/privacy.py",
    "scripts/local_ai/extract.py",
    "scripts/local_ai/review.py",
    "scripts/local_ai/server.py",
    "scripts/local_ai/setup_local_ai.py",
    "tests/run_tests.py",
    "docs/local-ai/README.md",
    "docs/local-ai/privacy-mode.md",
    "config/team-leader.example.yaml",
    "config/team.example.yaml",
    "config/coaching.example.yaml",
    "config/integrations.example.yaml",
    "automations/catalog.yaml",
    "automations/schema.md",
    "automations/README.md",
    "scripts/setup.py", "scripts/validate.py", "scripts/privacy_scan.py",
    "scripts/sync_agent.py", "scripts/install_hermes.sh", "scripts/hermes.sh",
    "team-data/README.md",
    "docs/README.md",
]

SKILL_SECTIONS = [
    "## Purpose", "## When Hermes should use it", "## Required information",
    "## Workflow", "## Expected output", "## Safety boundaries",
    "## Human approval requirements", "## Related skills",
    "## What this skill must not assume", "## Tests",
]

AUTOMATION_FIELDS = [
    "id", "name", "category", "objective", "trigger", "cadence", "data_needed",
    "skill", "prompt", "output", "approval_required", "privacy", "setup",
    "customization", "time_saved_per_month",
]

# Automations that can produce an outward effect must require approval.
#
# Two rules, because a keyword scan alone both misses cases and produces false
# positives (a *review* skill mentions "publish" without ever publishing):
#   1. Any automation producing publishable marketing content.
#   2. Anything whose description implies contacting a person.
OUTWARD_KEYWORDS = ("send", "contact", "outreach", "message to", "publish to")
CONTENT_PRODUCING = {
    "marketing-weekly-content-plan", "marketing-daily-content-ideas",
    "marketing-market-news-to-content", "marketing-guideline-to-realtor-education",
    "marketing-content-repurposing", "marketing-video-script-batch",
    "marketing-team-training-segment", "marketing-campaign-followup",
}

CONFIG_SHAPE = {
    "config/team-leader.example.yaml": ["identity", "market", "goals", "leadership", "schedule", "permissions"],
    "config/team.example.yaml": ["members", "standards", "recruiting_pipeline"],
    "config/coaching.example.yaml": ["one_on_one", "tracks", "intervention_triggers", "guardrails"],
    "config/integrations.example.yaml": ["integrations"],
}

# Paths that would identify one specific machine or person.
LEAKY_PATH = re.compile(r"(/Users/[A-Za-z0-9._-]+|/Volumes/[A-Za-z0-9._ '-]+/|/home/[A-Za-z0-9._-]+)")
LINK = re.compile(r"\[[^\]]*\]\(([^)#]+?)(?:#[^)]*)?\)")

results: list[tuple[bool, str, list[str]]] = []


def check(name: str):
    """Decorator: run a check function that returns a list of problem strings."""
    def wrap(fn):
        problems = fn()
        results.append((not problems, name, problems))
        return fn
    return wrap


def tracked_files() -> list[Path]:
    """Files git would actually commit — the only ones that can leak."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
    return [ROOT / line for line in out.splitlines() if line and (ROOT / line).is_file()]


def text_files() -> list[Path]:
    keep = {".md", ".yaml", ".yml", ".py", ".sh", ".txt", ".json", ".example"}
    return [p for p in tracked_files() if p.suffix in keep or p.name == ".env.example"]


# --------------------------------------------------------------------------

@check("required files exist")
def _required():
    return [f"missing {f}" for f in REQUIRED_FILES if not (ROOT / f).exists()]


@check("skills are well-formed")
def _skills():
    problems = []
    paths = sorted(SKILLS_DIR.rglob("SKILL.md"))
    if not paths:
        return ["no skills found in .hermes/skills/"]
    for path in paths:
        skill = path.parent
        body = path.read_text(encoding="utf-8")
        if not body.startswith("---\n"):
            problems.append(f"{skill.name}: missing YAML frontmatter")
        else:
            head = body.split("---", 2)[1]
            meta = loads_subset(head) or {}
            if meta.get("name") != skill.name:
                problems.append(
                    f"{skill.name}: frontmatter name is {meta.get('name')!r}, "
                    f"should match the directory name"
                )
            for key in ("description", "version"):
                if not meta.get(key):
                    problems.append(f"{skill.name}: frontmatter missing {key}")
        for section in SKILL_SECTIONS:
            if section not in body:
                problems.append(f"{skill.name}: missing section {section!r}")
    return problems


@check("automation catalog is valid")
def _automations():
    problems = []
    catalog = loads_subset((ROOT / "automations/catalog.yaml").read_text(encoding="utf-8"))
    items = catalog.get("automations") or []
    if not items:
        return ["catalog.yaml has no automations"]
    if catalog.get("defaults", {}).get("active") is not False:
        problems.append("defaults.active must be false")

    known_skills = {p.parent.name for p in SKILLS_DIR.rglob("SKILL.md")}
    seen = set()
    for item in items:
        ident = item.get("id", "<no id>")
        if ident in seen:
            problems.append(f"{ident}: duplicate id")
        seen.add(ident)
        for field in AUTOMATION_FIELDS:
            if item.get(field) in (None, ""):
                problems.append(f"{ident}: missing field {field!r}")
        if item.get("active") is True:
            problems.append(f"{ident}: active must be false in the catalog")
        if item.get("skill") not in known_skills:
            problems.append(f"{ident}: skill {item.get('skill')!r} does not exist")
        blob = f"{item.get('objective','')} {item.get('output','')}".lower()
        outward = any(word in blob for word in OUTWARD_KEYWORDS)
        if (outward or ident in CONTENT_PRODUCING) and not item.get("approval_required"):
            reason = ("produces publishable content" if ident in CONTENT_PRODUCING
                      else "description implies contacting someone")
            problems.append(f"{ident}: {reason} but approval_required is not true")
    return problems


@check("automation index matches the catalog")
def _index():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_automation_index.py"), "--check"],
        cwd=ROOT, capture_output=True, text=True,
    )
    return [] if result.returncode == 0 else [result.stdout.strip() or "index is stale"]


@check("config templates parse and have the expected shape")
def _configs():
    problems = []
    for name, keys in CONFIG_SHAPE.items():
        path = ROOT / name
        if not path.exists():
            problems.append(f"missing {name}")
            continue
        try:
            data = loads_subset(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{name}: does not parse — {exc}")
            continue
        for key in keys:
            if key not in (data or {}):
                problems.append(f"{name}: missing top-level key {key!r}")
    return problems


@check("hermes-home is in sync with agent/ templates")
def _hermes_home():
    if not (ROOT / "hermes-home").exists():
        return []  # not installed yet; that is fine
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/sync_agent.py"), "--check"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if result.returncode == 0:
        return []
    return ["hermes-home/ is stale — run: python3 scripts/sync_agent.py"]


@check("Hermes profile keys and toolset names are real")
def _hermes_profile():
    """Verify the profile against the installed Hermes, when one is present.

    A misspelled toolset name is silently ignored by Hermes rather than
    rejected, which would turn a safety setting into a no-op. This check makes
    that failure loud. It is skipped when Hermes is not installed yet.
    """
    venv = ROOT / "vendor/hermes-venv/bin/python"
    src = ROOT / "vendor/hermes-agent"
    if not venv.exists() or not src.exists():
        return []

    probe = (
        "import sys,json;"
        f"sys.path.insert(0,{str(src)!r});"
        "from hermes_cli.tools_config import CONFIGURABLE_TOOLSETS as C;"
        "print(json.dumps([k for k,_,_ in C]))"
    )
    result = subprocess.run([str(venv), "-c", probe], cwd=ROOT,
                            capture_output=True, text=True)
    if result.returncode != 0:
        return [f"could not query installed Hermes: {result.stderr.strip()[:200]}"]

    import json
    try:
        valid = set(json.loads(result.stdout.strip().splitlines()[-1]))
    except (ValueError, IndexError):
        return ["could not parse the toolset list from Hermes"]

    profile = loads_subset((ROOT / "agent/team-leader/config.example.yaml").read_text(encoding="utf-8"))
    disabled = ((profile or {}).get("agent") or {}).get("disabled_toolsets") or []
    problems = [f"disabled_toolsets: {name!r} is not a Hermes toolset"
                for name in disabled if name not in valid]

    # These are the settings that make the profile safe. If any is missing or
    # loosened in the template, say so.
    expected = {
        ("approvals", "mode"): "manual",
        ("approvals", "cron_mode"): "deny",
        ("security", "redact_secrets"): True,
        ("privacy", "redact_pii"): True,
    }
    for (section, key), want in expected.items():
        got = ((profile or {}).get(section) or {}).get(key)
        if got != want:
            problems.append(f"{section}.{key} is {got!r}, expected {want!r}")
    return problems


@check("document-type skill routing resolves")
def _skill_routing():
    """Every skill review.py routes to must actually exist.

    A dangling entry here means the pipeline tells the Team Leader to use a
    skill that is not installed — which looks like a working handoff and is not.
    """
    review = ROOT / "scripts" / "local_ai" / "review.py"
    if not review.exists():
        return ["scripts/local_ai/review.py is missing"]

    body = review.read_text(encoding="utf-8")
    start = body.find("SKILL_FOR_TYPE = {")
    if start < 0:
        return ["SKILL_FOR_TYPE not found in review.py"]
    block = body[start:body.index("}", start)]

    referenced = re.findall(r'"([a-z0-9-]+-review|[a-z0-9-]+-comparison)"', block)
    installed = {p.parent.name for p in SKILLS_DIR.rglob("SKILL.md")}
    problems = [f"review.py routes to {name!r} but no such skill exists"
                for name in sorted(set(referenced)) if name not in installed]

    # Schemas referenced for routing must exist too.
    schema_start = body.find("SCHEMA_FOR_TYPE = {")
    if schema_start >= 0:
        schema_block = body[schema_start:body.index("}", schema_start)]
        for schema in sorted(set(re.findall(r':\s*"([a-z_]+)"', schema_block))):
            if not (ROOT / "schemas" / f"{schema}.schema.json").exists():
                problems.append(f"review.py routes to schema {schema!r} which does not exist")
    return problems


@check("marketing archetypes are documented")
def _archetypes():
    """Every archetype used in config must exist in the knowledge file.

    Without this, someone can add an archetype to configuration that no skill
    knows how to coach, and the agent will silently fall back to generic advice.
    """
    config = ROOT / "config" / "marketing.example.yaml"
    profiles = ROOT / "knowledge" / "marketing" / "lo-marketing-profiles.md"
    if not config.exists() or not profiles.exists():
        return ["config/marketing.example.yaml or the profiles knowledge file is missing"]

    documented = set()
    for line in profiles.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("`archetype:") and line.endswith("`"):
            documented.add(line[len("`archetype:"):-1].strip())

    problems = []
    if not documented:
        return ["no `archetype: <slug>` markers found in lo-marketing-profiles.md"]

    data = loads_subset(config.read_text(encoding="utf-8")) or {}
    for officer in data.get("loan_officers") or []:
        archetype = officer.get("archetype")
        if archetype and archetype not in documented:
            problems.append(
                f"{officer.get('id')}: archetype {archetype!r} is not documented in "
                f"knowledge/marketing/lo-marketing-profiles.md"
            )

    # Content mixes must total 100 or the calendar maths is wrong.
    mixes = [("team", (data.get("team") or {}).get("content_mix"))]
    mixes += [(o.get("id"), o.get("content_mix")) for o in (data.get("loan_officers") or [])]
    for name, mix in mixes:
        if not mix:
            continue
        total = sum(v for v in mix.values() if isinstance(v, int))
        if total != 100:
            problems.append(f"{name}: content_mix totals {total}, should be 100")
    return problems


@check("no machine-specific paths in tracked files")
def _paths():
    problems = []
    allow = {"scripts/validate.py", "scripts/privacy_scan.py"}
    for path in text_files():
        rel = path.relative_to(ROOT).as_posix()
        if rel in allow:
            continue
        try:
            body = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for match in LEAKY_PATH.findall(body):
            problems.append(f"{rel}: contains machine path {match!r}")
    return problems


@check("relative documentation links resolve")
def _links():
    problems = []
    for path in tracked_files():
        if path.suffix != ".md":
            continue
        rel = path.relative_to(ROOT).as_posix()
        for target in LINK.findall(path.read_text(encoding="utf-8")):
            target = target.strip()
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                problems.append(f"{rel}: broken link -> {target}")
    return problems


@check("example data is labelled fictional")
def _examples():
    problems = []
    for name in ("config/team.example.yaml", "config/team-leader.example.yaml"):
        body = (ROOT / name).read_text(encoding="utf-8").lower()
        if "fictional" not in body:
            problems.append(f"{name}: no 'fictional' label")
    sample = ROOT / "examples"
    if sample.exists():
        for path in sample.rglob("*.md"):
            if "fictional" not in path.read_text(encoding="utf-8").lower():
                problems.append(f"{path.relative_to(ROOT)}: no 'fictional' label")
    return problems


# --------------------------------------------------------------------------

def main() -> int:
    print("Validating the Team Leader OS\n")
    failed = 0
    for ok, name, problems in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        if not ok:
            failed += 1
            for problem in problems[:12]:
                print(f"         - {problem}")
            if len(problems) > 12:
                print(f"         ... and {len(problems) - 12} more")
    total = len(results)
    print(f"\n{total - failed}/{total} checks passed")
    if failed:
        print("\nFix the items above, then run this again.")
        return 1
    print("Everything checks out.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
