---
name: tl-automation-advisor
description: "Identify what the Team Leader should automate, and write it up as a spec-compliant automation card."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [team-leader, automation, ai, leverage, workflow]
---

# Automation Advisor

## Purpose
Find the repetitive work eating the leader's week and convert it into a properly specified
automation — or say plainly that it should stay manual. Recommending automation for things
that should not be automated is the failure mode to avoid.

## When Hermes should use it
Use when the Team Leader describes repetitive work, asks whether to automate something,
or when another skill surfaces a repeated task.
## Required information
- What the leader describes doing repeatedly
- Findings from `tl-weekly-review`
- `config/integrations.yaml` — what is actually connected
- `automations/schema.md` — the required card format
- `automations/catalog.yaml` — what already exists, so you do not duplicate

## Tools and commands it may use
Reading the repository and configuration. Drafting automation cards.
**Never creating, scheduling, or activating anything.**

## Safety boundaries
Read-only. Automations you write are inactive by definition.

## Human approval requirements
The leader creates and activates. You never do. `cron_mode: deny` in the Hermes profile
enforces this at the runtime level too.

## Workflow
1. Qualify the task honestly:
   - How often? (below weekly, it is usually not worth automating)
   - How long each time?
   - Is the input structured and available?
   - Does it end in a decision a human must make?
2. **Check the catalog first.** If an existing automation covers it, point there.
3. Classify:
   - **Automate** — repetitive, structured input, output is a draft or a report
   - **Assist** — the leader still runs it, the agent prepares it
   - **Keep manual** — judgment-heavy, low frequency, or the thinking *is* the value
   Say which and why. "Keep manual" is a legitimate and often correct answer.
4. Check `config/integrations.yaml`. If the required data source is `placeholder`, say the
   automation cannot run yet and specify what would need to be built.
5. Write the card against `automations/schema.md` — all required fields.
6. Set `active: false` and `approval_required: true` for anything that produces outward
   effects. Never propose auto-send.
7. Estimate the time saved per month, and be conservative.

## Evidence rules
Time-saved estimates state their arithmetic ("15 min × 5×/week = 5 hrs/month"). Never claim
a capability the integrations config does not support.

## Expected output
```
AUTOMATION ASSESSMENT — <task>

QUALIFY
Frequency: <N>/week | Time each: <N>m | Input: <structured? available?>
Ends in a human decision: <yes/no>

ALREADY COVERED?
<existing automation id, or "no">

VERDICT: <AUTOMATE | ASSIST | KEEP MANUAL>
<why, in two sentences>

BLOCKED BY
<any placeholder integration this needs, or "nothing">

TIME SAVED
<the arithmetic> ≈ <N> hrs/month

--- AUTOMATION CARD ---
<full card per automations/schema.md, active: false>
```

## Stop conditions
Stop and recommend against automation if the proposal would: send borrower or partner
communication without review; modify CRM/LOS records; publish content; or make any
lending-related determination.

## Error behavior
If the frequency or time cost is unknown, ask for those two numbers. They determine the
entire recommendation.

## Related skills
- `tl-weekly-review` — surfaces automation candidates
- the marketing automations in `automations/catalog.yaml`
- every automation in `automations/catalog.yaml`

## What this skill must not assume
- **Do not assume automation is the answer.** 'Keep it manual' is often correct.
- **Do not assume an integration exists.** Check `config/integrations.yaml`.
- **Do not assume the leader wants to maintain it.**
- **Do not assume time saved is time recovered** — automations carry upkeep.

## Tests
- Returns KEEP MANUAL when appropriate — it is not an automation salesman.
- Checks the existing catalog before proposing new.
- Every card is `active: false`.
- Refuses auto-send proposals.
- Names blocking placeholder integrations.
