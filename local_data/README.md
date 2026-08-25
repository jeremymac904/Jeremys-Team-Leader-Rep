# local_data — never leaves your computer

Everything in this folder is **gitignored**. It is the one place in this
repository where private material belongs.

| Folder | What goes here |
|---|---|
| `models/` | Downloaded model weights (`.gguf`). Multiple gigabytes. Never committed. |
| `borrower_documents/` | Documents you want reviewed. Paystubs, W2s, bank statements, contracts. **Real borrower data lives here and only here.** |
| `working/` | Intermediate extraction output — page text, rendered images, JSON. |
| `audit/` | Local privacy audit log. Records that a document was processed, never its contents. |

## Why this exists

The repository is public. Borrower documents contain names, Social Security
numbers, account numbers, and income detail. A single committed paystub is a
serious problem that cannot be undone by deleting it later — it stays in git
history and in every clone.

So there are three independent layers of protection:

1. `local_data/**` is gitignored
2. `*.gguf`, `*.safetensors`, and similar are gitignored everywhere
3. `python3 scripts/privacy_scan.py` refuses to pass when it finds an SSN,
   account number, or credential in anything git would commit

## Putting documents in

```bash
cp ~/Downloads/paystub.pdf local_data/borrower_documents/
```

Then ask your agent to review it. With Local Privacy Mode on, the file is read,
extracted, and analyzed entirely on this machine.

Verify that for yourself at any time:

```bash
python3 scripts/local_ai/privacy.py status
```
