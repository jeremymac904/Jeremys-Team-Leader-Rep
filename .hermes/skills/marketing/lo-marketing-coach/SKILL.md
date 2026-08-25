---
name: lo-marketing-coach
description: "Diagnose a Loan Officer's marketing situation and build a plan they will actually execute, matched to their archetype."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [marketing, coaching, loan-officer, loan-factory]
---

# Loan Officer Marketing Coach

## Purpose
Most Loan Officer marketing advice fails because it is generic. This diagnoses where a
specific LO actually is, then builds a plan sized to what they will really do — which is
usually much smaller than what they say they will do.

## When Hermes should use it
Use when the Team Leader asks about a Loan Officer's marketing, wants a 30-day plan built,
asks why someone is not posting, or wants to review an existing strategy. Prefer this over
general marketing advice whenever a named LO is involved.

## Required information
- The LO's entry in `config/marketing.yaml` — especially `archetype`
- Their roster entry in `team-data/team.yaml` for experience level
- What they are currently doing, if anything
- What they have tried and abandoned, which is usually the most useful input

## Tools and commands it may use
Reads configuration and the shared marketing knowledge. Drafts content. Takes no outward
action — nothing is posted, scheduled, or sent.

Shared knowledge this skill applies:
- `knowledge/marketing/marketing-compliance.md`
- `knowledge/marketing/brand-voice.md`
- `knowledge/marketing/lo-marketing-profiles.md`
- `knowledge/marketing/content-strategy.md`

## Workflow
1. **Identify the archetype.** Read it from `config/marketing.yaml`, or infer it and say
   which you inferred. `knowledge/marketing/lo-marketing-profiles.md` defines all ten and
   what each needs.
2. **Diagnose before prescribing.** Distinguish the three real causes, because the fix
   differs completely:
   - **No system** — they do not know what to post
   - **No time** — they know, but never batch
   - **No comfort** — the format itself is the blocker
3. **Check what they abandoned.** Whatever failed before will fail again unless something
   structural changes. Ask.
4. **Size the plan to reality.** Cut the target until it is trivially achievable, then cut
   it again if they have a history of stopping. Eight consistent weeks at low volume beats
   two strong weeks.
5. **Pick ONE platform and ONE format** to start. Expanding comes later.
6. Apply the content mix — team default, or their override.
7. **Build the batching rhythm.** Deciding what to post daily is what breaks people. One
   batching block per week is the single highest-leverage habit.
8. Define the win condition from their archetype, and say what does not matter yet.

## Expected output
```
MARKETING PLAN — <LO name>
Archetype: <archetype>   Current state: <what they actually do now>

DIAGNOSIS
  Real blocker: <no system | no time | no comfort>
  Evidence: <what points to it>
  What this is NOT: <rule out the wrong fix>
  Previously abandoned: <what and why it failed>

THE PLAN — next 30 days
  Platform: <one>          Format: <one>
  Cadence: <deliberately small>
  Batching: <when, how long>

  Week 1: <specific>
  Week 2: <specific>
  Week 3: <specific>
  Week 4: <specific>

CONTENT MIX
  <pillar> <pct>% — <what that looks like for this person>

WIN CONDITION
  <the one thing that means this worked>

NOT THE GOAL YET
  <what to explicitly ignore for now>

WHAT I OWE THEM
  <the Team Leader's side>
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
> "Build a 30 day marketing plan for Jordan."
> "Review Sam's current marketing strategy."
> "Help Priya become more consistent."

## Related skills
- `tl-lo-coaching-prep` — general coaching; invoke this for the marketing portion
- `content-calendar-builder` — turns this plan into dated content
- `brand-voice-builder` — if their voice is undefined
- `marketing-accountability` — tracks whether the plan happens

## What this skill must not assume
- **Do not assume they will do what they say.** Size to demonstrated behavior.
- **Do not assume video is required.** For a camera-shy LO it is the wrong starting point.
- **Do not assume more platforms is better.** It is the most common cause of collapse.
- **Do not assume the problem is motivation.** It is usually the absence of a system.
- **Do not assume the team mix fits them** — check for an override.
- **Do not assume no content means no marketing.** A partner-driven LO may already market
  effectively offline.

## Tests
- Names the archetype and adapts the plan to it.
- Diagnoses blocker type before prescribing.
- Starts with exactly one platform and one format.
- Includes a batching rhythm.
- States what is explicitly not the goal yet.
