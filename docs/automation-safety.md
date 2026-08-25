# Automation safety

Read this before activating anything from the automation library.

## The pattern

> **The agent prepares → you review → you approve → the system executes.**

Every automation that could have an outward effect follows it. That is not a default you
can casually flip; it is the design.

## Everything ships inactive

All 35 automations in `automations/catalog.yaml` have `active: false`. The library is a
catalog of things you *could* set up, not a set of running jobs. Most need no setup at
all — copy the `prompt` field into a conversation and you are done.

`scripts/validate.py` fails if any catalog entry is `active: true`.

## What the agent will never do on its own

- Send email, SMS, or any message to anyone
- Contact a borrower, Realtor, candidate, or team member
- Modify a CRM or LOS record
- Publish or post content
- Create or activate a scheduled job
- Spend money
- Make a lending, credit, pricing, underwriting, or eligibility decision

The last one is never available, at any setting. The rest require your explicit approval
each time.

This is enforced in three places: the instructions in `AGENTS.md`, the `approvals.mode:
manual` and `cron_mode: deny` settings in the Hermes profile, and the disabled toolsets.

## Prefer automations that prepare

An automation that *drafts* your Monday agenda is safe: worst case you delete it. An
automation that *sends* your team a message is not: worst case it is already sent.

Be enthusiastic about the first kind and reluctant about the second. The
`tl-automation-advisor` skill is built to tell you when something should stay manual, and
"keep it manual" is a legitimate answer it will give.

## Failure behavior

Automations **fail closed**: on error they produce nothing, write a local note, and do not
retry an external action. A partial send is worse than no send.

They also never fill gaps by guessing. If the data is stale or missing, the automation says
so and omits the conclusion.

## Before you activate one

1. Read the whole card, especially `privacy` and `approval_required`
2. Run it manually a few times by pasting the prompt — see what it actually produces
3. Confirm the data source exists (`config/integrations.yaml`; most are `placeholder`)
4. Only then consider a schedule
5. Know how to turn it off — every card has `stop_control`

## Privacy

Every card declares what sensitive data it touches. Pipeline exports contain borrower
names and loan detail — the single most sensitive input in the system. They belong in
`team-data/` or `local_data/`, never in a tracked folder.

For borrower *documents*, see [local-ai/privacy-mode.md](local-ai/privacy-mode.md), where
LOCAL_REQUIRED routing applies and there is no cloud fallback.
