---
name: loan-estimate-review
description: "Read a Loan Estimate, break down costs by section, and compare against another LE or a Closing Disclosure."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [mortgage, documents, loan-estimate, disclosure, local]
---

# Loan Estimate Review

## Purpose
Explain what a Loan Estimate actually says, section by section, and make a like-for-like
comparison possible when a borrower brings a competitor's LE.

## When Hermes should use it
Use when an LE has been extracted, when comparing two LEs, or when comparing an LE against
a Closing Disclosure.

## Required information
Extracted Loan Estimate fields. For a comparison, the second LE or the CD.

## Tools and commands it may use
```bash
./vendor/hermes-venv/bin/python scripts/local_ai/extract.py <file> --json
python3 scripts/local_ai/privacy.py check "loan estimate review"
```
Extraction schema: `schemas/loan_estimate.schema.json`
Local reasoning only, against `127.0.0.1`. Normally invoked by
`local-loan-document-review`, which does the extraction first.

## Workflow
1. Report loan terms: amount, rate, term, type, purpose, and **whether the rate is locked**.
   An unlocked rate makes every cost figure provisional — say so.
2. Break costs into sections A through J as the form does. Do not blend them.
3. Report cash to close and how it is composed.
4. For a comparison: line up the same sections side by side. Differences in
   **loan amount, rate, lock status, and points** explain most apparent cost differences —
   check those before concluding one offer is cheaper.
5. Note where APR and rate diverge and what that generally indicates.

## Expected output
```
LOAN ESTIMATE REVIEW

TERMS
  Amount <v>   Rate <v>   Term <v>   Type <v>   Locked: <yes/no>
  P&I <v>   Total monthly <v>   APR <v>

COSTS
  A Origination        <v>
  B Cannot shop        <v>
  C Can shop           <v>
  D Total loan costs   <v>
  E Taxes/gov          <v>
  F Prepaids           <v>
  G Initial escrow     <v>
  H Other              <v>
  J Total closing      <v>
  Lender credits       <v>
  Cash to close        <v>

COMPARISON   (when a second document is provided)
  <section>   this <v>   other <v>   difference <v>   <note>

BEFORE CONCLUDING ANYTHING
  Compare only at the same loan amount, rate, lock status, and point structure.
  An unlocked rate is not a quote.
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
> "Break down this Loan Estimate."
> "Compare our LE to the one the borrower got from another lender."

## Related skills
- `local-loan-document-review` — extracts the fields
- `closing-disclosure-review` — for LE vs CD
- `tl-guideline-research` — for tolerance rules

## What this skill must not assume
- **Do not declare one offer better.** Report the differences and what makes them
  comparable or not.
- **Do not treat an unlocked rate as a real quote.**
- **Do not state tolerance or re-disclosure rules from memory** — they are specific and
  change. Defer to verification.
- **Do not assume escrow figures are accurate** — they are estimates on this form.
- **Do not produce a borrower-facing quote.** This is internal review.

## Tests
- Always reports lock status and qualifies costs when unlocked.
- Keeps sections A-J separate.
- Comparison output normalizes for amount, rate, lock, and points.
- Never declares a winner.
