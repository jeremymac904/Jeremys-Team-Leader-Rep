---
name: tl-guideline-research
description: "Research mortgage program, product, or guideline questions with sources and dates. Education only — never an eligibility determination."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [team-leader, mortgage, research, education, compliance]
---

# Mortgage Guideline Research

## Purpose
Answer product and program questions for training and internal education, with the source
and the date attached — so the team learns from current information instead of from
whatever the agent remembers.

## When Hermes should use it
Use for any mortgage program, product, or guideline question asked for education or
training. Never for a live borrower file.
## Required information
- The question, the program (Conventional / FHA / VA / USDA / Non-QM / etc.), and whether
  it is for training or a live scenario
- `mortgage_specialties` from `config/team-leader.yaml`

## Tools and commands it may use
Public research where available. Reading approved internal knowledge in
`coaching/` and `team-data/`. **No pricing engine, no AUS, no LOS, no borrower record.**

## Safety boundaries
Public and approved internal sources only. If borrower specifics enter the question, stop —
see Stop conditions.

## Human approval requirements
None to research. Distributing the result as team training material is the leader's call.

## Workflow
1. Determine whether this is **general education** or a **live file question**. If it is a
   live file, stop and route it to the actual underwriter or the AUS.
2. Prefer primary sources: the agency selling guide, the handbook, the lender's own
   published overlay documentation. Secondary commentary is labeled as such.
3. Record source name, publication or revision date, and the date you retrieved it.
4. Distinguish **agency guideline** from **investor overlay** from **your lender's rule**.
   These are constantly confused and the distinction changes the answer.
5. State the general rule, then the common exceptions, then what is fact-specific.
6. Attach the verification note. Always.

## Evidence rules
Every factual statement carries source + date. Anything you cannot source is labeled
"unverified — check before relying on this." Never present recalled knowledge as current.

## Expected output
```
GUIDELINE RESEARCH — <question>          [EDUCATION — NOT AN ELIGIBILITY DETERMINATION]

SHORT ANSWER
<the general rule>

LAYER
Agency guideline: ...
Investor overlay: ...
Lender-specific:  <varies — check yours>

COMMON EXCEPTIONS
- ...

WHAT MAKES THIS FACT-SPECIFIC
<the variables that change the answer>

SOURCES
- <name> — <revision date> — retrieved <date> — <url if available>

⚠ VERIFY BEFORE ACTING
Guidelines and overlays change. Confirm against the current source and your lender's
own guidance before applying this to a file. This is education, not an underwriting
decision, and not a commitment to lend.
```

## Stop conditions
Stop immediately and route to a human if the question involves: a specific borrower's
credit, income, assets, or property; whether a specific file will be approved; a rate, fee,
or pricing quote; or drafting a disclosure or a denial.

## Error behavior
If you cannot find an authoritative current source, say so and name where to look. Do not
answer from memory and do not estimate. An unsourced guideline answer is worse than no
answer.

## Related skills
- `tl-training-plan` — turns research into a session
- `purchase-contract-review`, `loan-estimate-review` — raise guideline questions
- `local-loan-document-review` — for the document itself

## What this skill must not assume
- **Do not assume recalled guideline knowledge is current.** It changes constantly.
- **Do not assume agency guideline equals investor overlay equals lender rule.**
- **Do not assume a general rule applies to a specific file.**
- **Do not answer a borrower-specific eligibility question at all.** Route it to underwriting.

## Tests
- Output always carries the education label and the verification warning.
- Every factual claim has a source and a date.
- Separates agency / overlay / lender layers.
- Refuses borrower-specific eligibility questions.
