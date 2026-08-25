---
name: w2-review
description: "Interpret an extracted W-2 and compare it against paystubs and other years."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [mortgage, documents, income, w2, local]
---

# W-2 Review

## Purpose
Explain what a W-2 shows, and surface the differences between boxes and across years that
normally need an explanation.

## When Hermes should use it
Use when a W-2 has been extracted, or when comparing two years of W-2s, or checking a W-2
against a paystub from the same employer.

## Required information
Extracted W-2 fields. Optionally prior-year W-2s and the current paystub.

## Tools and commands it may use
```bash
./vendor/hermes-venv/bin/python scripts/local_ai/extract.py <file> --json
python3 scripts/local_ai/privacy.py check "w2 review"
```
Extraction schema: `schemas/w2.schema.json`
Local reasoning only, against `127.0.0.1`. Normally invoked by
`local-loan-document-review`, which does the extraction first.

## Workflow
1. Report the core boxes: 1 (wages), 2 (federal withheld), 3 and 5 (SS and Medicare wages).
2. **Compare Box 1 with Boxes 3 and 5.** They differ for ordinary reasons — 401(k) deferrals
   reduce Box 1 but not Box 3/5; pre-tax health premiums reduce all three differently. A gap
   is normal. An unexplained gap is worth asking about. Say which this looks like.
3. Note Box 12 codes, especially D (401k), and Box 13 retirement plan.
4. Across years: report the change in Box 1 and whether it is a rise, a fall, or flat.
   A falling income trend is an underwriting consideration, not a decline.
5. Against a paystub: check the employer name matches exactly and the YTD is plausible.

## Expected output
```
W-2 REVIEW — <employer>, tax year <year>

  Box 1  Wages                  <v>
  Box 3  Social security wages  <v>
  Box 5  Medicare wages         <v>
  Box 2  Federal withheld       <v>

BOX 1 vs BOX 3/5
  Difference: <v> — <likely explanation, or "unexplained, worth asking about">

YEAR OVER YEAR   (when multiple years provided)
  <year>: <v>  ->  <year>: <v>   change: <v> (<pct>)

MUST BE VERIFIED
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
> "Read this W2 and tell me if anything looks unusual."
> "Compare these two years of W2s."

## Related skills
- `local-loan-document-review` — extracts the fields
- `paystub-review`, `income-document-comparison`

## What this skill must not assume
- **Do not assume a Box 1 / Box 3 difference is a problem.** It usually is not.
- **Do not assume the W-2 is the whole income picture.** Self-employment, rental, and
  other income never appear here.
- **Do not calculate qualifying income.**
- **Do not assume declining income disqualifies anyone.** That is an underwriting judgment.

## Tests
- Explains the Box 1 vs Box 3/5 difference rather than flagging it blindly.
- Reports year-over-year direction when given multiple years.
- Refuses to state qualifying income.
