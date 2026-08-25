---
name: tl-content-plan
description: "Plan team marketing content and draft scripts for Realtor and consumer education. Marketing-compliance aware."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [team-leader, marketing, content, realtors, education]
---

# Team Content Plan

## Purpose
Keep the team visible without the leader inventing content every week. Produce a content
plan and draft scripts for Realtor education, consumer education, and team positioning.

## When Hermes should use it
Use when planning marketing content, drafting a script, or building Realtor education.
## Required information
- `marketing_goals` from `config/team-leader.yaml`
- `mortgage_specialties` and `primary_market`
- Questions the team is actually being asked — the best content source there is
- Which LOs will appear in or distribute the content

## Tools and commands it may use
Drafting. Public research with citation. **No publishing, no posting, no scheduling.**

## Safety boundaries
Content is outward-facing and subject to advertising rules. Everything you produce is a
draft for human review and, where required, compliance review.

## Human approval requirements
Publishing always requires the leader's approval, and marketing content usually requires
company compliance review. State this on every output.

## Workflow
1. Source topics from real questions the team is fielding, then from the leader's
   `marketing_goals`. Not from generic "mortgage content ideas."
2. Split by audience — Realtor education and consumer education are different jobs, with
   different compliance exposure. Do not blend them.
3. For each piece: the hook, the single point, the concrete example, the call to action.
4. Apply advertising guardrails while drafting:
   - No rate or payment figure without the disclosures that must accompany it — and note
     that you are not producing those disclosures
   - No "guaranteed," "approved," "lowest," or "best" claims
   - No promise of approval or of a specific outcome
   - No comparison that disparages a named competitor
   - Include the trigger-term warning if a rate, term, or payment appears
5. Build the calendar to the cadence in `marketing_goals` — no more.
6. Emit the plan with the compliance note attached.

## Evidence rules
Any statistic or market claim carries a source and date. Never a rate quote.

## Expected output
```
CONTENT PLAN — <period>          [MARKETING — REQUIRES REVIEW BEFORE PUBLISHING]
Cadence: <from marketing_goals>

REALTOR EDUCATION
1. <title>
   Hook: ...   Point: ...   Example: ...   CTA: ...
   Format: <video / email / one-pager>   Owner: <LO>

CONSUMER EDUCATION
1. <title>
   ... (same structure)

SCRIPT — <the one to shoot first>
<the actual draft>

COMPLIANCE FLAGS
- <anything in these drafts that needs review, e.g. a rate/term/payment reference>
- ⚠ No rate, APR, payment, or term appears here without required disclosures. If you add
  one, trigger-term advertising rules apply and this must go to compliance.
- Company policy on advertising, rates, and fees governs. Nothing here is approved
  advertising until a human approves it.
```

## Stop conditions
Stop if asked to publish or schedule anything, to include a specific rate or APR, to make
a guarantee or superiority claim, or to name and disparage a competitor.

## Error behavior
If the leader has not set `marketing_goals`, propose a minimum sustainable cadence
(one piece per week) and say that is an assumption.

## Related skills
- `tl-partner-review` — partner value items
- `tl-guideline-research` — sourced educational content

## What this skill must not assume
- **Do not assume content is approved.** Everything here is a draft for review.
- **Do not assume advertising rules do not apply** — they apply to almost all of this.
- **Do not assume the team has capacity** for the cadence you propose.
- **Do not include a rate, APR, or payment figure.** That triggers disclosure requirements.

## Tests
- Every output carries the marketing label and review requirement.
- Never includes a rate or APR figure.
- Rejects "guaranteed" / "lowest" / "approved" claims.
- Separates Realtor and consumer audiences.
- Never publishes.
