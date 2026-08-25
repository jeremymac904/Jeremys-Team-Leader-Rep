# Keeping your information private

This repository is **public**. Anyone can read what is committed to it.

## The rule

Private information lives in gitignored directories. Only fictional examples are committed.

| Location | Contents | Committed |
|---|---|---|
| `team-data/` | Your roster, coaching notes, scorecards | **Never** |
| `local_data/` | Borrower documents, model weights, audit log | **Never** |
| `config/*.yaml` | Your filled-in configuration | **Never** |
| `hermes-home/`, `vendor/` | Hermes runtime, may hold API keys | **Never** |
| `.env` | Secrets | **Never** |
| `config/*.example.yaml` | Fictional templates | Yes |
| `examples/synthetic-documents/` | Fictional PDFs | Yes |

## Never put in GitHub

Borrower documents or data · Social Security numbers · credit reports · bank statements ·
income documents · driver licenses · your real roster · recruiting candidate details ·
private emails or messages · API keys, tokens, passwords · production exports · model
weights.

## Three layers of protection

1. **`.gitignore`** blocks those directories, plus `*.gguf`, `*.safetensors`, `*.csv`,
   `*.xlsx`, `auth.json`, and more.
2. **`scripts/privacy_scan.py`** scans everything git would commit for credentials, SSNs,
   card numbers, private keys, JWTs, and account numbers.
3. **`tests/run_tests.py`** asserts those paths are genuinely ignored, so a future
   `.gitignore` edit cannot silently remove the protection.

```bash
python3 scripts/privacy_scan.py
```

Run it before every commit. It exits non-zero on a blocking finding.

## What the agent will not do

- Write private team or borrower information into a tracked file
- Send anything to anyone without your explicit approval
- Send borrower documents to a cloud model while Local Privacy Mode is on
- Echo an API key or `.env` contents

## Careful with pasting

When you paste into a chat with a **cloud** model, that text goes to the provider. Fine for
a pipeline export with file IDs. Not fine for a tax return.

Before pasting to a cloud model, strip: borrower names, SSNs, account numbers, credit data,
and income documents. Team members' first names are usually fine; borrower identities are
not.

For borrower documents, use local review instead — the document never leaves your machine.
See [local-ai/privacy-mode.md](local-ai/privacy-mode.md).

## If something private gets committed

Deleting the file is not enough — git keeps history, and every clone has a copy.

1. If not yet pushed: `git reset --soft HEAD~1`, remove the file, commit again
2. If pushed: treat the data as exposed. Rotate every credential. For borrower data,
   follow your company's incident procedure — it is likely reportable.

See [../SECURITY.md](../SECURITY.md).
