---
name: document-set-review
description: "Review a whole file of documents together: what is missing, what conflicts, and what to request."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [mortgage, documents, file-review, comparison, local]
---

# Document Set Review

## Purpose
Look at every document in a file at once and answer two questions the Team Leader actually
asks: what is missing, and what contradicts something else.

## When Hermes should use it
Use when several documents have been extracted for the same borrower, when a file is being
prepared for submission, or when the Team Leader asks what is still outstanding.

## Required information
Extracted fields from every available document, plus the loan type and purpose if known.

## Tools and commands it may use
```bash
./vendor/hermes-venv/bin/python scripts/local_ai/extract.py <file> --json
python3 scripts/local_ai/privacy.py check "document set review"
```

Local reasoning only, against `127.0.0.1`. Normally invoked by
`local-loan-document-review`, which does the extraction first.

## Workflow
1. Inventory what is present, by type and period.
2. **Check continuity**: consecutive bank statement months, consecutive pay periods,
   consecutive W-2 years. Name the specific gaps.
3. **Cross-document conflicts** — check these specifically, because they are the ones that
   surface late and hurt:
   - employer name differs between paystub and W-2
   - property address differs between contract, LE, and appraisal
   - loan amount differs between contract and LE
   - borrower name spelled differently across documents
   - purchase price differs between contract and LE
   - dates that contradict each other
4. **Missing documents**: list what a file of this type normally includes and is absent here.
   Frame it as a checklist to confirm, not a guideline requirement you are certain of.
5. Produce a single prioritized request list the Team Leader can send to the LO.

## Expected output
```
DOCUMENT SET REVIEW — <borrower reference>

PRESENT
  <type>  <period/date>  <source file>

CONTINUITY GAPS
  - <e.g. bank statements: May present, June missing, July present>

CROSS-DOCUMENT CONFLICTS
  - <field>: <doc A> says <v>, <doc B> says <v>   -> <what to check>

APPARENTLY MISSING
  - <document> — commonly needed; confirm against this file's actual requirements

REQUEST LIST  (prioritized)
  1. <item> — <why it matters / what it unblocks>

This is a completeness and consistency check, not a determination that the file
is or is not ready to submit.
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
> "What am I missing on this file?"
> "Do any of these documents contradict each other?"

## Related skills
- `local-loan-document-review` — extracts each document
- `income-document-comparison` — deeper income cross-check
- `tl-pipeline-review` — turns the request list into pipeline actions

## What this skill must not assume
- **Do not assert a document is required.** Requirements depend on program, AUS findings,
  and the specific file. Present a checklist to confirm, not a rule.
- **Do not assume a conflict is an error** — addresses and names legitimately vary in format.
- **Do not assume the set you were given is the complete file.**
- **Do not declare a file ready to submit.**

## Tests
- Names specific continuity gaps by period.
- Checks the listed cross-document conflicts explicitly.
- Frames missing documents as a checklist, never as a guideline requirement.
- Produces one prioritized request list.
