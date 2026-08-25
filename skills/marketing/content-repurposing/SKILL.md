---
name: content-repurposing
description: "Turn one substantial asset — a training, webinar, or long video — into weeks of content."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [marketing, content, repurposing, leverage]
---

# Content Repurposing

## Purpose
Most Loan Officers create one good thing then start from zero again. This turns a single
recording or training into 20+ pieces, which is the difference between a sustainable
cadence and burnout.

## When Hermes should use it
Use when the Team Leader has a training, webinar, podcast, long video, or written piece and
wants more from it — or when an LO produces good content but not enough of it.

## Required information
- The source asset: transcript, recording notes, outline, or the written piece
- Which LO will publish it and their formats
- The period to spread it across

## Tools and commands it may use
Reads configuration and the shared marketing knowledge. Drafts content. Takes no outward
action — nothing is posted, scheduled, or sent.

Shared knowledge this skill applies:
- `knowledge/marketing/marketing-compliance.md`
- `knowledge/marketing/brand-voice.md`
- `knowledge/marketing/content-repurposing.md`

## Workflow
1. **Extract the distinct teaching points.** Most 20-minute assets contain 5–8. Each becomes
   the seed of a piece.
2. Map to outputs using the table in `content-repurposing.md` — short clips, carousels,
   written posts, stories, email, Realtor one-pager, long post, FAQ entries.
3. **Reframe, do not re-cut.** A Realtor version needs a different hook and next step, not
   the same text rebranded. This is where most repurposing goes wrong.
4. **Re-check compliance on every derived piece.** A claim that was safe inside a full
   explanation can mislead as a 30-second clip stripped of context. This is the single most
   important step and the most commonly skipped.
5. Space them across the period. Ten pieces over three weeks, never ten in one day.
6. Note what should NOT be repurposed — time-sensitive commentary, anything with numbers,
   and anything that was weak originally.

## Expected output
```
REPURPOSING PLAN — <source asset>
Teaching points found: <n>   Pieces produced: <n>   Spread over: <period>

TEACHING POINTS
  1. <point> -> <which outputs>

OUTPUT PLAN
  <format>  <n> pieces
    - <title> — <angle> — <audience> — week <n>
      Reframed for: <audience>, so the hook becomes "<new hook>"
      Compliance re-check: <clean | flag>

DO NOT REPURPOSE
  - <part> — <why: time-sensitive / contains numbers / was weak>

SEQUENCING
  Week 1: <pieces>   Week 2: <pieces>   ...
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
> "Turn one training into ten pieces of content."
> "We recorded a webinar on VA loans — what can we get out of it?"
> "Priya posts good videos but not enough. Fix that."

## Related skills
- `content-calendar-builder` — places the output on dates
- `video-script-builder` — scripts derived clips
- `lo-marketing-coach` — for the strong-video and has-content archetypes

## What this skill must not assume
- **Do not assume everything repurposes.** Time-sensitive and numeric content does not.
- **Do not assume a clip keeps its context.** Compliance must be re-checked per piece.
- **Do not multiply weak content.** Repurposing scales reach, not quality.
- **Do not assume one platform's format works elsewhere.**
- **Do not schedule them all at once.**

## Tests
- Extracts distinct teaching points before proposing outputs.
- Every derived piece is reframed, not just re-cut.
- Compliance is re-checked per piece.
- Names what should not be repurposed.
- Spreads output across the period.
