---
name: mortgage-statement-review
description: "Read a mortgage statement for payoff, escrow, and payment-history context."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [mortgage, documents, servicing, refinance, local]
---

# Mortgage Statement Review

## Purpose
Pull the servicing facts that matter on a refinance or a departing-residence file: balance,
rate, escrow, payment composition, and whether anything is past due.

## When Hermes should use it
Use when a mortgage statement has been extracted — typically on a refinance, when qualifying
someone who is keeping a departing residence, or when verifying an existing obligation.

## Required information
Extracted mortgage statement fields. The purpose — refinance, departing residence, or
liability verification — because it changes what matters.

## Tools and commands it may use
```bash
./vendor/hermes-venv/bin/python scripts/local_ai/extract.py <file> --json
python3 scripts/local_ai/privacy.py check "mortgage statement review"
```
Extraction schema: `schemas/mortgage_statement.schema.json`
Local reasoning only, against `127.0.0.1`. Normally invoked by
`local-loan-document-review`, which does the extraction first.

## Workflow
1. Report servicer, balance, rate, and payment due date.
2. Break the payment into **principal, interest, and escrow**. This matters because the
   escrow portion is not part of the debt obligation in the same way, and the full payment
   including taxes and insurance is what counts for a departing residence.
3. Flag **past due amounts or late fees** — mortgage lates are significant and need
   explanation early, not at underwriting.
4. Report the **escrow balance** and note that an escrow shortage or surplus affects cash to
   close on a refinance.
5. Note that the statement balance is **not a payoff figure**. A payoff includes per-diem
   interest and fees and must come from the servicer.
6. For a departing residence, note what else is needed to confirm the full housing payment —
   taxes, insurance, and HOA if not escrowed.

## Expected output
```
MORTGAGE STATEMENT REVIEW — <servicer>

BALANCE AND TERMS
  Principal balance <v>   Rate <v>   Statement date <v>   Due date <v>

PAYMENT COMPOSITION
  Principal <v>   Interest <v>   Escrow <v>   Total <v>

ESCROW
  Balance <v>   <note on shortage/surplus affecting a refinance>

PAST DUE / LATE FEES
  <amounts, or none shown>
  <if present: mortgage lates need explanation early>

FOR A DEPARTING RESIDENCE
  Full housing payment also requires: <taxes / insurance / HOA if not escrowed>

NOT A PAYOFF
  The balance shown is not a payoff figure. A payoff includes per-diem interest
  and fees and must be requested from the servicer.
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
> "Read this mortgage statement."
> "What do I need for the departing residence?"
> "Is there anything past due here?"

## Related skills
- `local-loan-document-review` — extracts the fields
- `document-set-review` — what else the file needs
- `bank-statement-review` — to match the payment against the debit

## What this skill must not assume
- **Do not treat the balance as a payoff.** It is not, and using it as one causes real
  closing problems.
- **Do not assume taxes and insurance are escrowed.** Many loans are not escrowed.
- **Do not assume no lates shown means none occurred** — a single statement shows one period.
- **Do not assume the rate is fixed** unless stated.
- **Do not calculate a debt-to-income figure.** That is underwriting.

## Tests
- Always states the balance is not a payoff.
- Breaks the payment into principal, interest, and escrow.
- Flags past due amounts prominently.
- Names what else is needed for a departing residence.
