---
name: realtor-marketing-coach
description: "Build Realtor-facing content and partner value plans that earn relationships instead of asking for business."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [marketing, realtors, partners, content]
---

# Realtor Marketing Coach

## Purpose
Realtors do not need another lender asking for buyers. This builds content and value plans
that demonstrate deal-structure competence and make partners more effective — which is what
actually earns referrals.

## When Hermes should use it
Use when the Team Leader wants Realtor-facing content, a partner value plan, Realtor
education for the team, or is coaching an LO whose business is partner-driven.

## Required information
- The LO's profile, especially `referral_partner_type`
- What the partners actually struggle with — ask if unknown
- Any specific partner being targeted
- The team's `content_pillars`

## Tools and commands it may use
Reads configuration and the shared marketing knowledge. Drafts content. Takes no outward
action — nothing is posted, scheduled, or sent.

Shared knowledge this skill applies:
- `knowledge/marketing/marketing-compliance.md`
- `knowledge/marketing/brand-voice.md`
- `knowledge/marketing/realtor-value.md`
- `knowledge/marketing/cta-system.md`

## Workflow
1. **Establish what the partners' real problem is.** Deals falling apart late, slow
   communication, unrealistic pre-approvals, buyers who cannot actually buy. If unknown,
   the first deliverable is the question to ask them — not content.
2. Use the Realtor post framework in `realtor-value.md`: hook the deal risk, explain the
   cause, show how the LO helps, invite a conversation.
3. **Never write "send me your buyers."** It is the thing every other lender says.
4. Build value items that are specific and forwardable — buyer education with the agent's
   name on it, a readiness checklist, a market update they can send their own sphere.
5. For an LO with a Realtor-heavy mix, weight the calendar accordingly — 40%+ rather than
   the default 20%.
6. **Flag RESPA exposure** on anything of value flowing to a referral source, especially
   co-branded material and cost-sharing. Flag; do not clear.

## Expected output
```
REALTOR MARKETING PLAN — <LO name>
Partner type: <type>   Their core problem: <specific>

CONTENT PIECES
  1. <title>
     Deal risk : <what goes wrong>
     Cause     : <why>
     Value     : <how the LO helps identify options>
     CTA       : "<partner-appropriate ask>"
     Format    : <format>

VALUE ITEMS  (things partners can actually use)
  - <item> — <why it makes them look good to their client>
    RESPA flag: <none | needs compliance review before offering>

IF THE PROBLEM IS UNKNOWN
  Ask them: <the specific questions>

NEVER SAY
  "Send me your buyers." Show the thinking instead.
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
> "Create a Realtor focused content plan for Sam."
> "Create Realtor education content for my team."
> "Build a Realtor workshop campaign."

## Related skills
- `tl-partner-review` — which partners need attention
- `content-calendar-builder` — schedules these pieces
- `campaign-builder` — for workshops and events
- `tl-guideline-research` — sourced content for agent education

## What this skill must not assume
- **Do not assume you know their problem.** Ask. The answer is specific and rarely rate.
- **Do not assume co-branded content is fine.** RESPA applies; flag it.
- **Do not assume partners want to be marketed to.** They want to be made effective.
- **Do not assume every LO should target Realtors.** A consumer-direct LO may not.
- **Do not promise approvals or closings** in partner-facing content.

## Tests
- Never produces 'send me your buyers' content.
- Every value item is specific and forwardable.
- RESPA-sensitive items are flagged, not cleared.
- Asks for the partner's real problem when it is unknown.
