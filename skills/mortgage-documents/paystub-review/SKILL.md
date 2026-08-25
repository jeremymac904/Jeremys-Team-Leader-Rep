---
name: paystub-review
description: "Interpret an extracted paystub: income components, YTD consistency, and what a human must verify."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [mortgage, documents, income, paystub, local]
---

# Paystub Review

## Purpose
Read an extracted paystub and explain what it shows about income — base, overtime, bonus,
commission — and where the numbers do not agree with each other.

## When Hermes should use it
Use when a paystub has been extracted and the Team Leader wants to understand the income
picture, or is comparing it against a W2 or another pay period.

## Required information
The extracted paystub fields from `local-loan-document-review`. Optionally a prior
paystub or the W2 for the same employer.

## Tools and commands it may use
```bash
./vendor/hermes-venv/bin/python scripts/local_ai/extract.py <file> --json
python3 scripts/local_ai/privacy.py check "paystub review"
```
Extraction schema: `schemas/paystub.schema.json`
Local reasoning only, against `127.0.0.1`. Normally invoked by
`local-loan-document-review`, which does the extraction first.

## Workflow
1. Confirm you have pay period dates, pay date, and pay frequency. Without frequency you
   cannot reason about YTD at all — say so instead of guessing.
2. Separate income into **base**, **overtime**, **bonus**, **commission**, **other**.
   These are treated very differently in underwriting; never merge them.
3. Check internal consistency:
   - hourly rate x hours vs base pay for the period
   - gross minus deductions vs net
   - YTD gross vs (per-period gross x periods elapsed in the year)
4. Flag anything that does not reconcile, showing the arithmetic.
5. Note deductions that may indicate an **undisclosed debt** — a loan repayment,
   a garnishment, a child support order.
6. List what a human must verify.

## Expected output
```
PAYSTUB REVIEW — <employee>, period ending <date>

INCOME COMPONENTS          CURRENT        YTD
  Base                     <v>            <v>
  Overtime                 <v>            <v>
  Bonus / Commission       <v>            <v>
  Gross                    <v>            <v>

CONSISTENCY CHECKS
  <check> : <pass / does not reconcile> — <the arithmetic>

POSSIBLE UNDISCLOSED OBLIGATIONS
  - <deduction line> — <why it is worth asking about>

MUST BE VERIFIED
  - <items>

This is not an income calculation. Qualifying income is determined by underwriting.
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
> "What does this paystub show, and does the YTD make sense?"
> "Compare this paystub to the one from two weeks ago."

## Related skills
- `local-loan-document-review` — extracts the fields
- `income-document-comparison` — compares against W2s and other periods
- `w2-review`, `bank-statement-review`

## What this skill must not assume
- **Do not assume YTD is arithmetically clean.** Mid-year raises, unpaid leave, and
  employer changes all break the simple multiplication. A mismatch is a question, not a finding.
- **Do not assume overtime or bonus will continue.** Continuity is an underwriting judgment
  requiring history you do not have.
- **Do not calculate qualifying income.** That is underwriting.
- **Do not assume the pay frequency** if it is not printed. Ask.
- **Do not assume OCR read the digits correctly.**

## Tests
- Separates base / overtime / bonus / commission rather than reporting one gross figure.
- Shows the arithmetic for every consistency check.
- Refuses to state qualifying income.
- Flags deduction lines that may be undisclosed debts.
