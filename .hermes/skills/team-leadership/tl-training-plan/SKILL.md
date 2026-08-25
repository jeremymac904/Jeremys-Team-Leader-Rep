---
name: tl-training-plan
description: "Choose the team's next training topics from actual performance gaps and build the session."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [team-leader, training, enablement, planning]
---

# Team Training Plan

## Purpose
Pick training topics from evidence rather than from a content calendar, and turn the topic
into a session the leader can actually run in 20–30 minutes.

## When Hermes should use it
Use when choosing what to train the team on next, or when building a session.
## Required information
- Roster development areas across the whole team
- Recent scorecards or pipeline patterns
- `training_schedule` from `config/team-leader.yaml`
- `mortgage_specialties` — the products this team actually sells

## Tools and commands it may use
Reading configuration and provided data. Drafting session material. Public research on
products, programs, and guidelines — cited with source and date.

## Safety boundaries
Team-level patterns only. Do not build a session that is visibly aimed at one person.

## Human approval requirements
None to build. Delivering it is the leader's job.

## Workflow
1. Find the shared gap. Count how many LOs list the same development area or show the same
   broken funnel stage. Two or more makes it a team topic; one makes it a one-on-one.
2. Rank candidate topics by how much production the gap is costing, not by how interesting
   they are.
3. Build the session with more drilling than lecturing: aim for at most one-third teach,
   at least one-third live rep, and a takeaway.
4. For any guideline or product content, cite the authoritative source and the date, and
   add a verification note. Do not recite guidelines from memory as current fact.
5. Produce a takeaway artifact — a one-page cheat sheet or script card.
6. Propose the next 4 sessions so the schedule stops being decided the night before.

## Evidence rules
Topic selection shows its work: "4 of 5 LOs list objection handling; team appointment-set
rate is 8%." Guideline content is sourced and dated, and labeled as education requiring
verification.

## Expected output
```
TRAINING PLAN — <date>

TOPIC SELECTED: <topic>
Evidence: <the counted gap and the number it is costing>
Rejected: <topic> — <why it ranked lower>

SESSION (<N> minutes)
  Teach (<N>m):  <the 2-3 points, nothing more>
  Drill (<N>m):  <the live rep, the exact scenario>
  Takeaway:      <the one-page artifact>

TAKEAWAY ARTIFACT
<the actual cheat sheet or script card>

GUIDELINE CONTENT   [EDUCATION]
Source: <name> | Retrieved: <date>
⚠ Verify against the current source before relying on this operationally.

NEXT FOUR SESSIONS
1. <topic> — <the gap it addresses>
```

## Stop conditions
Stop if asked to state a current agency guideline as settled fact without a source, or to
build training that instructs LOs to make eligibility or pricing representations.

## Error behavior
If no shared gap exists in the data, say so and recommend a one-on-one instead of inventing
a team topic.

## Related skills
- `tl-team-meeting-prep` — where the session is delivered
- `tl-guideline-research` — for sourced product content
- `tl-role-play` — the drill inside the session

## What this skill must not assume
- **Do not assume a shared development area means a shared root cause.**
- **Do not assume guideline knowledge is current** without a dated source.
- **Do not assume more training fixes an activity problem.**
- **Do not assume one session changes behavior.**

## Tests
- Topic selection cites a counted gap.
- Drill time is at least as long as teach time.
- Guideline content always carries source, date, and a verification warning.
- Recommends a one-on-one when the gap is one person.
