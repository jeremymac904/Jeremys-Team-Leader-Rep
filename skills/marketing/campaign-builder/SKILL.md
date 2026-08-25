---
name: campaign-builder
description: "Build a time-bound marketing campaign around a loan program, event, or audience."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [marketing, campaign, planning, programs]
---

# Campaign Builder

## Purpose
Turn a goal into a structured campaign with an audience, an arc, a schedule, and a
follow-up plan — instead of a burst of posts with no end and no measurement.

## When Hermes should use it
Use when the Team Leader wants a campaign around a loan program, a workshop or seminar, a
seasonal moment, or a market shift. Not for ongoing content — that is
`content-calendar-builder`.

## Required information
- The goal and how it will be measured
- The audience — specifically
- Duration, default four weeks
- The program or event
- Who handles responders

## Tools and commands it may use
Reads configuration and the shared marketing knowledge. Drafts content. Takes no outward
action — nothing is posted, scheduled, or sent.

Shared knowledge this skill applies:
- `knowledge/marketing/marketing-compliance.md`
- `knowledge/marketing/brand-voice.md`
- `knowledge/marketing/campaign-planning.md`
- `knowledge/marketing/cta-system.md`

## Workflow
1. **Check this is actually a campaign.** "We should market more" is cadence, not a
   campaign. A campaign has one goal, one audience, and an end date. Say so if it does not.
2. Define the elements from `campaign-planning.md`: goal, audience, duration, core message,
   CTA, follow-up, measurement.
3. **Write the core message as one sentence.** If it takes three, it is two campaigns —
   split it.
4. Build the arc: problem awareness → education → proof → direct offer. **The ask comes
   last**, after three weeks of usefulness. Leading with the ask is why campaigns fail.
5. For program campaigns: name the audience's real problem, correct the common
   misconception, and **state honestly what disqualifies people** — that builds more trust
   than the upside. Never state eligibility rules as fact without a source; route to
   `tl-guideline-research`.
6. **Define follow-up before launch.** Who responds, how fast, what the second touch is,
   when a lead is retired. A campaign without this is content with a deadline.
7. Flag the whole campaign for compliance review before the first piece — program and rate
   campaigns carry the highest exposure of any marketing work.

## Expected output
```
CAMPAIGN — <name>
Goal: <specific + how measured>   Audience: <specific>   Runs: <start> to <end>

CORE MESSAGE
  <one sentence>

ARC
  Week 1 — Problem awareness : <pieces>
  Week 2 — Education         : <pieces>
  Week 3 — Proof             : <pieces>
  Week 4 — Direct offer      : <the single ask>

CTA (consistent throughout)
  "<the ask>"

HONEST DISQUALIFIERS
  <who this genuinely is not for — builds trust>

FOLLOW-UP
  Responder goes to : <who>   Response time: <target>
  Second touch      : <what, when>
  Retire after      : <when>

MEASUREMENT
  <the number that says whether this worked>

COMPLIANCE
  Review the full campaign before the first piece publishes.
  Guideline claims requiring sourcing: <list>
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
> "Build a campaign around VA loans."
> "Create a Realtor workshop campaign."
> "We want a first-time buyer campaign for spring."

## Related skills
- `content-calendar-builder` — schedules campaign pieces
- `tl-guideline-research` — sources any program claims
- `realtor-marketing-coach` — for partner-facing campaigns
- `marketing-performance-review` — measures the result

## What this skill must not assume
- **Do not assume every marketing push is a campaign.** Say when it is really cadence.
- **Do not state program eligibility as fact.** Route to guideline research with sources.
- **Do not lead with the ask.**
- **Do not assume follow-up will happen.** Name the owner and the timing.
- **Do not assume the audience is broad.** Narrow campaigns outperform.
- **Do not include rate content** unless allowed and disclosed.

## Tests
- Distinguishes a real campaign from ongoing cadence.
- Core message is one sentence.
- The direct ask lands last.
- Follow-up has a named owner and timing.
- Program claims are routed for sourcing.
- States honest disqualifiers.
