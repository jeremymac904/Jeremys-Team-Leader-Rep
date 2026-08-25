---
name: purchase-contract-review
description: "Extract contract terms and dates that affect financing, and surface deadlines needing attention."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [mortgage, documents, contract, purchase, local]
---

# Purchase Contract Review

## Purpose
Pull the terms and deadlines out of a purchase contract that determine whether the loan closes
on time, and put the dates in front of the Team Leader before they become emergencies.

## When Hermes should use it
Use when a purchase contract has been extracted, when a new contract comes in, or when the
Team Leader asks what dates are coming up on a file.

## Required information
Extracted purchase contract fields. The current date, to compute days remaining.

## Tools and commands it may use
```bash
./vendor/hermes-venv/bin/python scripts/local_ai/extract.py <file> --json
python3 scripts/local_ai/privacy.py check "purchase contract review"
```
Extraction schema: `schemas/purchase_contract.schema.json`
Local reasoning only, against `127.0.0.1`. Normally invoked by
`local-loan-document-review`, which does the extraction first.

## Workflow
1. Report the parties, property, price, and financing structure.
2. Build the **date timeline**, and for each deadline show days remaining from today.
   Order by urgency, not by where it appeared in the contract.
3. Check **price vs down payment vs loan amount** for internal consistency.
4. Flag **seller concessions** — they are commonly capped by program and occupancy, and
   exceeding the cap is a real problem. Say it needs checking against the specific program;
   do not state the cap from memory.
5. Flag terms that affect financing: short financing contingency, aggressive closing date,
   unusual occupancy, HOA presence, personal property included in price.
6. Note missing signatures or initials.

## Expected output
```
PURCHASE CONTRACT REVIEW — <property>

TERMS
  Buyer <names>   Seller <names>
  Price <v>   Earnest money <v>   Down payment <v>   Loan amount <v>
  Financing <type>   Occupancy <type>   Seller concessions <v>

DATES  (most urgent first)
  <date>  <label>              <n> days from today
  ...

CONSISTENCY
  Price - down payment = <v> vs stated loan amount <v> — <matches / differs>

FINANCING CONCERNS
  - <term> — <why it matters for the loan>

SELLER CONCESSIONS
  <v> = <pct>% of price. Concession limits vary by program and occupancy —
  verify against the actual program guidelines for this file.

MISSING SIGNATURES
  - <items>
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
> "What dates do I need to worry about on this contract?"
> "Is anything in this contract going to cause a financing problem?"

## Related skills
- `local-loan-document-review` — extracts the fields
- `tl-pipeline-review` — puts the deadlines into the pipeline
- `tl-guideline-research` — for the actual concession limits

## What this skill must not assume
- **Do not state a seller concession limit from memory.** Limits vary by program,
  occupancy, and LTV, and they change. Say it must be checked.
- **Do not assume the contract is fully executed** unless signatures are visible.
- **Do not assume all addenda are present.**
- **Do not compute a closing timeline as achievable or not** — that depends on the file.
- **Do not assume the loan amount** when it is not stated.

## Tests
- Dates are ordered by urgency with days remaining.
- Concession limits are always deferred to guideline verification.
- Checks price / down payment / loan amount arithmetic.
- Reports missing signature blocks.
