---
name: local-loan-document-review
description: "Review a mortgage document entirely on this machine. Routes to the right extraction method and schema, and never sends borrower data to a cloud model."
version: 1.0.0
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [mortgage, documents, local, privacy, extraction, loan-factory]
---

# Local Loan Document Review

## Purpose
Turn a borrower document into structured, verifiable findings **without the document
leaving this computer**. This skill is the front door for every mortgage document
workflow: it decides how to read the file, which schema applies, and which specialist
skill should interpret the result.

## When Hermes should use it
Use this whenever the Team Leader references a borrower document — a paystub, W2, tax
return, bank statement, purchase contract, Loan Estimate, Closing Disclosure, mortgage
statement, insurance or HOA document, or any file in `local_data/borrower_documents/`.

Use it **before** any specialist document skill. Those skills interpret extracted fields;
this skill produces them.

Do not use it for public guideline questions (`tl-guideline-research`) or for anything
with no document involved.

## Required information
- A path to the document, normally under `local_data/borrower_documents/`
- Nothing else. Do not ask the Team Leader to retype figures from the document.

If no path is given, ask for one. Never invent document contents.

## Tools and commands it may use
```bash
# Confirm this workflow must stay local (it will say LOCAL_REQUIRED)
python3 scripts/local_ai/privacy.py check "<document type>"

# Extract locally: native text, then tables, then OCR, then vision
./vendor/hermes-venv/bin/python scripts/local_ai/extract.py <file> --json

# Confirm the local model is up and is on loopback
python3 scripts/local_ai/server.py health
```
Reasoning runs against the local llama.cpp endpoint on `127.0.0.1`. No cloud API.

## Workflow
1. **Check routing first.** Run the privacy check. A borrower document is
   `LOCAL_REQUIRED`. If Local Privacy Mode is off, say so plainly and ask whether to
   continue before doing anything.
2. **Confirm the local model is running.** If it is not, say so and give the start
   command. Do not silently switch to a cloud model — that is the one thing this
   skill exists to prevent.
3. **Extract.** Run the extractor. It reports which method each page used:
   `native` (a real text layer), `ocr` (scanned, read locally by tesseract), or
   `image-only` (needs the local vision model).
4. **Classify.** The extractor proposes a document type and a confidence. If confidence
   is `low` or `none`, say what you think it is and ask before proceeding on that basis.
5. **Select the schema** from `schemas/` matching the document type.
6. **Extract fields against the schema.** Record the page and the verbatim snippet for
   every important value.
7. **Hand off** to the specialist skill for that document type (see Related skills).
8. **Report**, always including what could not be read and what a human must verify.

## Expected output
```
LOCAL DOCUMENT REVIEW — <filename>
Processed entirely on this machine.  Privacy mode: ON

DOCUMENT
  Type       : <type> (confidence: high | moderate | low)
  Pages      : <n>
  Read using : native text / local OCR / local vision
  Model      : <local model> at http://127.0.0.1:<port>

EXTRACTED FIELDS
  <field> : <value>        [page N] "<verbatim snippet>"   confidence: <level>

COULD NOT READ
  - <page or field, and why>

POTENTIAL ISSUES  (observations, not conclusions)
  - <what looks off, and the values that make it look that way>

MUST BE VERIFIED BY A HUMAN
  - <specific items>

NOT AN UNDERWRITING DECISION
This is extracted information and observations. It is not an approval, a denial,
an income calculation, or an eligibility determination.
```

## Safety boundaries
Distinguish these four things explicitly in every response, and never let them blur:

| Category | What it means |
|---|---|
| **Extracted fact** | The document says this. Cite page and snippet. |
| **Potential issue** | Something looks inconsistent. An observation, not a finding. |
| **Underwriting consideration** | Something an underwriter would want to look at. |
| **Recommended verification** | What a human must confirm. |

Never produce a **final lending determination**. You are not the underwriter, the
lender, compliance, title, an attorney, an accountant, the credit bureau, or the insurer.

Additional hard rules:
- Never record a full account number or Social Security number in output. Mask them.
- Never copy a borrower document into a git-tracked directory.
- Never send document text to a cloud model while Local Privacy Mode is on.
- If a local step fails, report the failure. Do not fall back to the cloud. Ever.

## Human approval requirements
- Reading and extracting locally: no approval needed.
- Using a cloud model for any part of this: **explicit approval, every time**, and only
  after showing exactly what would be sent.
- Sending any output to anyone: the Team Leader sends it, not you.

## Examples
> "Review the paystub in local_data/borrower_documents/."

> "What type of document is this and what did you manage to read from it?"

> "This is a scanned bank statement — can you read it without sending it anywhere?"

## Related skills
- `paystub-review`, `w2-review`, `bank-statement-review`, `purchase-contract-review`,
  `loan-estimate-review` — interpret what this skill extracts
- `income-document-comparison` — compares across several extracted documents
- `document-set-review` — checks a whole file for missing or conflicting documents
- `tl-pipeline-review` — turns a finding into an operational next step
- `tl-guideline-research` — for guideline questions raised by a document

## What this skill must not assume
- **Do not assume the extraction is correct.** OCR misreads digits. A `3` becomes an `8`.
  Every dollar amount and date is a candidate for human verification.
- **Do not assume the document is complete.** Statements lose pages; contracts lose addenda.
- **Do not assume the document is genuine.** You cannot detect a forgery, and you must not
  imply that you can.
- **Do not assume a missing field is absent from the file** — it may be on a page that
  failed to extract.
- **Do not assume classification is right** when confidence is low.
- **Do not assume income from a single document.** Qualifying income is an underwriting
  calculation, not an extraction.

## Tests
- Refuses to run when Local Privacy Mode is on and the endpoint is not loopback.
- Reports the extraction method per page.
- Every extracted value carries a page reference.
- Output always contains the "not an underwriting decision" statement.
- Masks account numbers and SSNs.
- On local failure, reports it and stops rather than using a cloud model.
