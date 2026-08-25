# The Team Leader Agent

This directory is the agent itself.

| File | What it is |
|---|---|
| `AGENTS.md` | The agent's operating instructions — identity, how it answers, coaching behavior, hard boundaries. **This is the file to edit if you want the agent to behave differently.** |
| `config.example.yaml` | The Hermes profile template. Copy to `config.yaml` (gitignored) and fill in your path, or run `python3 scripts/setup.py`. |

Its capabilities live one level up in [`../../.hermes/skills/`](../../.hermes/skills/) as Hermes skills.

## Making it yours

Three levers, in the order most people should use them:

1. **Configuration** — `config/team-leader.yaml`, `team-data/team.yaml`,
   `config/coaching.yaml`. Covers identity, goals, KPIs, roster, coaching style,
   permissions. Most customization should happen here.
2. **Instructions** — edit `AGENTS.md`. Change tone, add a rule, add a boundary.
   Plain English; no code.
3. **Skills** — add a directory under `../skills/` with a `SKILL.md`. See
   [`../../.hermes/skills/README.md`](../../.hermes/skills/README.md).

## Running it

See [`../../docs/hermes.md`](../../docs/hermes.md). Short version: this profile is
designed for the Hermes Agent runtime, and the same `AGENTS.md` + skills also work
as context for Claude Code, Codex, or another coding assistant if you are not
running Hermes.
