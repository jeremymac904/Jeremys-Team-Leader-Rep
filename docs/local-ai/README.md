# Run your Team Leader AI locally

Plain-English guide. No prior knowledge assumed.

- **[Start here](getting-started.md)** — what local AI is and how to set it up
- **[Hardware and models](hardware-and-models.md)** — what your machine can run
- **[Local Privacy Mode](privacy-mode.md)** — what stays on your computer, and how to prove it
- **[Advanced](advanced.md)** — llama.cpp, GGUF, quantization, context, tuning
- **[Troubleshooting](troubleshooting.md)** — when something does not work

## The short version

Normally when you use AI, your words are sent over the internet to a company's
servers. That is fine for "write me a market update." It is **not** fine for a
borrower's tax return.

**Local AI** runs the model on your own computer. Nothing is sent anywhere. The
tradeoff is that a model small enough to run on a laptop is not as smart as a large
cloud model — so this system uses local AI where privacy matters and lets you use
cloud models where it does not.

## Why a Team Leader should care

Your team handles paystubs, W2s, tax returns, bank statements, and contracts every
day. Those documents contain Social Security numbers, account numbers, and income
detail. Pasting them into a cloud AI tool is a genuine problem — often a policy
violation, sometimes worse.

This gives you a way to use AI on those documents where the document never leaves
your machine.

## What it can actually do

- Read a PDF, including a scanned one, entirely on your computer
- Pull structured fields out of a paystub, W2, bank statement, purchase contract,
  Loan Estimate, Closing Disclosure, or mortgage statement
- Flag what looks inconsistent and what a human must verify
- Compare documents against each other
- Tell you what is missing from a file

## What it will never do

It will not underwrite. It is not the underwriter, the lender, compliance, an
attorney, or an accountant. It extracts information and points at things worth
checking. **Every figure it reports must be verified by a person** before anyone
relies on it.

## Setup in four commands

```bash
brew install llama.cpp
./vendor/hermes-venv/bin/python -m pip install -r requirements-local-ai.txt
./vendor/hermes-venv/bin/python scripts/local_ai/setup_local_ai.py
./vendor/hermes-venv/bin/python scripts/local_ai/server.py start
./vendor/hermes-venv/bin/python scripts/local_ai/review.py examples/synthetic-documents/synthetic-paystub.pdf
```

That last command reviews a fictional paystub that ships with this repository, so
you can see the whole thing work before pointing it at anything real.
