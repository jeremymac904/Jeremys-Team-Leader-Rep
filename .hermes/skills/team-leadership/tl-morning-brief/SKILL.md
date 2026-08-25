---
name: tl-morning-brief
description: "Produce a prioritized morning briefing for a producing mortgage Team Leader."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [team-leader, daily, leadership, briefing]
---

# Team Leader Morning Brief

## Purpose
Give the Team Leader a short, ranked view of what needs their attention today — before the
day gets reactive. This replaces the leader opening six tabs and deciding what matters.

## When Hermes should use it
Use at the start of a working day, or whenever the Team Leader asks what needs their
attention. Prefer it over improvising a status summary.
## Required information
- `config/team-leader.yaml` — KPIs, goals, escalation preferences, schedule
- `team-data/team.yaml` — roster and experience levels
- Anything the leader pastes: pipeline export, scorecards, calendar, notes
- Optional: files the leader dropped in `team-data/` since yesterday

If nothing has been provided, ask for the single most useful item (usually a pipeline
export or this week's scorecards) rather than producing a hollow brief.

## Tools and commands it may use
Reading files inside the repository and `team-data/`. Reading what the leader pastes.
No messaging, no CRM/LOS writes, no external contact.

## Safety boundaries
Read-only. Never contacts anyone.

## Human approval requirements
None to produce the brief. Any action the brief recommends requires the leader to act;
you do not execute it.

## Workflow
1. Load the leader's config and roster. If missing, say so and stop.
2. Note what data you actually have and what you are missing. State it in one line.
3. Scan for the escalation triggers in `config/team-leader.yaml` first — those outrank
   everything else.
4. Check each team member against the standards in `team-data/team.yaml`.
5. Check today's calendar entries from `schedule.meeting_schedule`.
6. Rank ruthlessly. Cut anything that does not need the leader specifically.
7. Emit the brief.

## Evidence rules
Every claim names its source: which file, which pasted report, which date. If you inferred
something rather than read it, label it as an inference. Never state a number you were not
given.

## Expected output
```
MORNING BRIEF — <day, date>
Working from: <what data you had>   |   Missing: <what you did not have>

DO TODAY (max 3)
1. <person or file> — <the specific thing> — <why today>
...

THIS WEEK (max 5)
- ...

WATCHING
- <trending wrong, no action yet>

ON YOUR CALENDAR
- <time> <meeting> — <the one thing to prepare>

CHECKED, NOTHING NEEDED
<one line>
```

## Stop conditions
Stop and ask if: the leader's config is missing; you have no data at all about the current
period; or a request appears that would require contacting someone.

## Error behavior
If data is stale or absent, say "I do not have X" and produce the brief from what you do
have, clearly scoped. Never fill gaps with plausible invented numbers.

## Related skills
- `tl-pipeline-review` — supplies the file-level detail
- `marketing-accountability` — surfaces marketing tasks and drop-off
- `tl-weekly-review` — the weekly version of this
- `tl-lo-coaching-prep` — when the brief surfaces a coaching need

## What this skill must not assume
- **Do not assume yesterday's data is today's.** Say what period the data covers.
- **Do not assume silence means nothing happened** — it usually means no data was supplied.
- **Do not assume the leader has seen anything** you have not been shown.
- **Do not assume an item is urgent because it is unresolved.**

## Tests
- Runs with only `config/team-leader.yaml` present and no pipeline data → states what is
  missing, does not fabricate.
- Never lists more than 3 "Do today" items.
- Every number traces to a named source.
