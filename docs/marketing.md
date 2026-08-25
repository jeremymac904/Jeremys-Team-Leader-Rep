# The marketing system

<img src="../assets/branding/loan-factory-logo-360w.png" alt="Loan Factory" width="180">

Ten skills, a shared knowledge base, and 14 automations for coaching Loan Officer
marketing — built so the advice is specific to the person rather than generic.

## The skills

| Skill | Use it when |
|---|---|
| [`lo-marketing-coach`](../.hermes/skills/marketing/lo-marketing-coach/SKILL.md) | Building or reviewing a Loan Officer's marketing plan |
| [`content-calendar-builder`](../.hermes/skills/marketing/content-calendar-builder/SKILL.md) | Turning strategy into a dated calendar |
| [`realtor-marketing-coach`](../.hermes/skills/marketing/realtor-marketing-coach/SKILL.md) | Realtor-facing content and partner value plans |
| [`video-script-builder`](../.hermes/skills/marketing/video-script-builder/SKILL.md) | Short-form scripts, including no-camera formats |
| [`content-repurposing`](../.hermes/skills/marketing/content-repurposing/SKILL.md) | One training into weeks of content |
| [`campaign-builder`](../.hermes/skills/marketing/campaign-builder/SKILL.md) | A program, workshop, or seasonal campaign |
| [`social-post-review`](../.hermes/skills/marketing/social-post-review/SKILL.md) | Checking a draft before it publishes |
| [`brand-voice-builder`](../.hermes/skills/marketing/brand-voice-builder/SKILL.md) | An LO whose content sounds generic |
| [`marketing-accountability`](../.hermes/skills/marketing/marketing-accountability/SKILL.md) | Who is actually executing their plan |
| [`marketing-performance-review`](../.hermes/skills/marketing/marketing-performance-review/SKILL.md) | Is any of this working? |

## Just ask

The agent routes to the right skill:

> "Build a 30 day marketing plan for Jordan."
> "Create a Realtor focused content plan."
> "Give me five content ideas for today's market."
> "Turn this guideline change into Realtor education."
> "Build a weekly content accountability plan for my team."
> "Create a marketing training for Friday's team meeting."
> "Review this social media post and improve it."
> "Build a campaign around VA loans."
> "Turn one training into ten pieces of content."
> "Create a video script for a Loan Officer who hates being on camera."

## Why the advice is specific

Most Loan Officer marketing coaching fails because it treats everyone the same. Each LO
gets an **archetype** in `config/marketing.yaml`, and the skills coach accordingly:

| Archetype | What they actually need |
|---|---|
| `no-audience` | One platform, two posts a week, consistency only |
| `established-partners-no-content` | Realtor content their existing partners can use |
| `camera-shy` | Written and screen-recording formats. Never "just start posting video." |
| `strong-video` | Repurposing — they are leaving most of the value unused |
| `writer` | Tightening, then a path toward video |
| `realtor-focused` | A partner-heavy content mix, well above the default |
| `consumer-direct` | Volume and fast response |
| `inconsistent` | **Cut the target.** Rebuild the streak. |
| `needs-full-plan` | A complete 30-day plan |
| `has-content-needs-systems` | Batching, repurposing, a calendar |

Defined in
[`../knowledge/marketing/lo-marketing-profiles.md`](../knowledge/marketing/lo-marketing-profiles.md).
Validation fails if configuration uses an archetype that is not documented, so the two
cannot drift apart.

## Shared knowledge

Skills reference [`../knowledge/marketing/`](../knowledge/marketing/README.md) rather than
each carrying its own copy of the same principles. Change a rule once and every skill
follows.

Nine files: content strategy, brand voice, compliance, CTAs, video frameworks, Realtor
value, repurposing, campaign planning, and the archetypes.

## Customizing brand voice

Two layers:

- **Team-wide, fixed** — Loan Factory positioning, prohibited language, compliance
- **Per Loan Officer** — tone, vocabulary, humour, story use, formality

Set `brand_voice` per LO in `config/marketing.yaml`, or run `brand-voice-builder` to
develop one. A voice an LO cannot sustain gets abandoned, so the aim is *theirs*, not a
house style.

## Content mix

The default is 40% buyer education, 25% scenario/problem solving, 20% Realtor value,
10% investor/specialty, 5% direct conversion.

Only 5% is a direct ask — the other 95% earns the right to make it. Override per LO; a
Realtor-focused LO should run 40% partner content. Validation checks every mix totals 100.

## Compliance

Every marketing skill applies
[`../knowledge/marketing/marketing-compliance.md`](../knowledge/marketing/marketing-compliance.md).

Content is labeled by category — educational, general marketing, loan program, or
rate-related — so a reviewer knows the exposure. `allow_rate_content` is **false** by
default: no rate, APR, payment, or fee figures unless you have approved terms and the full
disclosure set.

Disclosure text is **configurable**, not hardcoded, because required wording varies by
company and state. Licensing identifiers come from your configuration.

**The agent flags. It does not clear.** Nothing it writes is approved advertising until a
person approves it, and it never publishes.

## Automations

14 marketing automations in [`../automations/README.md`](../automations/README.md) — weekly
content planning, daily ideas from real questions, market news to content, guideline
updates to Realtor education, repurposing, script batching, scorecards, campaign follow-up,
and performance review.

Every one that produces publishable content requires approval. None publishes anything.
The pattern is always: **AI prepares → the LO or Team Leader reviews → a human approves →
publishing happens separately.**

## Brand assets

The official Loan Factory logo is in
[`../assets/branding/`](../assets/branding/README.md). The original is preserved untouched;
one scaled derivative exists for documentation.

Your own team assets go in `assets/team/`, which is gitignored — team graphics may be
licensed and do not belong in a public repository. Point `brand.assets` in
`config/marketing.yaml` at them.

**Do not create unofficial logo variations.** Something that looks official but is not
causes real problems for a regulated brand.

## Where this came from

Derived from Loan Factory marketing source material supplied for this project. What was
extracted, what was excluded and why, and which source won where they overlapped is
recorded in [`provenance.md`](provenance.md).
