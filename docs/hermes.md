# How Hermes and this package fit together

## The short version

**Hermes is the program. This repository is the customization.**

You install Hermes the normal, official way. You download this folder. You run
Hermes from inside the folder. Hermes finds the Team Leader skills and uses them.

Nothing is copied, bundled, or built. There is no custom application.

## What Hermes is

[Hermes Agent](https://github.com/NousResearch/hermes-agent) is an open-source AI
agent from Nous Research (MIT licensed) that runs on your own computer. It can
drive different AI models — cloud models like Claude or GPT, or a local model.

Install it the official way:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes setup
```

`hermes setup` walks you through choosing an AI provider. Use whichever you
already have. This package does not require or prefer any particular one.

## How Hermes finds the Team Leader skills

`python3 scripts/setup.py` registers this repository's `.hermes/skills/`
directory in `skills.external_dirs` in your Hermes config. That is Hermes's
supported mechanism for loading skills from outside its own home, and it is
**global** — every session sees them, from any directory, in Desktop and CLI.

Run it directly any time:

```bash
python3 scripts/install_global_skills.py          # register
python3 scripts/install_global_skills.py --check  # verify
```

The installer:

- preserves every other setting in your Hermes config, and backs it up first
- skips the entry if it is already present, so it is safe to re-run
- verifies the skills are visible **from outside the repo**

Because nothing is copied, `git pull` updates your skills immediately.

Previously this package used project-local skills, which only loaded when
Hermes started inside the folder. Running setup migrates you to global loading.
The old `hermes skills trust` entry is harmless and can stay.

## How Hermes knows how to behave

Two files at the root of this package:

| File | What it does |
|---|---|
| [`AGENTS.md`](../AGENTS.md) | The agent's operating instructions. Hermes automatically reads a project-root `AGENTS.md` as context. |
| `config/*.yaml` + `team-data/team.yaml` | Your identity, team, goals, and coaching style — created by `scripts/setup.py` and gitignored |

`AGENTS.md` is plain English. If you want the agent to behave differently — a
different tone, an extra rule, a boundary — edit that file. No code involved.

## Your configuration stays yours

| Gitignored (private) | Committed (public) |
|---|---|
| `config/*.yaml` | `config/*.example.yaml` |
| `team-data/` | The skills, frameworks, and templates |
| `local_data/` | Fictional sample data |

A `git pull` never overwrites your configuration.

To customize a skill that ships here without fighting future updates, copy it
into your own Hermes profile skills directory under the same name — profile
skills are yours and are never touched by a `git pull`.

## Other AI tools

`AGENTS.md` and the skills are plain Markdown. Claude Code, Codex, and similar
assistants read them as context. Point them at
[`PROJECT_STATUS.md`](../PROJECT_STATUS.md) for the architecture and what is
tested.

## Optional: running a model locally

Separate and not required for anything above.

**The local model is for document review, not for chatting with Hermes.** Keep a
normal cloud provider for conversation.

**Hermes enforces a 64,000-token minimum context window for its chat model.**
Point it at a smaller one and it refuses outright:

```
Model local-model has a context window of 32,768 tokens, which is below the
minimum 64,000 required by Hermes Agent.
```

The local tiers in this package run at 8K–32K on purpose, to leave memory for
the operating system and document extraction. Raising a local model to 64K to
satisfy Hermes was tested on a 24 GB machine and failed: the model loaded at
13.1 GB but inference returned a compute error.

That is fine, because it is not what the local model is for. Reading one
document needs a few thousand tokens of context. Driving an extended tool-using
conversation needs far more.

So the two run side by side:

| Workflow | Model |
|---|---|
| Talking to your Team Leader Agent | Your normal cloud provider |
| Reviewing a borrower document | The local model on `127.0.0.1` |

Local Privacy Mode enforces the second: borrower documents are routed to the
local endpoint and refuse a cloud one. See
[local-ai/privacy-mode.md](local-ai/privacy-mode.md).

## For maintainers: isolated testing

`scripts/install_hermes.sh` and `scripts/hermes.sh` install a **separate** copy
of Hermes inside `vendor/` with its own `HERMES_HOME`, for testing this package
without touching a real Hermes installation.

**Team Leaders do not need these.** Use the official installer above.
