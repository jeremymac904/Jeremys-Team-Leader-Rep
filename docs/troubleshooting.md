# Troubleshooting

## Setup

**`python3: command not found`**
Install Python 3.11+ from [python.org](https://www.python.org/downloads/). On macOS,
`brew install python@3.12` also works. Some systems use `python` — try `python --version`.

**`bash scripts/install_hermes.sh` fails on git**
macOS: `xcode-select --install`. Windows: install Git for Windows.

**The Hermes install fails partway**
Safe to re-run — it updates an existing clone instead of starting over. If a dependency
failed, the script retries with a base install automatically. Check the output for the real
error.

**`python3 scripts/validate.py` reports missing files**
Run `python3 scripts/setup.py` first. Files listed as missing are the ones setup creates.

## The agent

**It says my configuration is missing**
```bash
python3 scripts/setup.py --check
```
Anything MISSING is created by `python3 scripts/setup.py`.

**It does not know my team**
Your roster lives in `team-data/team.yaml`, not in `config/`. Open it and replace the
fictional Northstar team.

**It uses the fictional team instead of mine**
That happens when `team-data/team.yaml` does not exist — it falls back to the example and
should say so. Create the real file.

**My skills are not showing up**
```bash
bash scripts/hermes.sh skills list
```
Expect 35. If zero, the profile is not pointed at the repository:
```bash
python3 scripts/sync_agent.py
grep -A3 "external_dirs" hermes-home/config.yaml
```

**I edited a skill and nothing changed**
Skills are read fresh each run — just restart the agent. Only `SOUL.template.md` and
`config.example.yaml` need `sync_agent.py`.

**It invented numbers**
Report it — that is a bug. The skills instruct it to state what data it lacks. It is most
likely to happen if you asked for a review without supplying data.

**It claims it can read my email**
Also a bug. Nothing here connects to Gmail. See [integrations.md](integrations.md).

## Hermes

**It is using my other Hermes setup**
It is not — `scripts/hermes.sh` sets `HERMES_HOME` to this repository's `hermes-home/`.
Confirm:
```bash
bash scripts/hermes.sh --version
```
Always launch through `scripts/hermes.sh`, not a global `hermes` command.

**Did this change my existing Hermes?**
No. The clone in `vendor/` and the home in `hermes-home/` are separate from `~/.hermes`.

**No model configured**
```bash
bash scripts/hermes.sh setup
```

**`No module named pymupdf` during local document review**
```bash
./vendor/hermes-venv/bin/python -m pip install -r requirements-local-ai.txt
```

## Validation

**`validate.py` fails on broken links**
A Markdown link points at a file that does not exist. The message names the file and the
target.

**`validate.py` fails on machine-specific paths**
A tracked file contains an absolute home or volume path. Replace it with `${REPO_PATH}` or a
relative path — those paths leak your local layout into a public repository.

**`privacy_scan.py` reports warnings**
Warnings are usually intentional examples. Read each one. Only BLOCK findings stop a commit.

**The automation index is out of date**
```bash
python3 scripts/build_automation_index.py
```

## Local AI

See [local-ai/troubleshooting.md](local-ai/troubleshooting.md).

## Still stuck

```bash
python3 scripts/validate.py
python3 scripts/setup.py --check
bash scripts/install_hermes.sh --check
./vendor/hermes-venv/bin/python tests/run_tests.py
```

Include that output when asking for help.
