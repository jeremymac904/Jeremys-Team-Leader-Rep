# Skills

A **skill** is a written procedure the agent follows for a recurring job. Each lives in its
own directory as a `SKILL.md`. There is no code — a skill is structured instructions, which
is why you can read and edit them without being a programmer.

This format follows the Hermes Agent skill convention. Hermes loads these **directly from
this repository** via `skills.external_dirs`, so a `git pull` updates them and editing one
takes effect on the next run. Nothing is copied. See [../docs/hermes.md](../../docs/hermes.md).

Confirm they loaded:
```bash
hermes skills list
```

## Team leadership (14)

| Skill | Use it when |
|---|---|
| [`tl-morning-brief`](team-leadership/tl-morning-brief/SKILL.md) | Starting the day — what needs you today |
| [`tl-pipeline-review`](team-leadership/tl-pipeline-review/SKILL.md) | Stalled files, slipping closings, silent borrowers |
| [`tl-lo-coaching-prep`](team-leadership/tl-lo-coaching-prep/SKILL.md) | Before a one-on-one |
| [`tl-development-plan`](team-leadership/tl-development-plan/SKILL.md) | Ramp, recovery, or growth plan |
| [`tl-team-meeting-prep`](team-leadership/tl-team-meeting-prep/SKILL.md) | Building the weekly agenda |
| [`tl-role-play`](team-leadership/tl-role-play/SKILL.md) | Live sales reps with scoring |
| [`tl-recruiting-review`](team-leadership/tl-recruiting-review/SKILL.md) | Candidate pipeline and interviews |
| [`tl-partner-review`](team-leadership/tl-partner-review/SKILL.md) | Realtor relationships gone quiet |
| [`tl-training-plan`](team-leadership/tl-training-plan/SKILL.md) | Choosing the next training topic |
| [`tl-weekly-review`](team-leadership/tl-weekly-review/SKILL.md) | Your own weekly review |
| [`tl-monthly-review`](team-leadership/tl-monthly-review/SKILL.md) | Monthly production, quarterly planning |
| [`tl-automation-advisor`](team-leadership/tl-automation-advisor/SKILL.md) | "Should I automate this?" |
| [`tl-guideline-research`](team-leadership/tl-guideline-research/SKILL.md) | Program questions, with sources |
| [`tl-content-plan`](team-leadership/tl-content-plan/SKILL.md) | Marketing content and scripts |

## Mortgage documents (8)

These run **locally**. Borrower documents are never sent to a cloud model while Local
Privacy Mode is on. See [../docs/local-ai/privacy-mode.md](../../docs/local-ai/privacy-mode.md).

| Skill | Use it when |
|---|---|
| [`local-loan-document-review`](mortgage-documents/local-loan-document-review/SKILL.md) | **Start here** — extracts any mortgage document locally |
| [`paystub-review`](mortgage-documents/paystub-review/SKILL.md) | Income components and YTD consistency |
| [`w2-review`](mortgage-documents/w2-review/SKILL.md) | W-2 boxes and year-over-year |
| [`bank-statement-review`](mortgage-documents/bank-statement-review/SKILL.md) | Large deposits, sourcing, missing pages |
| [`purchase-contract-review`](mortgage-documents/purchase-contract-review/SKILL.md) | Terms, deadlines, financing concerns |
| [`loan-estimate-review`](mortgage-documents/loan-estimate-review/SKILL.md) | Cost breakdown and LE comparison |
| [`income-document-comparison`](mortgage-documents/income-document-comparison/SKILL.md) | Cross-checking income documents |
| [`document-set-review`](mortgage-documents/document-set-review/SKILL.md) | What is missing or contradictory in a file |

## Using one

Ask in plain language — the agent matches your request:

> "Prep my one-on-one with Jordan."
> "Run a pipeline review on this export." *(then paste it)*
> "Review the paystub in local_data/borrower_documents/."

Or name it: *"Use tl-morning-brief."*

## What every skill guarantees

Each `SKILL.md` declares the same sections, and they are the contract:

**Purpose** · **When Hermes should use it** · **Required information** ·
**Tools and commands it may use** · **Workflow** · **Expected output** ·
**Safety boundaries** · **Human approval requirements** · **Related skills** ·
**What this skill must not assume** · **Tests**

Mortgage document skills additionally distinguish **extracted fact** from **potential
issue** from **underwriting consideration** from **recommended verification**, and state
that the agent is not the underwriter.

## Writing your own

```bash
mkdir -p .hermes/skills/team-leadership/tl-my-skill
cp .hermes/skills/team-leadership/tl-morning-brief/SKILL.md skills/team-leadership/tl-my-skill/SKILL.md
# edit the frontmatter name to match the directory, then each section
python3 scripts/validate.py
```

The directory it sits in becomes its category in Hermes. Validation fails if a required
section is missing or the frontmatter name does not match the directory.
