---
name: tax-return-review
description: "Surface the income indicators and add-back candidates in a tax return. Review assistance only — this does not calculate qualifying income."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [mortgage, documents, income, tax-return, self-employed, local]
---

# Tax Return Review Assistance

## Purpose
Read an extracted tax return and point at what an underwriter will look at: which schedules
are present, what income is likely recurring, and which items commonly get added back.
**It does not compute qualifying income** — that is an underwriting determination requiring
methodology this skill deliberately does not apply.

## When Hermes should use it
Use when a tax return has been extracted, when reviewing a self-employed borrower's file, or
when the Team Leader wants to know what a return implies before it reaches underwriting.

## Required information
Extracted tax return fields. Ideally two consecutive years, because trend matters more than
any single year. The business structure if known.

## Tools and commands it may use
```bash
./vendor/hermes-venv/bin/python scripts/local_ai/extract.py <file> --json
python3 scripts/local_ai/privacy.py check "tax return review"
```
Extraction schema: `schemas/tax_return.schema.json`
Local reasoning only, against `127.0.0.1`. Normally invoked by
`local-loan-document-review`, which does the extraction first.

## Workflow
1. Report the year, filing status, and which **schedules are present**. The schedules are
   the story: C means sole proprietorship, E means rental or pass-through, F means farm,
   K-1 means partnership or S-corp.
2. Separate income by **character**, because they are treated very differently:
   - W-2 wages
   - Self-employment (Schedule C)
   - Rental (Schedule E)
   - Capital gains — frequently non-recurring
   - Interest and dividends — often small and variable
3. Flag **likely add-back candidates**: depreciation, amortization, depletion, business use
   of home, and one-time casualty losses. Name them as *candidates for underwriting review*,
   never as amounts you have added back.
4. Flag **losses** that may reduce qualifying income, especially Schedule C or E losses.
5. Across two years, report the direction of each income category. A large swing needs an
   explanation regardless of direction.
6. State clearly what requires underwriting analysis and why.

## Expected output
```
TAX RETURN REVIEW — <taxpayer>, <year>          [REVIEW ASSISTANCE — NOT INCOME CALCULATION]

RETURN
  Filing status <v>   Total income <v>   AGI <v>   Taxable income <v>

SCHEDULES PRESENT
  <schedule> — <what it indicates>

INCOME BY CHARACTER
  W-2 wages        <v>
  Schedule C net   <v>   (gross receipts <v>, expenses <v>)
  Schedule E net   <v>
  Capital gains    <v>   <likely recurring / likely one-time>
  Interest/div     <v>

ADD-BACK CANDIDATES  (for underwriting to evaluate, not applied here)
  Depreciation            <v>
  Business use of home    <v>
  <other>                 <v>

POSSIBLE NON-RECURRING
  - <item and why>

LOSSES THAT MAY REDUCE INCOME
  - <item>

YEAR OVER YEAR   (when two years supplied)
  <category>: <year1> -> <year2>   <direction>   <needs explanation?>

REQUIRES UNDERWRITING ANALYSIS
  - <specific items and why>

This lists indicators. Qualifying income is calculated by underwriting using their
methodology, not here.
```

## Safety boundaries
Label every statement as one of: **extracted fact** (with page and snippet),
**potential issue** (an observation), **underwriting consideration**, or
**recommended verification**. Never issue a final lending determination.

You are not the underwriter, the lender, compliance, title, an attorney, an
accountant, the credit bureau, or the insurer. Say so when the Team Leader asks you
to be one.

Mask account numbers and Social Security numbers. Never write borrower data into a
git-tracked directory. While Local Privacy Mode is on, nothing here reaches a cloud
model, and a local failure is reported rather than worked around.

## Human approval requirements
Local extraction and analysis need no approval. Using a cloud model for any part of
this requires explicit approval, every time, after showing exactly what would be sent.
Any communication to a borrower, agent, or team member is written by a human.

## Examples
> "What does this tax return tell me about their income?"
> "Which add-backs will underwriting look at here?"
> "Compare these two years of returns."

## Related skills
- `local-loan-document-review` — extracts the fields
- `income-document-comparison` — cross-checks against W2s and paystubs
- `document-set-review` — checks whether all required years are present
- `tl-guideline-research` — for how a program treats a given income type

## What this skill must not assume
- **Do not calculate qualifying income.** Different programs use different methodology, and
  getting this wrong sets a borrower's expectations incorrectly. This is the single most
  important boundary in this skill.
- **Do not assume an add-back will be allowed.** It depends on program and documentation.
- **Do not assume Schedule C net profit is usable income** without underwriting review.
- **Do not assume one year represents the trend.**
- **Do not assume the return is complete** — schedules and K-1s are commonly missing.
- **Do not assume a loss disqualifies anyone.**

## Tests
- Never states a qualifying income figure.
- Add-backs are labeled candidates, never applied.
- Separates income by character rather than reporting one total.
- Reports which schedules are present.
- Output carries the review-assistance label.
