---
name: tl-lo-coaching-prep
description: "Prepare a one-on-one coaching session for a specific Loan Officer, adapted to their experience level."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [team-leader, coaching, one-on-one, weekly]
---

# Loan Officer Coaching Prep

## Purpose
Turn a scheduled 30-minute one-on-one into a prepared, specific session — so the leader
walks in knowing the number, the diagnosis, the skill to drill, and the one commitment
to close on.

## When Hermes should use it
Use before a scheduled one-on-one, or when the Team Leader asks how to coach a specific
person. Always prefer this over generic coaching advice.
## Required information
- The Loan Officer's entry in `team-data/team.yaml` (experience level, goals, strengths,
  development areas)
- `config/coaching.yaml` — session structure, track emphasis, intervention triggers
- Their recent scorecard(s) — pasted or in `team-data/`
- Notes from the previous session, if any

## Tools and commands it may use
Reading configuration, roster, and provided scorecards. No contact with the LO.

## Safety boundaries
Coaching notes are private employee information. They belong in `team-data/`, never in a
tracked file.

## Human approval requirements
None to prepare. The leader runs the session.

## Workflow
1. Look up the LO's `experience_level` and load the matching track from `config/coaching.yaml`.
2. **Diagnose before prescribing.** Walk the funnel and find the first stage that breaks:
   conversations → appointments set → appointments held → applications → closings.
   Low output at the end of a healthy funnel is a different problem than a dry top.
3. Check `intervention_triggers`. If one has fired, that conversation comes first and
   skill coaching waits.
4. Pick **one** skill to drill live, chosen from their development areas and the broken
   funnel stage — not from a general list of good habits.
5. Draft 3–5 questions the leader can ask that make the LO reach the diagnosis themselves.
6. Prepare the commitment: one number, one focus, one next step.
7. Emit the prep sheet.

## Evidence rules
The diagnosis cites the actual ratio. "96 conversations → 1 appointment" is the evidence.
Never assert a cause you cannot show in the numbers; offer it as a hypothesis to test in
the room.

## Expected output
```
COACHING PREP — <LO name> — <date>
Track: <experience level> | Emphasis: <track emphasis>

THE NUMBER
<goal vs actual, and the ratio that matters most this week>

DIAGNOSIS
<which funnel stage is actually broken, with the ratio as evidence>
<what this is NOT — rule out the wrong fix>

TRIGGER CHECK
<any intervention trigger that has fired, or "none">

QUESTIONS TO ASK
1. ...

DRILL THIS (<N> minutes)
<the one script or behavior, and the exact scenario to role-play>

CLOSE WITH
One number: ... | One focus: ... | One next step: ...

FOLLOW-UP FROM LAST TIME
<what they committed to, and whether it happened>
```

## Stop conditions
Stop and hand to a human if the session topic becomes disciplinary, compensation, a
protected-class matter, termination, or anything an HR professional should own. Say so
plainly and do not draft it.

## Error behavior
With no scorecard, produce the structure and say which numbers the leader needs to bring.
Do not invent performance data about a real person.

## Related skills
- `tl-development-plan` — when a trigger has fired
- `tl-role-play` — for the live drill
- `tl-weekly-review` — surfaces who needs coaching

## What this skill must not assume
- **Do not assume the numbers explain the behavior.** Ask before concluding.
- **Do not assume a drop is a performance problem** — it is often a life event.
- **Do not assume last session's commitment was kept** unless told.
- **Do not assume the leader wants a script.** They want a diagnosis.

## Tests
- Adapts emphasis by experience level (a top-producer prep is about leverage, not activity).
- Refuses HR/disciplinary drafting.
- Diagnosis always cites a ratio.
- Ends with exactly one number, one focus, one next step.
