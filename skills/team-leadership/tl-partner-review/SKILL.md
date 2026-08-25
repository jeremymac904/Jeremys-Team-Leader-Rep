---
name: tl-partner-review
description: "Review Realtor and referral-partner relationships, find inactivity, and plan the next value touch."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [team-leader, partners, realtors, referrals, weekly]
---

# Referral Partner Review

## Purpose
Referral relationships decay quietly. This review finds partners who have gone cold,
partners producing below their potential, and the specific next value touch for each —
so partner strategy stays deliberate instead of reactive.

## When Hermes should use it
Use for a weekly partner review, before an agent meeting, or when referral volume drops.
## Required information
- A partner list with last-contact date and referral counts, from `team-data/` or pasted
- The team's `minimum_realtor_meetings_per_week` standard
- Which LO owns each relationship

## Tools and commands it may use
Reading provided data. Drafting outreach and value items for review. Public research on
an agent's market activity, cited. **No contact with any partner.**

## Safety boundaries
Partner lists are business-confidential. Keep them in `team-data/`. Do not put real agent
names into examples or commits.

## Human approval requirements
Every message to a partner is drafted, reviewed by the leader or the owning LO, and sent
by a human.

## Workflow
1. Segment partners: **producing** (referred recently), **warm** (engaged, no recent
   referral), **cold** (no contact in 60+ days), **new** (not yet tested).
2. Flag the decay cases specifically: a partner who used to refer and stopped is the most
   urgent category, and the most commonly missed.
3. Check per-LO meeting activity against the team standard.
4. For each flagged partner, propose one **specific value item** — a market update for
   their listings, buyer education for their open house, a fast-turn commitment, a
   co-branded piece — not "check in."
5. Draft the touch for human review where useful.
6. Emit the review.

## Evidence rules
Every "gone quiet" claim carries the last-contact date and the prior referral cadence.
Public research about an agent's activity carries a source and date.

## Expected output
```
PARTNER REVIEW — <date>   |   <N> partners

STOPPED REFERRING  (highest priority)
- <partner> — owned by <LO> — last referral <date>, previously ~<cadence>
  Value item: <the specific thing>
  Draft touch: "<message for human review>"

COLD 60+ DAYS
- <partner> — <LO> — last contact <date> — <re-engage or retire?>

WARM, NOT CONVERTING
- <partner> — engaged but no referrals — <what to test>

MEETING ACTIVITY vs STANDARD
<LO>: <N> meetings this week (standard: <N>)

NEW PARTNERS TO TEST
- ...
```

## Stop conditions
Stop if asked to send outreach directly, to offer anything of value in exchange for
referrals (RESPA — flag it and say a human and compliance must review), or to quote rates
in partner-facing content.

## Error behavior
Without last-contact dates you cannot detect decay. Say so and ask for that one column
rather than producing a list that looks analytical but is not.

## Related skills
- `tl-content-plan` — content used as a partner value item
- `tl-pipeline-review` — files tied to a partner

## What this skill must not assume
- **Do not assume a quiet partner is lost.** Something specific usually happened.
- **Do not assume referral counts measure the relationship.**
- **Do not assume a value item is compliant.** RESPA applies — flag, do not clear.
- **Do not assume the owning LO has already followed up.**

## Tests
- Flags RESPA-sensitive "value exchange" requests instead of drafting them.
- Never sends anything.
- Every value item is specific, never "check in."
- Decay claims cite dates.
