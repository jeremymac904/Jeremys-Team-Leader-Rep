# Configuration

Five files. All are copied from `*.example.yaml` templates and are gitignored once filled in.

| File | What it controls |
|---|---|
| `config/team-leader.yaml` | You: identity, market, goals, KPIs, leadership style, schedule, permissions |
| `team-data/team.yaml` | Your roster, standards, recruiting pipeline — **private** |
| `config/coaching.yaml` | How you coach and when to escalate |
| `config/integrations.yaml` | What is connected |
| `config/local-ai.yaml` | Local models and privacy routing |

Create them all:
```bash
python3 scripts/setup.py
python3 scripts/setup.py --check     # what exists
```

## team-leader.yaml

**`identity`** — name, team, contact, NMLS, timezone, working hours.

**`market`** — states, primary market, `mortgage_specialties`. The specialties drive what
training and guideline research focus on.

**`goals`** — production goals including `personal_units_per_month` (your own production,
which the weekly review tracks separately because it is what quietly disappears), plus
recruiting and marketing goals.

**`goals.kpis`** — the handful of numbers you actually manage by. The agent ranks against
these instead of inventing a scoreboard. Keep it short.

**`leadership`** — `coaching_style`, `preferred_communication_style` (the agent matches
it), `team_culture`, `accountability_standards`, `escalation_preferences`. Escalation
preferences outrank everything else in the morning brief.

**`schedule`** — meetings, training, recurring responsibilities. Meeting durations are used
to time-box generated agendas.

**`permissions`** — three lists: `allowed_without_asking`, `never_without_approval`,
`never_at_all`. Read [automation-safety.md](automation-safety.md) before loosening these.

## team.yaml (private)

Per member: `experience_level` (`new` / `developing` / `established` / `top-producer`),
`tenure_months`, `goals`, `strengths`, `development_areas`.

**`experience_level` and `development_areas` do the most work.** They select the coaching
track and drive what the agent drills. Vague development areas produce vague coaching.

`standards` sets team-wide expectations — scorecard due time, minimum conversations,
borrower contact SLA. `recruiting_pipeline` holds candidates; keep real ones here only,
never in a tracked file.

## coaching.yaml

`one_on_one` — session structure and length.

`tracks` — per experience level: `emphasis`, `weekly_focus`, `role_play_minutes`, `tone`.
This is why a top producer gets coached on leverage rather than call volume.

`intervention_triggers` — condition and action pairs. When one fires, that conversation
comes before skill coaching.

`guardrails` — things the agent refuses, including promising income and writing HR
language.

## integrations.yaml

Each entry has `status: working` or `status: placeholder`. Only local files, pasting, and
local documents are `working` — see [integrations.md](integrations.md).

## local-ai.yaml

`privacy_mode.enabled` — on by default. `on_local_failure` is `stop_and_ask` or `stop`.

`routing` — the four categories. `hybrid` is off and its `require_approval` cannot be
disabled.

`engine` — host, ports, `gpu_layers` (lower it if you run out of memory), threads.

`models` — `tier: auto` uses hardware detection. Override only if you know better.

`documents` — inbox path, OCR settings, `render_dpi`, `max_pages_per_document`.

See [local-ai/privacy-mode.md](local-ai/privacy-mode.md).

## After editing

```bash
python3 scripts/validate.py
python3 scripts/sync_agent.py    # only if you changed the Hermes profile template
```

## Where things do not go

Never put a real roster, borrower data, or an API key in a `config/*.example.yaml` file.
Those are committed. Real values go in the gitignored `config/*.yaml`, `team-data/`, and
`.env`.
