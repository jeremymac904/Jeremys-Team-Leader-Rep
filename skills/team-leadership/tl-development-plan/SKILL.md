---
name: tl-development-plan
description: "Build a 30/60/90-day development plan for a Loan Officer, matched to their level and the specific gap."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [team-leader, coaching, development, planning]
---

# Loan Officer Development Plan

## Purpose
Produce a written development plan a Loan Officer can actually execute — new-hire ramp,
improvement plan for someone stalling, or growth plan for a producer hitting a ceiling.

## When Hermes should use it
Use when onboarding a new LO, when an intervention trigger fires, or when a capable
producer has plateaued.
## Required information
- The LO's roster entry (experience level, tenure, goals, strengths, development areas)
- `config/coaching.yaml` tracks and intervention triggers
- Recent production and activity numbers
- The leader's `production_goals` and `kpis`

## Tools and commands it may use
Reading configuration, roster, and provided numbers. Drafting the plan document.

## Safety boundaries
The finished plan concerns a named employee. It is saved to `team-data/`, never committed.

## Human approval requirements
None to draft. The leader reviews, edits, and delivers it. You never deliver it.

## Workflow
1. Identify which of the three plan types this is: **ramp** (new), **recovery**
   (below standard), or **growth** (capable, plateaued). They are structured differently.
2. Name the gap in one sentence, with the number that proves it.
3. Set the 30/60/90 targets. Make them activity-based early and outcome-based later —
   an LO controls conversations, not closings.
4. For each phase, specify: the daily behavior, the weekly number, the skill being built,
   and the checkpoint.
5. Define what support the *leader* owes — plans fail when only one side has commitments.
6. State what "back on track" looks like, concretely.
7. Emit the plan.

## Evidence rules
Every target traces to either the team standard in `team-data/team.yaml` or the leader's
`production_goals`. Do not invent industry benchmarks.

## Expected output
```
DEVELOPMENT PLAN — <LO name>
Type: <ramp | recovery | growth>   Prepared: <date>   Review dates: <30/60/90>

THE GAP
<one sentence + the number>

DAYS 1-30 — <phase name>
  Daily behavior: ...
  Weekly number: ...
  Skill focus: ...
  Checkpoint (date): ...

DAYS 31-60 — <phase name>
  ...

DAYS 61-90 — <phase name>
  ...

WHAT I OWE YOU
- <leader's commitments: coaching time, leads, introductions, training>

WHAT "ON TRACK" MEANS
<the concrete standard>

NOT A PROMISE
This plan sets activity and skill targets. It does not promise income, a closing
count, or any business result.
```

## Stop conditions
Stop if the plan is being used as documentation for termination or formal discipline.
That is an HR document and needs a human and probably counsel. Say so.

## Error behavior
If you lack the LO's current numbers, build the structure and mark each target
`<needs current baseline>` rather than guessing.

## Related skills
- `tl-lo-coaching-prep` — the weekly execution of the plan
- `tl-recruiting-review` — onboarding plans for new hires

## What this skill must not assume
- **Do not assume a plan fixes a motivation problem.**
- **Do not assume the leader can deliver unlimited support** — ask what they can commit.
- **Do not assume 30/60/90 fits every case.** Some need 2 weeks, some 6 months.
- **Do not assume this is a performance-management document** unless told, and if it is, stop.

## Tests
- Plan type changes the structure, not just the wording.
- Contains leader-side commitments.
- Contains the "not a promise" label.
- Refuses termination documentation.
