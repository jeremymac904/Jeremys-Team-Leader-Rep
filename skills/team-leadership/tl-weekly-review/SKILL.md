---
name: tl-weekly-review
description: "Run the Team Leader's own weekly review: team trends, personal capacity, delegation, and next week's plan."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [team-leader, executive, weekly, planning]
---

# Weekly Team Leader Review

## Purpose
The review the leader runs on themselves. Most Team Leaders review everyone else and never
look at their own week — which is why they stay buried. This covers team trends, the
leader's own production, where their time actually went, and what to hand off.

## When Hermes should use it
Use at the end of the working week, or when the Team Leader wants to step back.
## Required information
- This week's scorecards and pipeline review output
- The leader's own production numbers
- `personal_units_per_month` from `production_goals`
- `recurring_responsibilities` and `working_hours`
- What the leader says they spent time on

## Tools and commands it may use
Reading configuration and provided data. Analysis and drafting only.

## Safety boundaries
Read-only.

## Human approval requirements
None.

## Workflow
1. Team trend: compare this week to the prior 2–3 weeks. Direction matters more than level.
2. Individual movement: who improved, who slipped, who went quiet. One line each.
3. **Leader's own production** against `personal_units_per_month`. This gets its own section
   because it is the number that silently disappears.
4. Time audit: where the week actually went versus where it should have gone.
5. Delegation candidates: name specific tasks and specific people.
6. Automation candidates: anything done three or more times this week. Hand off to
   `tl-automation-advisor`.
7. Next week: three priorities, no more.

## Evidence rules
Trends cite at least two prior periods. A single week is noise, not a trend, and should be
labeled as such.

## Expected output
```
WEEKLY REVIEW — week of <date>

TEAM TREND
<metric>: <this week> vs <last> vs <prior>  →  <direction>

MOVEMENT
Up:    <person> — <what changed>
Down:  <person> — <what changed>
Quiet: <person> — <how long>

YOUR OWN PRODUCTION
<actual vs personal goal>  —  <on track / slipping>
<if slipping: what leadership work displaced it>

WHERE THE WEEK WENT
<estimate vs intended>

HAND OFF
- <task> → <person> — <why they can own it>

AUTOMATE
- <task done 3+ times> → see tl-automation-advisor

NEXT WEEK — THREE PRIORITIES
1. ...
```

## Stop conditions
None specific. Stay read-only.

## Error behavior
With only one week of data, report the level and state explicitly that no trend can be
read yet.

## Related skills
- `tl-morning-brief` — the daily version
- `tl-monthly-review` — the longer arc
- `tl-automation-advisor` — for the repetitive work it surfaces

## What this skill must not assume
- **Do not assume one week is a trend.**
- **Do not assume the leader's time estimate is accurate.**
- **Do not assume delegation capacity exists** — check who is already loaded.
- **Do not assume the leader's own production is fine** because the team's is.

## Tests
- Always includes the leader's own production section.
- Trend claims cite 2+ prior periods.
- Never more than three next-week priorities.
