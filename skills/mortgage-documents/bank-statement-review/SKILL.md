---
name: bank-statement-review
description: "Interpret an extracted bank statement: large deposits, sourcing questions, recurring debits, and missing pages."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [mortgage, documents, assets, bank-statement, local]
---

# Bank Statement Review

## Purpose
Surface the things on a bank statement that reliably create underwriting conditions: deposits
that need sourcing, recurring debits that suggest undisclosed debt, NSF activity, and missing pages.

## When Hermes should use it
Use when a bank or asset statement has been extracted and the Team Leader wants to know what
will come back as a condition.

## Required information
Extracted bank statement fields, ideally for consecutive months so gaps are visible.

## Tools and commands it may use
```bash
./vendor/hermes-venv/bin/python scripts/local_ai/extract.py <file> --json
python3 scripts/local_ai/privacy.py check "bank statement review"
```
Extraction schema: `schemas/bank_statement.schema.json`
Local reasoning only, against `127.0.0.1`. Normally invoked by
`local-loan-document-review`, which does the extraction first.

## Workflow
1. Confirm the statement period and check for **missing pages** — "Page 3 of 5" with only
   three pages present is one of the most common and most avoidable delays.
2. Identify **payroll deposits** (regular, same source, consistent amount) and separate them
   from everything else.
3. Flag **large non-payroll deposits**. Say why each is flagged and what documentation would
   normally answer it. Do not declare it unacceptable — sourcing is an underwriting decision.
4. Identify **recurring debits** that look like debt service and do not obviously match a
   known obligation. These are possible undisclosed debts and are worth asking about early.
5. Note **NSF or overdraft** activity if visible.
6. Report beginning, ending, and average balances.

## Expected output
```
BANK STATEMENT REVIEW — <institution>, <period>

BALANCES
  Beginning <v>   Ending <v>   Average <v>

PAYROLL DEPOSITS
  <date> <amount> <description>

LARGE NON-PAYROLL DEPOSITS  (likely to need sourcing)
  <date> <amount> <description>
    Why flagged: <reason>
    Typically documented by: <what usually answers it>

POSSIBLE UNDISCLOSED OBLIGATIONS
  <description> <amount> <frequency> — worth asking the borrower about

MISSING PAGES
  - <evidence>

MUST BE VERIFIED
  - <items>

Sourcing and asset eligibility are underwriting decisions. This is a list of what
an underwriter is likely to ask about.
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
> "What is going to get flagged on this bank statement?"
> "Are there any pages missing here?"

## Related skills
- `local-loan-document-review` — extracts the fields
- `document-set-review` — checks statement continuity across months
- `paystub-review` — matches payroll deposits to pay

## What this skill must not assume
- **Do not assume a large deposit is a problem.** It needs sourcing; that is routine.
- **Do not assume a recurring debit is an undisclosed debt.** It may be insurance, a
  subscription, or a transfer. It is a question to ask.
- **Do not conclude assets are or are not sufficient.** That is underwriting.
- **Do not assume the statement is complete** unless page numbering confirms it.
- **Do not record the full account number.**

## Tests
- Always checks page continuity.
- Separates payroll from non-payroll deposits.
- Frames sourcing as a question, never a denial.
- Masks the account number.
