# Getting started with local AI

## What you need

- A Mac with Apple Silicon (M1 or newer), a Windows PC, or Linux
- **At least 8 GB of memory.** 16 GB is the comfortable minimum; 24 GB is better
- Roughly 15 GB of free disk space
- An internet connection **for setup only** — once the model is downloaded, document
  review works with the internet off

## Step 1 — install the engine

The engine is the program that runs the model. We use **llama.cpp**, which is fast on
Apple Silicon and does not phone home.

**macOS**
```bash
brew install llama.cpp
```
If you do not have Homebrew, install it from [brew.sh](https://brew.sh) first.

**Windows**
```
winget install llama.cpp
```
Or download a release from the llama.cpp GitHub releases page and add it to your PATH.

**Linux** — see [advanced.md](advanced.md).

Check it worked:
```bash
llama-server --version
```

Install the local document-processing components:
```bash
./vendor/hermes-venv/bin/python -m pip install -r requirements-local-ai.txt
```

They provide PDF text extraction, page rendering, OCR support, tables, Word, and Excel
file extraction. They install into the private Hermes environment created by
`bash scripts/install_hermes.sh`; use that same Python for the commands below.

## Step 2 — run setup

```bash
./vendor/hermes-venv/bin/python scripts/local_ai/setup_local_ai.py
```

It will:

1. Look at your computer — operating system, memory, and whether you have Apple
   Silicon or a GPU
2. Pick the right model size for your machine and explain why
3. Show you the download size and **ask before downloading anything**
4. Download the model to `local_data/models/` (never committed to GitHub)
5. Write your configuration

Want to see the plan without downloading? Add `--dry-run`.

## Step 3 — start the model

```bash
./vendor/hermes-venv/bin/python scripts/local_ai/server.py start
```

The first start takes a minute or two while the model loads into memory. After that
it stays running until you stop it.

Check it:
```bash
./vendor/hermes-venv/bin/python scripts/local_ai/server.py health
./vendor/hermes-venv/bin/python scripts/local_ai/server.py test
```

## Step 4 — review a fictional document

Seven fictional documents ship with this repository. Nothing real, nothing private.

```bash
./vendor/hermes-venv/bin/python scripts/local_ai/review.py examples/synthetic-documents/synthetic-paystub.pdf
```

You will see each pipeline step, the extracted fields with the page they came from,
and a list of what a human must verify.

## Step 5 — confirm it stayed local

```bash
./vendor/hermes-venv/bin/python scripts/local_ai/privacy.py status
```

The review output also shows the inference endpoint. It should read
`http://127.0.0.1:8080/v1` with `loopback=True`. `127.0.0.1` means *this computer*.

For a harder proof, turn off your wi-fi and run a review again. It still works.

## Step 6 — use it on a real document

```bash
cp ~/Downloads/paystub.pdf local_data/borrower_documents/
./vendor/hermes-venv/bin/python scripts/local_ai/review.py local_data/borrower_documents/paystub.pdf
```

`local_data/` is gitignored. Nothing in it is ever committed.

## Stopping and cleaning up

```bash
./vendor/hermes-venv/bin/python scripts/local_ai/server.py stop            # stop the model, free the memory
./vendor/hermes-venv/bin/python scripts/local_ai/setup_local_ai.py --list  # see what is downloaded
./vendor/hermes-venv/bin/python scripts/local_ai/setup_local_ai.py --remove qwen3-vl-8b-q8   # delete a model
```

## Going back to a cloud model

Local AI is optional and per-workflow. To point Hermes back at a cloud model:

```bash
bash scripts/hermes.sh model
```

Local Privacy Mode still protects borrower documents — those refuse to use a cloud
endpoint regardless of which model Hermes is configured for.
