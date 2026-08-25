# Local Privacy Mode

The most important feature in the local AI stack. It is on by default.

## What it does

When Local Privacy Mode is on, anything classified **LOCAL REQUIRED** must be
processed entirely on your computer. There is **no silent cloud fallback**. If a
local step fails, the system tells you what failed and stops. It does not quietly
send your document somewhere else to finish the job.

## The four routing categories

| Category | What it covers | Behavior |
|---|---|---|
| **LOCAL REQUIRED** | Borrower documents, credit, income, assets, applications, anything with a borrower name, SSN, or account number | Never leaves this machine |
| **LOCAL PREFERRED** | Internal team documents, coaching notes, production reviews, candidate notes | Local when available; you are asked before any cloud use |
| **CLOUD ACCEPTABLE** | Public guideline research, training creation, marketing, market research | Cloud is fine — no private data involved |
| **HYBRID** | Extract and redact locally, show you exactly what would be sent, then optionally use a stronger cloud model | Off by default; approval can never be disabled |

Edit these in `config/local-ai.yaml`.

## It fails closed

If the system cannot tell what a workflow is, it treats it as LOCAL REQUIRED while
privacy mode is on. Guessing wrong in the permissive direction means a tax return
goes to a cloud API. Guessing wrong in the restrictive direction means you get asked
a question. Only one of those is recoverable.

## Check anything

```bash
python3 scripts/local_ai/privacy.py status
python3 scripts/local_ai/privacy.py check "bank statement"      # LOCAL_REQUIRED
python3 scripts/local_ai/privacy.py check "marketing content"   # CLOUD_ACCEPTABLE
```

## What happens when a local step fails

You get this, and nothing else happens:

```
LOCAL STEP FAILED: local model inference
  The local model server is not running.

Local Privacy Mode is on, so nothing was sent anywhere. This document has
not left your computer.

Your options:
  1. Fix the local problem and retry
  2. Do this step by hand
  3. Explicitly approve a cloud model for THIS document only — which means
     its contents leave your computer

Nothing happens until you choose. There is no automatic fallback.
```

## Turning it off

```bash
python3 scripts/local_ai/privacy.py off
```

You will get a warning. Think carefully — with it off, borrower documents may be sent
to cloud models. Turn it back on with `privacy.py on`.

## What this guarantees, and what it does not

This is an honest description. Please read it.

**What is enforced:**

- The code will not call a cloud endpoint for a LOCAL REQUIRED workflow
- The inference endpoint is checked and must resolve to loopback (`127.0.0.1`, `::1`,
  or `localhost`) before any document text is sent to it
- Document extraction — PDF parsing, table extraction, OCR — makes no network calls at
  all, by construction
- llama-server binds to loopback only, so it is not reachable from your network
- A local failure stops the pipeline instead of falling back

**What is NOT enforced:**

This is **application-level** routing, not operating-system network isolation. This
system does not install firewall rules, and it cannot stop *other* software on your
computer from using the network. If you separately configure Hermes to use a cloud
model and then paste document text into a chat yourself, nothing here prevents that.

A hardened offline mode — firewall rules or a network namespace that make outbound
connections impossible during local review — is a **future enhancement**. It does not
exist yet, and this system does not claim otherwise.

## Verifying it yourself

The strongest check available to you costs nothing:

1. Start the local model
2. Turn off wi-fi
3. Run a document review

If it completes, inference was local. That is real proof, not a promise.

You can also watch the audit log, which records that a document was processed and
where inference went — never the contents:

```bash
cat local_data/audit/privacy-audit.jsonl
```
