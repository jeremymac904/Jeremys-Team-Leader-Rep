---
name: content-calendar-builder
description: "Turn a strategy into a dated content calendar with specific topics, formats, and CTAs."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [marketing, content, calendar, planning]
---

# Content Calendar Builder

## Purpose
Produce a calendar specific enough to execute without further thinking — dated, with the
topic, format, hook, and CTA already decided. Vague calendars do not get used.

## When Hermes should use it
Use when the Team Leader asks for a content plan or calendar for a Loan Officer or the
team, or after `lo-marketing-coach` has produced a strategy that needs dates.

## Required information
- The LO's profile, or the team defaults
- Period to cover (default 30 days)
- **Questions the team is actually being asked this week** — the best possible input
- Any campaign running in the same period

## Tools and commands it may use
Reads configuration and the shared marketing knowledge. Drafts content. Takes no outward
action — nothing is posted, scheduled, or sent.

Shared knowledge this skill applies:
- `knowledge/marketing/marketing-compliance.md`
- `knowledge/marketing/brand-voice.md`
- `knowledge/marketing/content-strategy.md`
- `knowledge/marketing/cta-system.md`

## Workflow
1. **Ask for real questions first.** Content built from questions the team is genuinely
   fielding outperforms generated topics every time. Only fall back to pillars if none are
   offered.
2. Apply the content mix — the LO's override if present, otherwise the team default.
3. Use the weekly structure in `content-strategy.md` as the skeleton so each day has a job.
4. For each slot specify: **date, pillar, topic, format, hook, one teaching point, CTA**.
   A calendar entry that says "post about FHA" is not usable.
5. Match formats to `comfort_with_video` and `preferred_format`. Never schedule video for a
   camera-shy LO.
6. **Mark batching days** — group everything filmable or writable together.
7. Flag any entry needing compliance review before it is drafted.
8. Leave slack. A calendar with no gaps breaks on the first busy week.

## Expected output
```
CONTENT CALENDAR — <LO or team> — <period>
Cadence: <n>/week   Platforms: <list>   Mix: <summary>

WEEK 1
  <date>  <pillar>
    Topic  : <specific>
    Format : <written | carousel | video | story>
    Hook   : "<the actual opening line>"
    Point  : <the one thing they learn>
    CTA    : "<the actual ask>"
    Flags  : <compliance review needed, or none>

  BATCH DAY: <date> — produce <items> together (<estimated time>)

...

SOURCED FROM
  <which real questions drove which entries>

GAPS LEFT ON PURPOSE
  <where there is slack, and why>
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
> "Build a content calendar for Sam for next month."
> "Turn this training topic into a month of content."
> "Give me a 30 day Realtor focused content plan for Jordan."

## Related skills
- `lo-marketing-coach` — supplies the strategy
- `content-repurposing` — fills the calendar from one asset
- `campaign-builder` — when the period contains a campaign
- `social-content-strategist` — for platform specifics

## What this skill must not assume
- **Do not assume they can produce every format.** Check comfort and preference.
- **Do not fill every slot.** Slack is what makes a calendar survive a busy week.
- **Do not assume topics are evergreen** — market-dependent entries expire.
- **Do not schedule rate content** unless `allow_rate_content` is true.
- **Do not assume the team mix applies** to a specialist LO.

## Tests
- Every entry has a date, topic, format, hook, point, and CTA.
- Formats respect comfort_with_video.
- Batching days are marked.
- Real questions are used when supplied, and the source is shown.
- Deliberate gaps are left.
