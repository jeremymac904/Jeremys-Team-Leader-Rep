---
name: social-post-review
description: "Review a draft social post or script for compliance, clarity, and whether it will actually work."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [marketing, review, compliance, content]
---

# Social Post Review

## Purpose
Check a draft before it publishes: compliance exposure first, then whether it teaches
anything, then whether the hook and CTA earn their place. Then rewrite the weakest part
with exact words.

## When Hermes should use it
Use when the Team Leader or a Loan Officer supplies a draft post, caption, script, or email
and wants it checked or improved. Prefer this over general writing feedback.

## Required information
- The draft
- Intended platform and audience
- Whose voice it should be in, if a specific LO

## Tools and commands it may use
Reads configuration and the shared marketing knowledge. Drafts content. Takes no outward
action — nothing is posted, scheduled, or sent.

Shared knowledge this skill applies:
- `knowledge/marketing/marketing-compliance.md`
- `knowledge/marketing/brand-voice.md`
- `knowledge/marketing/content-strategy.md`
- `knowledge/marketing/cta-system.md`

## Workflow
1. **Compliance first, before anything else.** Scan against
   `marketing-compliance.md`: rate/payment/fee figures, guarantees, universal
   qualification, government endorsement implications, protected-class targeting, tax or
   legal advice, competitor attacks, non-Loan Factory branding. Anything found is a **STOP**,
   not a suggestion.
2. Classify the content category so the reviewer knows the exposure level.
3. Check it has the five essentials from `content-strategy.md`: specific audience, real
   mortgage problem, one teaching point, one practical next step, safe language.
4. **Test the hook.** Does it name a specific mortgage problem, or is it generic attention
   bait? Most weak posts fail here.
5. Check the CTA asks for information rather than a commitment, and is specific.
6. Check the voice against the LO's `brand_voice` — not a house style they cannot sustain.
7. **Rewrite the single weakest element with exact words.** "Make the hook stronger" changes
   nothing; supplying the replacement line does.
8. Confirm the disclosure is present if required.

## Expected output
```
POST REVIEW
Category: <educational | general marketing | loan program | rate-related>
Platform: <platform>   Audience: <who>

COMPLIANCE
  [STOP]  <violation> — "<the exact phrase>" — <why> — <replacement>
  [FLAG]  <needs review>
  [OK]    <no issues found>
  Disclosure required: <yes/no>   Present: <yes/no>

THE FIVE ESSENTIALS
  Specific audience    <yes/no>
  Real problem         <yes/no>
  One teaching point   <yes/no — or "three, pick one">
  Practical next step  <yes/no>
  Safe language        <yes/no>

HOOK
  Current : "<quote>"
  Verdict : <names a specific problem | generic>
  Rewrite : "<exact replacement>"

CTA
  Current : "<quote>"
  Verdict : <specific and low-commitment | vague>
  Rewrite : "<exact replacement>"

VOICE
  <matches their brand_voice, or where it drifts>

VERDICT: <publish as is | publish with these edits | do not publish>
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
> "Review this social media post and improve it."
> "Is this caption compliant?"
> "Make this script better."

## Related skills
- `video-script-builder` — for a full rewrite
- `brand-voice-builder` — if voice drift is systematic
- `content-calendar-builder` — for the surrounding plan

## What this skill must not assume
- **Do not assume a post is compliant because it sounds harmless.** Check explicitly.
- **Do not soften a compliance problem into a suggestion.** It is a STOP.
- **Do not impose a house voice** over the LO's configured voice.
- **Do not assume the LO wrote it** — it may be AI-generated and need heavier scrutiny.
- **Do not approve.** The verdict is advisory; a human decides.

## Tests
- Compliance is checked before style, always.
- Violations are STOP, not suggestions.
- Hook and CTA get exact replacement wording.
- Content category is stated.
- Never claims to approve content.
