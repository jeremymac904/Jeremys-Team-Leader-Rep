# Contributing

Improvements to skills, automations, coaching frameworks, prompts, and documentation are
welcome.

## The one absolute rule

**Never contribute anything containing real borrower, employee, or candidate information.**
Use the fictional Northstar Lending Team. Every example must be invented.

```bash
python3 scripts/privacy_scan.py
```

## Setup

```bash
git clone <your fork>
cd Jeremys-Team-Leader-Rep
bash scripts/install_hermes.sh
python3 scripts/setup.py --demo     # fictional team, no questions
./vendor/hermes-venv/bin/python tests/run_tests.py
```

## Before opening a pull request

```bash
python3 scripts/validate.py
python3 scripts/privacy_scan.py
./vendor/hermes-venv/bin/python tests/run_tests.py
```

All three must pass.

## Adding a skill

```bash
mkdir -p skills/team-leadership/tl-my-skill
cp skills/team-leadership/tl-morning-brief/SKILL.md skills/team-leadership/tl-my-skill/SKILL.md
```

Every skill needs: `## Purpose`, `## When Hermes should use it`, `## Required information`,
`## Tools and commands it may use`, `## Workflow`, `## Expected output`,
`## Safety boundaries`, `## Human approval requirements`, `## Related skills`,
`## What this skill must not assume`, `## Tests`. The frontmatter `name` must match the
directory name. The test suite checks all of this.

Mortgage document skills additionally must state that the agent is not the underwriter and
must distinguish extracted fact / potential issue / underwriting consideration /
recommended verification.

## Adding an automation

Add a card to `automations/catalog.yaml` following `automations/schema.md`, then:

```bash
python3 scripts/build_automation_index.py
```

`active` must be `false`. Anything with an outward effect must set
`approval_required: true`.

## Adding a model

Add it to `local-ai/models.manifest.yaml`. Verify the Hugging Face repository and filenames
actually exist, check the license permits commercial use, record `date_reviewed`, and mark
it `experimental` until tested. Update `local-ai/VALIDATION.md` when you test it.

## Style

- Plain language. The reader is a mortgage professional, not an engineer.
- Explain jargon on first use.
- Never claim a capability that does not exist. If it is untested, say so.
- Keep documentation and implementation in step — the test suite enforces parts of this.
