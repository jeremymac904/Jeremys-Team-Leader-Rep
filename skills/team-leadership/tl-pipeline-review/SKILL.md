---
name: tl-pipeline-review
description: "Review a team pipeline for stalls, slipping deadlines, and silent files. Operational only — never a credit or eligibility judgment."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [team-leader, pipeline, operations, weekly]
---

# Team Pipeline Review

## Purpose
Find the files that are quietly going wrong: stalled stages, approaching closing dates,
borrowers or agents who have not been contacted, and preapprovals aging out. This is an
**operational attention** review, not a credit review.

## When Hermes should use it
Use whenever a pipeline export is supplied, before a pipeline meeting, or when the Team
Leader asks which files are at risk.
## Required information
A pipeline export from the leader's LOS or CRM, pasted or saved into `team-data/`.
Useful columns: loan/file ID, assigned LO, stage, days in stage, contract closing date,
last borrower contact date, last agent contact date, outstanding conditions count.

The `borrower_contact_sla_days` standard from `team-data/team.yaml`.

## Tools and commands it may use
Reading provided data. No CRM/LOS writes. No borrower or agent contact.

## Safety boundaries
Pipeline exports frequently contain borrower names and loan detail. Treat the whole input
as confidential. Never write it into a tracked file, an example, or a commit. Refer to
files by ID where possible rather than borrower name.

## Human approval requirements
None to analyze. Any outreach that results is drafted for the leader and sent by a human.

## Workflow
1. Confirm what columns you actually received. Name the ones you are missing.
2. Flag by category, in this order of severity:
   - Contract closing date within 10 days and conditions outstanding
   - Any file past the borrower-contact SLA
   - Stage duration well above the team's own median for that stage
   - Preapprovals aging past the leader's follow-up window
   - Agent-side silence on active purchase files
3. Group by Loan Officer so the leader can hand each list to one person.
4. Separate "this is a process problem" from "this is a person problem."
5. Emit the review.

## Evidence rules
Every flagged file cites the field and value that triggered it ("42 days in Processing vs
team median 11"). No file is flagged on intuition.

## Expected output
```
PIPELINE REVIEW — <date>   |   <N> files reviewed   |   Source: <export name/date>
Columns missing: <list, or "none">

AT RISK NOW
- [<file id>] <LO> — <trigger + value> — <suggested next action>

BY LOAN OFFICER
<LO name>: <count> flagged — <the one pattern>

PATTERN, NOT PEOPLE
<process issues showing up across multiple LOs>

NOT A CREDIT REVIEW
This review looks at process and attention only. It makes no statement about
eligibility, approval likelihood, credit, or pricing.
```

## Stop conditions
Stop if asked to judge whether a file will be approved, to price or quote, to assess credit,
or to contact a borrower or agent.

## Error behavior
If the export lacks the fields needed for a category, skip that category and say which
column would enable it. Do not estimate days-in-stage you were not given.

## Related skills
- `local-loan-document-review` — for the documents behind a flagged file
- `document-set-review` — for what is missing on a file
- `tl-morning-brief` — surfaces the urgent subset

## What this skill must not assume
- **Do not assume a long stage duration is a problem.** Some files legitimately sit.
- **Do not assume missing columns mean missing data** — say which column you needed.
- **Do not assume a stalled file is the LO's fault.**
- **Do not infer approval likelihood from operational data. Ever.**

## Tests
- Refuses to state approval likelihood.
- Names missing columns instead of guessing.
- Output contains the "not a credit review" label.
