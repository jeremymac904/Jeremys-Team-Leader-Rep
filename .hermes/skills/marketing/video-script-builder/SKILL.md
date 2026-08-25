---
name: video-script-builder
description: "Write short-form mortgage video scripts, including formats for Loan Officers who will not appear on camera."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [marketing, video, script, content]
---

# Video Script Builder

## Purpose
Turn a mortgage topic into a script that can be filmed today — and when the Loan Officer
is camera-shy, into a format that does not require their face at all.

## When Hermes should use it
Use when a video script or short-form idea is requested, when a calendar entry needs the
actual words, or when an LO wants video but is uncomfortable on camera.

## Required information
- The topic, or a real question the team is being asked
- The audience — buyer, Realtor, investor
- The LO's `comfort_with_video`
- Target length, default 30–60 seconds

## Tools and commands it may use
Reads configuration and the shared marketing knowledge. Drafts content. Takes no outward
action — nothing is posted, scheduled, or sent.

Shared knowledge this skill applies:
- `knowledge/marketing/marketing-compliance.md`
- `knowledge/marketing/brand-voice.md`
- `knowledge/marketing/video-frameworks.md`
- `knowledge/marketing/cta-system.md`

## Workflow
1. **Check comfort first.** If `comfort_with_video` is low, offer the no-face formats from
   `video-frameworks.md` before writing a talking-head script — screen recording, text on
   B-roll, audio-first, or carousel instead. Do not push past discomfort; it produces nothing.
2. Pick one framework: myth-to-fact, mistake-to-fix, Realtor advisory, scenario review, or
   document prep.
3. Write the hook to name a **specific** mortgage problem. Generic hooks are the main reason
   these fail.
4. Follow hook → context → lesson → CTA. One point only.
5. Write for **speech**: short sentences, contractions, no clause stacking. Read it aloud
   mentally — if it needs a breath mid-sentence, cut it.
6. Add the on-screen text and B-roll notes.
7. Attach the caption with the configured disclosure when the topic touches options,
   qualification, programs, pre-approval, application, or payment planning.

## Expected output
```
VIDEO SCRIPT — <topic>
Audience: <who>   Length: ~<n>s   Framework: <which>
Format: <talking head | screen recording | text + B-roll | audio-first>
  <if not talking head: why this format was chosen for this LO>

SCRIPT
  [HOOK ~3s]      "<exact words>"
  [CONTEXT ~10s]  "<exact words>"
  [LESSON ~25s]   "<exact words>"
  [CTA ~7s]       "<exact words>"

ON SCREEN
  0:00 <text>   0:05 <text>

B-ROLL / VISUAL
  - <shot or screen>

CAPTION
  <caption text>
  <configured disclosure>

CATEGORY: <educational | general marketing | loan program marketing>
COMPLIANCE FLAGS: <items, or none>
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
> "Create a video script for a Loan Officer who hates being on camera."
> "Write a 45 second script on why pre-approvals fail."
> "Turn this question into a reel."

## Related skills
- `content-calendar-builder` — schedules the script
- `content-repurposing` — the script becomes other formats
- `social-content-strategist` — platform formatting

## What this skill must not assume
- **Do not assume the LO will appear on camera.** Check comfort.
- **Do not assume longer is better.** 30 focused seconds beats three rambling minutes.
- **Do not write for reading.** Scripts are spoken; the rhythm differs.
- **Do not include a rate or payment figure.**
- **Do not assume the hook works** — if it does not name a specific problem, rewrite it.

## Tests
- Offers no-face formats when comfort_with_video is low.
- Hook names a specific mortgage problem.
- Script is written for speech.
- Caption includes the configured disclosure when required.
- Exactly one teaching point.
