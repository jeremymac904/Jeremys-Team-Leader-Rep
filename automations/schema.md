# Automation card schema

Every automation in [`catalog.yaml`](catalog.yaml) is a **card** with the same fields.
The schema exists so that automations are comparable, reviewable, and safe by default —
and so `scripts/validate.py` can check them mechanically.

## Required fields

| Field | What it means |
|---|---|
| `id` | Unique slug, lowercase with hyphens. Never reused. |
| `name` | Human-readable name. |
| `category` | One of: `daily-leadership`, `pipeline`, `coaching`, `meetings`, `recruiting`, `partners`, `training`, `marketing`, `executive`, `ai-workflows`. |
| `objective` | The business outcome in one sentence. Not the mechanic — the outcome. |
| `trigger` | When it runs: a cron expression, a cadence, or an event. |
| `cadence` | Plain-English version of the trigger, for humans. |
| `data_needed` | Exactly what inputs it requires. If you cannot supply these, it cannot run. |
| `skill` | Which skill in `agent/skills/` does the work. |
| `prompt` | The suggested prompt. Copy-pasteable. |
| `output` | What it produces. |
| `approval_required` | `true` or `false`. **Anything with an outward effect must be `true`.** |
| `privacy` | What sensitive data it touches and how that constrains it. |
| `setup` | What you must do before it can run. |
| `customization` | The knobs worth turning. |
| `active` | **Always `false` in this catalog.** You activate it deliberately. |
| `failure_behavior` | What happens when it fails. Must fail closed. |
| `stale_data_behavior` | What it does when the input is old or missing. Must never fill gaps by inventing. |
| `stop_control` | How to turn it off. |
| `time_saved_per_month` | Honest estimate, with the arithmetic. |

## Rules the schema enforces

1. **`active: false` always.** The catalog ships inactive. Nothing here runs until you turn
   it on. This is not a formality — it is the difference between a library and a loaded gun.

2. **Outward effects require approval.** If an automation could send a message, change a
   record, publish content, or spend money, `approval_required` must be `true`. The pattern
   is always:

   > agent prepares → you review → you approve → the system executes

3. **Fail closed.** On error, produce nothing and log locally. Never retry an external
   action. Never partially send.

4. **Never invent.** If the data is stale or missing, say so and omit the conclusion. An
   automation that quietly guesses is worse than one that fails.

5. **Privacy is a declared field, not an afterthought.** If it touches borrower, employee,
   or candidate information, that is stated, and the output stays in `team-data/`.

## Adding your own

Copy an existing card, change the `id`, fill every field, keep `active: false`, then:

```bash
python3 scripts/validate.py
```

Validation fails if a field is missing, if `active` is `true`, or if an outward-effect
category is missing `approval_required: true`. Then add a row for it in
[`README.md`](README.md) — validation checks that too, so the docs cannot drift.
