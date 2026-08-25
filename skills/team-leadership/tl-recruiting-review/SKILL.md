---
name: tl-recruiting-review
description: "Review the recruiting pipeline, prepare interviews, compare candidates, and plan onboarding."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [team-leader, recruiting, hiring, pipeline]
---

# Recruiting Review

## Purpose
Keep recruiting from becoming the thing that only happens when someone quits. Review the
candidate pipeline, surface stalled conversations, prepare interviews, and structure
comparisons against the leader's stated target profile.

## When Hermes should use it
Use for a weekly recruiting review, before an interview, or when comparing candidates.
## Required information
- `recruiting_pipeline` from `team-data/team.yaml`
- `goals.recruiting_goals` from `config/team-leader.yaml` (hires per quarter, target profile)
- Notes from prior conversations, in `team-data/`

## Tools and commands it may use
Reading configuration and notes. Drafting questions, comparisons, and outreach for review.
Public research about a company or market. **No contact with any candidate.**

## Safety boundaries
Candidate information is confidential and sensitive — these are people considering leaving
a job. It lives in `team-data/` only. Never commit it, never put it in an example, never
mention a real candidate in shareable output.

Do not research a candidate's private life. Public professional information only.

## Human approval requirements
Every message to a candidate is drafted for the leader and sent by the leader.

## Workflow
1. Review each candidate's stage and days since last contact. Flag anything stalled.
2. Check pace against `hires_per_quarter` — is the top of the funnel wide enough?
3. For an upcoming interview, prepare questions against the `target_profile`, weighted to
   what actually predicts success on this team: consistency, coachability, existing
   relationships, and honesty about their numbers.
4. For a comparison, score candidates on the same declared criteria. Show the criteria.
5. For onboarding, produce a first-30-days plan tied to the ramp track in
   `config/coaching.yaml`.
6. Emit the review.

## Evidence rules
Cite the candidate's own stated numbers as *stated*, not verified. Public research carries
a source and date.

## Expected output
```
RECRUITING REVIEW — <date>
Goal: <N> hires/quarter | In pipeline: <N> | Pace: <on track / behind>

NEEDS ATTENTION
- <candidate> — <stage> — <days since contact> — <the specific next move>

STALLED
- <candidate> — <how long> — <close it out or re-engage?>

FUNNEL
<is the top wide enough for the goal? what would widen it?>

INTERVIEW PREP — <candidate>   (if requested)
Against target profile: <the leader's stated profile>
Ask: 1. ... 2. ...
Listen for: ...
Verify: <what they claimed that should be checked>

COMPARISON   (if requested)
Criteria: <declared, same for everyone>
<candidate A>: ... | <candidate B>: ...
```

## Stop conditions
Stop if asked to: contact a candidate directly; research private/personal life; evaluate
on any protected characteristic; make compensation commitments; or write an offer or
employment agreement. Those need a human and, for offers, HR/legal.

## Error behavior
If the recruiting pipeline is empty, say so and shift to sourcing strategy rather than
reviewing nothing.

## Related skills
- `tl-development-plan` — onboarding a new hire
- `tl-monthly-review` — capacity that justifies hiring

## What this skill must not assume
- **Do not assume a candidate's stated production is verified.** Label it as claimed.
- **Do not assume a stalled candidate is uninterested.**
- **Do not assume a top producer will transfer their book.**
- **Never assume anything from a name, photo, or any protected characteristic.**

## Tests
- Refuses to contact candidates.
- Refuses evaluation on protected characteristics.
- Comparison criteria are declared before scoring.
- Candidate-stated numbers are labeled as unverified.
