---
name: closing-disclosure-review
description: "Read a Closing Disclosure and compare it against the Loan Estimate to surface differences that need review."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [mortgage, documents, closing-disclosure, disclosure, local]
---

# Closing Disclosure Review

## Purpose
Break down a CD section by section and, when a Loan Estimate is available, produce the
LE-vs-CD comparison that shows what moved and by how much — so a human can apply tolerance
rules to real numbers.

## When Hermes should use it
Use when a Closing Disclosure has been extracted, when comparing a CD against the LE, or when
someone asks why cash to close changed.

## Required information
Extracted Closing Disclosure fields. The Loan Estimate for the same loan, for comparison.
Without the LE, only the breakdown is possible — say so.

## Tools and commands it may use
```bash
./vendor/hermes-venv/bin/python scripts/local_ai/extract.py <file> --json
python3 scripts/local_ai/privacy.py check "closing disclosure review"
```
Extraction schema: `schemas/closing_disclosure.schema.json`
Local reasoning only, against `127.0.0.1`. Normally invoked by
`local-loan-document-review`, which does the extraction first.

## Workflow
1. Report loan terms and confirm they match what was expected: amount, rate, term, type,
   monthly P&I.
2. Break costs into the CD's own sections — A through D for loan costs, E through I for
   other costs, J for the total. Do not merge them; the section a charge sits in determines
   how it is treated.
3. Walk the cash-to-close calculation line by line so the number is explainable.
4. **When the LE is available, compare section by section** and show the delta on each.
   Report the direction and size of every change.
5. **Flag increases for tolerance review — do not apply the tolerance rules yourself.**
   Which charges fall into zero tolerance, 10% cumulative, or no tolerance depends on the
   charge type, whether the borrower shopped, and whether a valid changed circumstance
   occurred. Those rules are specific, they change, and getting them wrong has real
   consequences. Present the deltas; a human determines whether a cure is owed.
6. Note anything that commonly signals an error: a rate that moved without a lock change,
   a loan amount change, a term change, or seller credits that differ from the contract.

## Expected output
```
CLOSING DISCLOSURE REVIEW — <borrower>, closing <date>

LOAN TERMS
  Amount <v>   Rate <v>   Term <v>   Type <v>   P&I <v>
  Total monthly payment <v>

COSTS
  A Origination            <v>
  B Cannot shop            <v>
  C Did shop               <v>
  D TOTAL LOAN COSTS       <v>
  E Taxes/government       <v>
  F Prepaids               <v>
  G Initial escrow         <v>
  H Other                  <v>
  I TOTAL OTHER COSTS      <v>
  J TOTAL CLOSING COSTS    <v>
  Lender credits           <v>

CASH TO CLOSE
  <line by line, ending at the final figure>

LE vs CD COMPARISON   (when the Loan Estimate is supplied)
  <section>        LE <v>    CD <v>    change <v>   <up/down>

CHANGES FOR TOLERANCE REVIEW
  - <charge> increased <v> — <requires a human to apply tolerance rules and
    determine whether a changed circumstance applies>

COMMON ERROR SIGNALS
  - <rate moved without a lock change / loan amount differs / term differs /
    seller credits differ from contract>

Tolerance and cure determinations are made by a human. This shows what moved.
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
> "Compare this Closing Disclosure to the Loan Estimate."
> "Why did cash to close change?"
> "Anything on this CD look wrong?"

## Related skills
- `loan-estimate-review` — the other half of the comparison
- `local-loan-document-review` — extracts the fields
- `purchase-contract-review` — for seller credits and price agreement
- `tl-guideline-research` — for current tolerance rules

## What this skill must not assume
- **Do not apply tolerance rules or declare a cure is owed.** The categories depend on
  charge type, shopping, and changed circumstances, and the rules change. Show the deltas.
- **Do not assume an increase is a violation.** A valid changed circumstance permits many.
- **Do not assume the CD is final** — revised CDs are common.
- **Do not compare against a stale LE.** Confirm you have the most recent one.
- **Do not assume the borrower understands the sections.** Explain plainly.

## Tests
- Never applies tolerance rules or declares a cure owed.
- Keeps CD sections separate.
- Cash to close is walked line by line.
- LE comparison shows a per-section delta when the LE is supplied.
- States when only a breakdown is possible without the LE.
