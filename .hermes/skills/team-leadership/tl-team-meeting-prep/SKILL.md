---
name: tl-team-meeting-prep
description: "Build a team meeting agenda with a training topic, wins, pipeline themes, and tracked action items."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [team-leader, meetings, training, weekly]
---

# Team Meeting Prep

## Purpose
Produce a timed agenda for the weekly team meeting that teaches something specific,
recognizes real wins, addresses the actual pipeline pattern, and ends with tracked
action items — instead of a status round-robin.

## When Hermes should use it
Use before a recurring team meeting, or when the Team Leader asks what to cover.
## Required information
- `schedule.meeting_schedule` from `config/team-leader.yaml` (duration)
- The roster
- This week's pipeline review or scorecards, if available
- Last meeting's action items
- The leader's `team_goals` and `marketing_goals`

## Tools and commands it may use
Reading configuration and provided data. Drafting the agenda and the recap.
Public research for market talking points, cited with dates.

## Safety boundaries
Do not put individual underperformance in a group agenda. Patterns are for the room;
individuals are for the one-on-one.

## Human approval requirements
None to draft. Distributing it to the team is a human action.

## Workflow
1. Read last meeting's action items and check which closed.
2. Pick **one** training topic, driven by the pattern in this week's data — not a topic
   rotation. If three LOs are losing files at the same stage, that is the topic.
3. Collect wins that are specific and attributable. "Sam closed the self-employed file
   two other lenders declined" beats "great week everyone."
4. Identify the pipeline theme that belongs in the room.
5. Add market talking points only if you have a cited, dated public source.
6. Time-box every block to fit the actual meeting duration. Sum the minutes and check.
7. Draft 2–3 action items with an owner and a due date each.
8. Emit the agenda, plus a recap template the leader can fill in afterward.

## Evidence rules
Market or rate commentary carries source and date, and is labeled education. Never a
rate quote. Wins name the person and what they specifically did.

## Expected output
```
TEAM MEETING — <date> — <N> minutes

0:00 (5m)  Wins
  - <person> — <specific thing>

0:05 (10m) Last week's action items
  - <item> — <owner> — <closed / carried>

0:15 (20m) TRAINING: <topic>
  Why this week: <the pattern in the data>
  Teach: ...
  Drill: <live rep, not a lecture>

0:35 (10m) Pipeline theme
  <the pattern, not individuals>

0:45 (10m) Market / product note   [EDUCATION — source: <name>, <date>]
  ...

0:55 (5m)  Action items
  1. <what> — <owner> — <due>

--- RECAP TEMPLATE (fill after the meeting) ---
Decided: ...   Assigned: ...   Carried: ...   Next week's topic: ...
```

## Stop conditions
Stop if asked to put a named individual's shortfall on a group agenda. Offer to prepare
a one-on-one instead.

## Error behavior
With no pipeline data, pick the training topic from the roster's shared development areas
and say that is what you used.

## Related skills
- `tl-training-plan` — chooses the training topic
- `lo-marketing-coach` — for a marketing training segment
- `tl-pipeline-review` — supplies the pipeline theme
- `tl-role-play` — for the in-meeting drill

## What this skill must not assume
- **Do not assume last meeting's action items were completed.**
- **Do not assume the whole team shares the same gap.**
- **Do not assume a full agenda is a good agenda.** Fewer, deeper items beat a packed hour.
- **Do not assume market commentary is current** without a dated source.

## Tests
- Block minutes sum to the configured meeting duration.
- No individual underperformance named in the agenda.
- Market content carries a source and date and is labeled education.
- Always produces action items with owners.
