---
name: brand-voice-builder
description: "Define a Loan Officer's distinct marketing voice within the team's positioning and compliance limits."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [marketing, brand, voice, personal-brand]
---

# Brand Voice Builder

## Purpose
Give a Loan Officer a voice they can actually sustain — theirs, not a house style they will
abandon in three weeks — while keeping team positioning and compliance fixed.

## When Hermes should use it
Use when an LO's content sounds generic or inconsistent, when setting up a new LO's
marketing profile, or when the Team Leader asks about personal brand.

## Required information
- The LO's background, niche, and how they actually talk
- Samples of anything they have written or recorded
- Their audience and primary programs

## Tools and commands it may use
Reads configuration and the shared marketing knowledge. Drafts content. Takes no outward
action — nothing is posted, scheduled, or sent.

Shared knowledge this skill applies:
- `knowledge/marketing/marketing-compliance.md`
- `knowledge/marketing/brand-voice.md`

## Workflow
1. **Separate what is fixed from what is theirs.** Fixed: Loan Factory positioning,
   prohibited language, compliance. Theirs: tone, vocabulary, humour, story use, formality,
   sentence length.
2. Find their **actual** voice. Ask how they explain a concept to a client out loud — that
   is usually their real voice, and it is better than anything they write when trying to
   sound professional.
3. Anchor it in their genuine niche and background. A former teacher explaining loans and a
   former investor explaining DSCR should not sound the same.
4. Write it down concretely: three adjectives, vocabulary level, sentence length, humour,
   story use, and three phrases they would say plus three they never would.
5. **Produce two sample pieces in the voice** so it is demonstrated, not described.
6. Note what to avoid — usually imitating someone whose voice they cannot sustain.

## Expected output
```
BRAND VOICE — <LO name>

FIXED (team-wide, not negotiable)
  Positioning: <the pillars>
  Compliance : <the guardrails>

THEIRS
  Three adjectives  : <x>, <y>, <z>
  Vocabulary        : <plain | technical | mixed>
  Sentence length   : <short | varied>
  Humour            : <none | dry | warm>
  Stories           : <often | occasionally | rarely>
  Formality         : <casual | professional-casual | formal>

THEY WOULD SAY
  "<phrase>"  "<phrase>"  "<phrase>"

THEY WOULD NEVER SAY
  "<phrase>"  "<phrase>"  "<phrase>"

ANCHOR
  <the background or niche this voice comes from>

SAMPLE 1 — <format>
  <written in the voice>

SAMPLE 2 — <different format>
  <written in the voice>

AVOID
  <the imitation trap specific to this person>
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
> "Help Jordan find their voice — everything sounds generic."
> "Set up a brand voice for a new LO who works with veterans."

## Related skills
- `lo-marketing-coach` — the surrounding plan
- `social-post-review` — checks drafts against this voice
- `video-script-builder` — writes in this voice

## What this skill must not assume
- **Do not impose a single team voice.** Positioning is shared; voice is not.
- **Do not assume their written voice is their real voice.** Spoken is usually truer.
- **Do not build a voice they cannot sustain.** Aspirational voices get abandoned.
- **Do not let voice override compliance.** Personality never justifies a claim.
- **Do not assume a niche exists** — help them find one if it does not.

## Tests
- Separates fixed positioning from personal voice.
- Produces two demonstrated samples, not just description.
- Includes would-never-say phrases.
- Anchors the voice in real background.
- Compliance stays fixed regardless of voice.
