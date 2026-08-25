---
name: marketing-accountability
description: "Track whether the team's marketing plans are actually happening, and coach the gap."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [marketing, accountability, team, coaching]
---

# Team Marketing Accountability

## Purpose
Marketing plans fail quietly. This surfaces who is executing, who has stopped, and what to
do about it — treating consistency as the metric that matters, not output volume.

## When Hermes should use it
Use for a weekly or monthly marketing review, when the Team Leader asks who is actually
posting, or when a plan built earlier needs checking.

## Required information
- Each LO's `posting_frequency_target` from `config/marketing.yaml`
- What each actually published — supplied by the Team Leader
- The period

## Tools and commands it may use
Reads configuration and the shared marketing knowledge. Drafts content. Takes no outward
action — nothing is posted, scheduled, or sent.

Shared knowledge this skill applies:
- `knowledge/marketing/marketing-compliance.md`
- `knowledge/marketing/brand-voice.md`
- `knowledge/marketing/lo-marketing-profiles.md`
- `knowledge/marketing/content-strategy.md`

## Workflow
1. Compare actual output against each LO's **own** target, not a team standard. A target
   of two per week met is success; four per week attempted and missed is not.
2. **Measure consistency, not volume.** The metric is consecutive weeks of any output.
   Someone at one post a week for eight weeks is winning; someone who did twelve posts in
   one week and nothing since is not.
3. Identify the failure pattern:
   - **Never started** — the plan was too big, or the format was wrong
   - **Started then stopped** — no batching rhythm; this is the most common
   - **Sporadic** — no calendar
   - **Consistent but ineffective** — a different problem; the system works
4. **Cut the target for anyone who stopped.** The instinct is to push harder; it does not
   work. Halve it and rebuild the streak.
5. Recognize streaks specifically and publicly — consistency is the behavior to reinforce.
6. Recommend one change per person, not a list.

## Expected output
```
MARKETING ACCOUNTABILITY — <period>

BY LOAN OFFICER
  <name>  target <n>/wk  actual <n>/wk  streak <n> weeks  <on track | slipping | stopped>
    Pattern : <never started | started-stopped | sporadic | consistent>
    One change: <the single specific thing>

STREAKS WORTH NAMING
  <name> — <n> consecutive weeks

STOPPED
  <name> — last published <date> — likely cause: <pattern>
    Recommended: cut target to <n>/wk and rebuild

TEAM PATTERN
  <if most of the team stopped, it is a system problem — say so>

WHAT I AM DOING ABOUT IT
  <the Team Leader's actions this week>
```

## Safety boundaries
Apply `knowledge/marketing/marketing-compliance.md` to everything produced. In short:
never generate a rate, APR, payment, fee, or savings figure unless
`compliance.allow_rate_content` is true and the Loan Officer supplied approved terms with
the full disclosure set. Never guarantee approval, eligibility, closing time, or savings.
No protected-class targeting. No tax, legal, credit-repair, or investment advice. No
competitor attacks. Loan Factory branding only.

Label every piece with its content category — educational, general marketing, loan program
marketing, or rate-related — so the reviewer knows the exposure. Attach the configured
disclosure from `config/marketing.yaml`; never hardcode licensing or NMLS data.

The agent flags compliance concerns. It does not clear them.

## Human approval requirements
Everything produced is a **draft**. Publishing always requires a human, and where your
company requires it, compliance review. This skill never posts, schedules, sends, or
publishes anything.

## Examples
> "Build a weekly content accountability plan for my team."
> "Who on my team is actually posting?"
> "Nobody is doing the marketing plan. Why?"

## Related skills
- `lo-marketing-coach` — rebuilds a plan that is not working
- `tl-weekly-review` — surfaces marketing alongside production
- `tl-lo-coaching-prep` — for the one-on-one conversation

## What this skill must not assume
- **Do not assume low output means low effort.** The plan may have been wrong.
- **Do not compare LOs to each other in writing.** It produces hiding, not output.
- **Do not assume pushing harder works.** For someone who stopped, cut the target.
- **Do not assume volume equals effectiveness.** They are separate problems.
- **Do not assume the team standard fits everyone** — targets are per-person.

## Tests
- Measures against each LO's own target.
- Consistency (streak) is the headline metric.
- Identifies the failure pattern before recommending.
- Recommends cutting targets for those who stopped.
- No cross-LO ranking.
