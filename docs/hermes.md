# Hermes and this repository

## What Hermes is

[Hermes Agent](https://github.com/NousResearch/hermes-agent) is an open-source AI agent
from Nous Research (MIT licensed) that runs on your own computer. It can drive different
AI models — cloud models like Claude or GPT, or a local model on your machine.

This repository does not replace or fork Hermes. It **configures** it.

## The isolated install

```bash
bash scripts/install_hermes.sh
```

This pulls a fresh Hermes clone into `vendor/hermes-agent/` with its own Python
environment in `vendor/hermes-venv/`. Both are gitignored.

**If you already run Hermes, it is not touched.** Isolation comes from `HERMES_HOME`,
which Hermes reads as the single source of truth for its home directory.
`scripts/hermes.sh` sets it to this repository's `hermes-home/` on every run, so this
agent's config, identity, skills, and session history are entirely separate from
`~/.hermes`.

```
vendor/hermes-agent/   fresh upstream clone
vendor/hermes-venv/    its own Python environment
hermes-home/           this repository's HERMES_HOME
```

## How the agent is assembled

| Piece | File | How Hermes finds it |
|---|---|---|
| Identity | `hermes-home/SOUL.md` | Hermes reads `$HERMES_HOME/SOUL.md` into the system prompt |
| Instructions | `AGENTS.md` at the repo root | Hermes auto-injects a project-root `AGENTS.md` |
| Skills | `skills/` | `skills.external_dirs` in the profile |
| Settings | `hermes-home/config.yaml` | Hermes reads `$HERMES_HOME/config.yaml` |

`SOUL.md` and `config.yaml` are generated from templates in `agent/team-leader/`:

```bash
python3 scripts/sync_agent.py
```

Re-run that after editing the SOUL template or the profile. **Editing a skill needs no
sync** — skills are read in place.

## Skills load from the repository

`skills.external_dirs` is Hermes's supported mechanism for reading skills from outside
`~/.hermes/skills/`. The profile points it at this repository's `skills/` folder:

```yaml
skills:
  external_dirs:
    - "/path/to/Jeremys-Team-Leader-Rep/skills"
```

This means:

- `git pull` updates your skills immediately — nothing to copy
- Editing a `SKILL.md` takes effect on the next run
- External directories are **read-only** to Hermes: when the agent creates a skill of its
  own it writes to `hermes-home/skills/`, never back into your git repository
- If a name collides, your local skill wins over the repository one

Confirm they loaded:
```bash
bash scripts/hermes.sh skills list
```

Skills are organized by directory, and the directory becomes the category:
`skills/team-leadership/` and `skills/mortgage-documents/`.

## Preserving your customizations

Your configuration lives in gitignored files, so `git pull` never overwrites it:

- `config/*.yaml`, `team-data/`, `hermes-home/config.yaml`

To customize a skill that ships here, either edit it directly — and accept that a pull may
conflict — or copy it to `hermes-home/skills/` under the same name, where it takes
precedence and is never touched by a pull.

## The safety profile

| Setting | Value | Effect |
|---|---|---|
| `approvals.mode` | `manual` | Every action-taking tool call is confirmed by you |
| `approvals.cron_mode` | `deny` | The agent cannot create or activate schedules |
| `security.redact_secrets` | `true` | Secrets are stripped from model context |
| `privacy.redact_pii` | `true` | User IDs hashed, phone numbers stripped |
| `agent.disabled_toolsets` | terminal, browser, code_execution, discord, discord_admin, cronjob, computer_use | No shell, no browsing, no messaging |
| `mcp_servers` | `{}` | No external connectors — honest, because none ship |

`file` and `skills` stay enabled so the agent can read your configuration and use its
skills.

`scripts/validate.py` checks these values against the installed Hermes and fails on a
typo — a misspelled toolset name is silently ignored by Hermes, which would turn a safety
setting into a no-op.

## Using a local model

```bash
python3 scripts/local_ai/server.py hermes-config
```

Prints the exact settings. Local inference uses the supported `custom` provider pointed at
`127.0.0.1`. See [local-ai/](local-ai/README.md).

## Other AI tools

`AGENTS.md` is a plain Markdown instruction file, and the skills are plain Markdown too.
Claude Code, Codex, and other assistants read them as context. Point them at
`PROJECT_STATUS.md` to pick up the architecture and what is tested.
