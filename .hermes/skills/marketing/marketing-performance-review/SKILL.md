---
name: marketing-performance-review
description: "Review what the team's marketing actually produced, and decide what to change."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [marketing, review, performance, analysis]
---

# Marketing Performance Review

## Purpose
Answer the question most marketing avoids: is any of this working? Separate leading
indicators from lagging ones, and be honest when the data cannot support a conclusion.

## When Hermes should use it
Use for a monthly or quarterly marketing review, after a campaign ends, or when the Team
Leader asks whether the marketing effort is worth it.

## Required information
- What was published, by whom, over what period
- Any engagement or response data available
- Actual inbound conversations or leads attributed to content
- The goals from `config/marketing.yaml`

## Tools and commands it may use
Reads configuration and the shared marketing knowledge. Drafts content. Takes no outward
action — nothing is posted, scheduled, or sent.

Shared knowledge this skill applies:
- `knowledge/marketing/marketing-compliance.md`
- `knowledge/marketing/brand-voice.md`
- `knowledge/marketing/content-strategy.md`
- `knowledge/marketing/campaign-planning.md`

## Workflow
1. **State what data you actually have.** Marketing measurement is usually incomplete. Say
   so rather than building a confident conclusion on thin evidence.
2. Separate the layers, because they mean different things:
   - **Output** — did content get produced? (fully controllable)
   - **Reach** — did anyone see it? (partly)
   - **Engagement** — did anyone respond? (partly)
   - **Conversations** — did it start a real conversation? (the one that matters)
   - **Business** — did it produce a loan? (long lag, hard to attribute)
3. **Judge against the right horizon.** Content marketing has a long lag. Three months of
   consistent output with no closings is normal, not failure. Say so — it prevents a Team
   Leader killing something that was about to work.
4. Identify what actually performed and, if the data supports it, why. If it does not
   support a why, say that instead of inventing one.
5. Recommend **one** change. Marketing reviews that produce ten changes produce none.
6. Be willing to conclude that an LO's marketing is not working and their effort is better
   spent on partner relationships. That is a legitimate finding.

## Expected output
```
MARKETING PERFORMANCE — <period>
Data available: <what you actually have>   Missing: <what would help>

OUTPUT
  <LO>: <n> pieces vs <n> target

REACH / ENGAGEMENT
  <what the data shows, or "not available">

CONVERSATIONS STARTED
  <the number that matters most, if known>

WHAT PERFORMED
  <piece or theme> — <why, if the data supports it; otherwise "cause unclear">

HORIZON CHECK
  Consistent output began <when>. <n> months in.
  <whether it is reasonable to expect business results yet>

THE ONE CHANGE
  <single recommendation>

HONEST ASSESSMENT
  <including "not enough data to say" or "this is not working for this LO">
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
> "Is our marketing working?"
> "Review last quarter's content performance."
> "Was the VA campaign worth it?"

## Related skills
- `campaign-builder` — defined the measurement
- `marketing-accountability` — output tracking
- `lo-marketing-coach` — acts on the finding
- `tl-monthly-review` — the wider business picture

## What this skill must not assume
- **Do not assume engagement equals business.** They correlate weakly.
- **Do not attribute a loan to content** without a stated attribution path.
- **Do not judge content marketing on a short horizon.**
- **Do not invent a reason something performed.** Say the cause is unclear.
- **Do not assume more content is the answer** — it often is not.
- **Do not assume the data is complete.** State what is missing.

## Tests
- States available and missing data before concluding.
- Separates output / reach / engagement / conversations / business.
- Applies a horizon check before judging.
- Recommends exactly one change.
- Willing to conclude 'not enough data' or 'not working'.
