---
name: income-document-comparison
description: "Compare paystubs, W-2s, and tax returns against each other and surface what does not line up."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [mortgage, documents, income, comparison, local]
---

# Income Document Comparison

## Purpose
Cross-check the income documents in a file against each other. Most income problems are found
by comparison, not by reading any single document.

## When Hermes should use it
Use when two or more income documents have been extracted and the Team Leader wants to know
whether the story is consistent.

## Required information
Extracted fields from at least two income documents. More is better.

## Tools and commands it may use
```bash
./vendor/hermes-venv/bin/python scripts/local_ai/extract.py <file> --json
python3 scripts/local_ai/privacy.py check "income document comparison"
```

Local reasoning only, against `127.0.0.1`. Normally invoked by
`local-loan-document-review`, which does the extraction first.

## Workflow
1. Build a table of every income document present: type, employer, period, and gross.
2. Check the **employer name is identical** across documents. A variation ("Northwind LLC"
   vs "Northwind Manufacturing") is usually nothing, occasionally a real employment change.
3. Check **YTD progression** across pay periods — it should only increase.
4. Check the **current paystub YTD against last year's W-2** for a plausible run rate.
5. Check for **gaps**: missing pay periods, a missing W-2 year, an employment gap.
6. Identify the **trend**: rising, flat, or falling, and over what span.
7. State clearly which discrepancies need a borrower explanation and which are routine.

## Expected output
```
INCOME DOCUMENT COMPARISON

DOCUMENTS
  <type>  <employer>  <period>  <gross>

EMPLOYER CONSISTENCY
  <matches exactly / variations found: ...>

YTD PROGRESSION
  <period> <ytd>  ->  <period> <ytd>   <consistent / inconsistent>

RUN RATE vs PRIOR YEAR
  Current YTD <v> over <n> periods implies <v> annualized
  Prior year W-2 Box 1 <v>   — <consistent / differs by ...>

GAPS
  - <missing period or year>

TREND
  <direction> over <span>

NEEDS BORROWER EXPLANATION
  - <specific item and the specific question to ask>

ROUTINE, NO ACTION
  - <items that look odd but usually are not>

Qualifying income is calculated by underwriting, not here.
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
> "Do these income documents tell a consistent story?"
> "Compare the paystub YTD to last year's W2."

## Related skills
- `paystub-review`, `w2-review`, `tax-return-review`
- `document-set-review` — for what is missing entirely
- `local-loan-document-review` — extracts the fields

## What this skill must not assume
- **Do not assume an employer name variation means a job change.**
- **Do not annualize YTD naively.** Raises, bonuses, and unpaid leave all distort it.
  Show the arithmetic and label it an estimate.
- **Do not calculate qualifying income.**
- **Do not assume the documents provided are all that exist.**
- **Do not treat a falling trend as disqualifying.**

## Tests
- Always checks employer name consistency.
- YTD progression is checked in date order.
- Annualization is labelled an estimate and shows its arithmetic.
- Separates 'needs explanation' from 'routine'.
