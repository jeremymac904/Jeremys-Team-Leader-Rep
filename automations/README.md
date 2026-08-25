# Automation library

46 automations across 10 categories. Every one ships **inactive**.

## How to actually use these

Most of them need no setup at all. Open [`catalog.yaml`](catalog.yaml), find the one you
want, and copy its `prompt` into a conversation with your agent. That is it. The `trigger`
field is a suggestion for when to run it, not something that runs on its own.

When you are ready to put one on a real schedule, read
[`../docs/automation-safety.md`](../docs/automation-safety.md) first. The short version:

> the agent prepares → you review → you approve → the system executes

Nothing in this library sends a message, changes a record, or publishes anything on its own.

To add your own, follow [`schema.md`](schema.md), then run:

```bash
python3 scripts/build_automation_index.py && python3 scripts/validate.py
```

---

## Daily leadership

Running the day instead of reacting to it.

| Automation | What it does | Cadence | Needs approval |
|---|---|---|---|
| `daily-morning-brief` | Start the day knowing the three things that need you, instead of discovering them at 4pm. | Every weekday morning, before the day gets reactive | no |
| `daily-urgent-email-triage` | Separate the three emails that need you from the sixty that do not. | Daily, or whenever the inbox has gotten away from you | yes |
| `daily-quiet-team-check` | Catch the team member who has stopped producing before it becomes a month. | Friday afternoon | no |

## Pipeline

Finding the files that are quietly going wrong.

| Automation | What it does | Cadence | Needs approval |
|---|---|---|---|
| `pipeline-weekly-review` | Find every file that is quietly going wrong before the closing date does it for you. | Weekly, before your pipeline meeting | no |
| `pipeline-closing-deadline-watch` | Never be surprised by a contract closing date. | Daily | no |
| `pipeline-preapproval-followup` | Recover preapproved buyers who went quiet instead of letting them expire. | Weekly | yes |
| `pipeline-deal-rescue` | Find files that are one specific action away from moving again. | Weekly, or when the month looks short | no |

## Loan Officer coaching

Preparing, running, and documenting coaching.

| Automation | What it does | Cadence | Needs approval |
|---|---|---|---|
| `coaching-weekly-prep` | Walk into every one-on-one already knowing the number, the diagnosis, and the drill. | The morning of your coaching day | no |
| `coaching-session-recap` | Document the same day, so next week's session starts from a real record instead of memory. | Immediately after every one-on-one | no |
| `coaching-development-plan` | Give a new hire a real ramp, or a stalling LO a real path, instead of a vague conversation. | As needed | no |
| `coaching-role-play` | Build the skill by saying it out loud, not by discussing it. | Weekly, in the one-on-one or the team meeting | no |
| `coaching-accountability-check` | Hold the standard consistently instead of only when you happen to notice. | Friday, after scorecards are due | no |

## Team meetings

Agendas that teach, and action items that survive.

| Automation | What it does | Cadence | Needs approval |
|---|---|---|---|
| `meeting-weekly-agenda` | Run a meeting that teaches something, instead of a status round-robin. | Friday, for Monday's meeting | no |
| `meeting-recap` | Make action items survive the meeting. | Immediately after | yes |
| `meeting-oneonone-schedule` | Prepare every one-on-one for the week in a single sitting. | Weekly, the morning of your coaching block | no |

## Recruiting

Keeping the candidate pipeline warm before you need it.

| Automation | What it does | Cadence | Needs approval |
|---|---|---|---|
| `recruiting-pipeline-review` | Keep recruiting from only happening after someone quits. | Weekly | no |
| `recruiting-interview-prep` | Interview against your stated profile instead of against your mood that day. | As needed | no |
| `recruiting-onboarding-plan` | Make the first 30 days deliberate so a new hire ramps instead of drifting. | Per hire | no |

## Referral partners

Noticing decay early and bringing real value.

| Automation | What it does | Cadence | Needs approval |
|---|---|---|---|
| `partners-weekly-review` | Notice the agent who stopped referring, in the month it happens rather than the quarter. | Weekly | yes |
| `partners-meeting-prep` | Walk into an agent meeting with something useful instead of a business card. | As needed | no |
| `partners-value-item-plan` | Give every A-tier partner a reason to keep working with you that is not price. | Quarterly | yes |

## Training

Training the gap that costs production.

| Automation | What it does | Cadence | Needs approval |
|---|---|---|---|
| `training-topic-selection` | Train on the gap that is costing production, not on whatever came up. | Weekly, before you plan the next session | no |
| `training-session-build` | Turn a topic into a 25-minute session with a live drill and a takeaway. | Weekly or monthly, matching your training_schedule | no |
| `training-guideline-refresh` | Teach current guidelines instead of remembered ones. | Monthly | no |

## Marketing

Staying visible without inventing content every week.

| Automation | What it does | Cadence | Needs approval |
|---|---|---|---|
| `marketing-content-plan` | Keep the team visible without inventing content every week. | Monthly | yes |
| `marketing-video-script` | Remove the blank-page problem from weekly video. | Weekly | yes |
| `marketing-realtor-education` | Be the lender agents learn from, which is a durable advantage over being the cheapest. | Monthly | yes |
| `marketing-weekly-content-plan` | Decide the week's content once, in one sitting, instead of every morning. | Friday, planning the week ahead | yes |
| `marketing-daily-content-ideas` | Never start from a blank page. | Daily or as needed | yes |
| `marketing-market-news-to-content` | Turn what is happening in the market into teaching content, without making rate claims. | Weekly | yes |
| `marketing-guideline-to-realtor-education` | Turn a program or guideline change into content that makes partners better at their job. | As needed | yes |
| `marketing-content-repurposing` | Stop letting a good recording produce exactly one post. | Whenever a substantial asset is created | yes |
| `marketing-video-script-batch` | Produce a week of scripts in one sitting so filming is one session. | Weekly, before the filming block | yes |
| `marketing-weekly-scorecard` | See who is executing their marketing plan before a month of silence goes unnoticed. | Weekly | no |
| `marketing-team-training-segment` | Give the weekly meeting a marketing segment that teaches something specific. | Weekly, with meeting prep | yes |
| `marketing-campaign-followup` | Make sure campaign responses are actually worked, which is where most campaigns fail. | Weekly during a campaign | yes |
| `marketing-social-post-review` | Catch a compliance problem before it publishes rather than after. | As needed | no |
| `marketing-monthly-performance` | Decide honestly whether the marketing effort is producing anything. | Monthly | no |

## Executive workflows

Reviewing yourself, not only everyone else.

| Automation | What it does | Cadence | Needs approval |
|---|---|---|---|
| `exec-weekly-review` | Review yourself, not only everyone else — including your own production. | Friday afternoon | no |
| `exec-monthly-production-review` | See structure instead of noise: real trajectories, concentration risk, capacity. | Monthly | no |
| `exec-quarterly-planning` | Set three objectives for the quarter that are measurable, instead of a wish list. | Quarterly | no |
| `exec-time-and-delegation-audit` | Find the work you are doing that someone else should own. | Monthly | no |

## AI workflows

Finding leverage and building it safely.

| Automation | What it does | Cadence | Needs approval |
|---|---|---|---|
| `ai-automation-assessment` | Get an honest answer, including 'keep it manual' when that is correct. | Whenever you notice yourself repeating something | no |
| `ai-prompt-builder` | Turn a prompt that worked once into one that works every time. | As needed | no |
| `ai-team-training` | Teach the team to use AI on their own work, so leverage is not bottlenecked on you. | Monthly | no |
| `ai-workflow-audit` | Find where the team's process wastes time or drops files. | Quarterly | no |

---

## Field reference

Every card declares: `id`, `name`, `category`, `objective`, `trigger`, `cadence`,
`data_needed`, `skill`, `prompt`, `output`, `approval_required`, `privacy`, `setup`,
`customization`, `active`, and `time_saved_per_month`. See [`schema.md`](schema.md).

<!-- Generated by scripts/build_automation_index.py — edit catalog.yaml, not this file. -->
