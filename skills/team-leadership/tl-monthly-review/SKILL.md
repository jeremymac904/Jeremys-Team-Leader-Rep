---
name: tl-monthly-review
description: "Monthly production review and quarterly planning: team performance trends, capacity, and the next quarter's plan."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [team-leader, executive, monthly, quarterly, planning]
---

# Monthly Production Review

## Purpose
Step back far enough to see structure instead of noise: multi-month trends per Loan
Officer, team capacity, where growth actually came from, and what the next quarter needs.

## When Hermes should use it
Use at month end, for quarterly planning, or when assessing team structure.
## Required information
- Monthly production by LO for at least 3 months
- `production_goals` (team units, team volume, personal units)
- Roster with tenure — ramp curves matter when judging a newer LO
- Recruiting pipeline status

## Tools and commands it may use
Reading configuration and provided data. Analysis and drafting.

## Safety boundaries
Read-only. Individual production is confidential — keep the output in `team-data/`.

## Human approval requirements
None to produce. Any compensation or staffing decision is a human decision.

## Workflow
1. Team totals vs goal, this month and trailing three.
2. Per-LO trajectory, judged against tenure. A 5-month LO doing 3 units is a different
   story from a 5-year LO doing 3 units. Say which story it is.
3. Concentration risk: what share of production comes from the top one or two people?
   Name the exposure.
4. Capacity: who is at their ceiling and needs support, who has room.
5. Source analysis, if the data supports it: where did the business actually come from?
6. Quarter plan: 3 objectives with the number that proves each one.
7. Emit the review.

## Evidence rules
Every trajectory claim shows the monthly series. Concentration risk shows the percentage.
Never compare an LO to an industry benchmark you cannot source.

## Expected output
```
MONTHLY REVIEW — <month>

TEAM
Units: <actual> / <goal>   Volume: <actual> / <goal>
Trailing 3: <m1> → <m2> → <m3>

BY LOAN OFFICER
<name> (<tenure>): <m1> → <m2> → <m3>  —  <trajectory read against tenure>

CONCENTRATION
Top <N> produce <X>% of team units.  Exposure: <plain statement>

CAPACITY
At ceiling: <who> — <what support would unlock>
Room to grow: <who> — <what is missing>

WHERE BUSINESS CAME FROM
<sources, if the data supports it — otherwise say the data does not>

NEXT QUARTER — THREE OBJECTIVES
1. <objective> — measured by <number>

DECISIONS FOR YOU
<staffing, support, or investment questions — stated, not answered>
```

## Stop conditions
Stop short of recommending compensation changes, terminations, or promotions. Frame those
as decisions for the leader, and note that HR should be involved.

## Error behavior
With fewer than 3 months of data, report what exists and state that trajectory analysis
needs more history.

## Related skills
- `tl-weekly-review` — the weekly input
- `tl-recruiting-review` — when capacity says hire
- `tl-development-plan` — for individuals the review flags

## What this skill must not assume
- **Do not assume tenure-adjusted expectations without knowing tenure.**
- **Do not assume concentration risk is bad** — it is an exposure to state, not a fault.
- **Do not compare to industry benchmarks** you cannot source.
- **Do not recommend compensation, promotion, or termination.** Frame them as the leader's decisions.

## Tests
- Judges each LO against tenure, not a flat standard.
- Always reports concentration risk as a percentage.
- Frames staffing/comp as decisions, never recommendations.
