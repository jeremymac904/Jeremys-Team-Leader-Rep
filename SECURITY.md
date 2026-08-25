# Security and privacy

This repository is **public**. Everything in it can be read by anyone.

## Never commit

- Borrower documents or any borrower data
- Social Security numbers, credit reports, bank statements, income documents
- Your real team roster — names, emails, phones, NMLS numbers
- Recruiting candidate information
- API keys, tokens, passwords, OAuth credentials, private keys
- Private email or message contents
- Production exports from a CRM or LOS
- Model weights (`.gguf`, `.safetensors`) — they are gigabytes and belong in `local_data/`

## Where private things go

| Directory | Contents | Status |
|---|---|---|
| `team-data/` | Roster, coaching notes, scorecards | gitignored |
| `local_data/` | Borrower documents, models, audit log | gitignored |
| `config/*.yaml` | Your filled-in configuration | gitignored |
| `hermes-home/`, `vendor/` | Hermes runtime, may hold API keys | gitignored |
| `.env` | Secrets | gitignored |

Only `*.example.yaml` templates are committed, and they contain fictional data.

## Three layers of protection

1. **`.gitignore`** blocks the directories above, plus `*.gguf`, `*.safetensors`, `*.csv`,
   `*.xlsx`, `auth.json`, and similar.
2. **`scripts/privacy_scan.py`** scans everything git would commit for credentials, SSNs,
   card numbers, private keys, JWTs, and account numbers.
3. **`tests/run_tests.py`** asserts that the dangerous paths are actually ignored, so a
   future edit to `.gitignore` cannot silently remove the protection.

## Before every commit

```bash
python3 scripts/privacy_scan.py
python3 scripts/validate.py
```

`privacy_scan.py` exits non-zero on a blocking finding. Warnings are usually intentional
examples, but read them.

## Local Privacy Mode

Borrower documents are classified LOCAL_REQUIRED and processed only on your machine. There
is no silent cloud fallback. See [docs/local-ai/privacy-mode.md](docs/local-ai/privacy-mode.md)
for exactly what is and is not enforced — including the explicit statement that this is
application-level routing, not operating-system network isolation.

## If you commit something private

Deleting the file is not enough — it stays in git history and in every clone.

1. Do not push, if you have not already
2. If unpushed: `git reset --soft HEAD~1`, remove the file, commit again
3. If pushed: treat the data as exposed. Rotate every credential involved. For borrower
   data, follow your company's incident procedure — this is likely a reportable event.
4. Rewriting history (`git filter-repo`) helps but does not undo exposure

Prevention is the whole strategy. Run the scan.

## Reporting a vulnerability

Open an issue for non-sensitive problems. For anything involving exposed data, contact the
repository owner directly rather than filing publicly.
