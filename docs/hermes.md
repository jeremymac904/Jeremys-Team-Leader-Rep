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

Hermes has a built-in feature for exactly this: **project-local skills**.

When you start Hermes from inside a Git repository, it looks for skills in
`.hermes/skills/` at the repository root. This package puts its 35 skills
there.

For safety, Hermes will not load skills from a folder you have not approved.
The first time, it tells you:

```
◆ 35 project skill(s) found in <folder> but not loaded —
  run `hermes skills trust` to enable them.
```

So you approve it once:

```bash
cd ~/Documents/Jeremys-Team-Leader-Rep
hermes skills trust
```

```
Trusted: <your home>/Documents/Jeremys-Team-Leader-Rep
35 project skill(s) will load in sessions started inside this repo
```

That is the entire integration. Because Hermes reads the folder directly:

- A `git pull` updates your skills immediately — nothing to reinstall
- Editing a skill takes effect the next time you start Hermes
- Project skills take precedence over same-named skills in your own profile
- Your other Hermes projects are unaffected

## Why you must start Hermes from inside the folder

Project-local skills are resolved from your **current directory**. Starting
Hermes somewhere else means it is not in this project, so the Team Leader skills
do not load.

```bash
cd ~/Documents/Jeremys-Team-Leader-Rep   # ← this matters
hermes
```

If you see 0 project skills, this is almost always why.

Check any time:

```bash
hermes skills list
```

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

Separate and not required. See [local-ai/](local-ai/README.md).

## For maintainers: isolated testing

`scripts/install_hermes.sh` and `scripts/hermes.sh` install a **separate** copy
of Hermes inside `vendor/` with its own `HERMES_HOME`, for testing this package
without touching a real Hermes installation.

**Team Leaders do not need these.** Use the official installer above.
