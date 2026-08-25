# Local AI troubleshooting

## "llama-server not found"

Not installed, or not on your PATH.

```bash
brew install llama.cpp     # macOS
llama-server --version     # verify
```

## The server exits right after starting

Read the log — it says why:

```bash
tail -40 local_data/working/llama-server.log
```

Usual causes:

- **Out of memory.** The model needs more than you have free. Close things, lower the
  context (`-c`), or drop a tier.
- **Corrupt download.** A partial file. Remove and re-download:
  ```bash
  ./vendor/hermes-venv/bin/python scripts/local_ai/setup_local_ai.py --remove <model-id>
  ./vendor/hermes-venv/bin/python scripts/local_ai/setup_local_ai.py --model <model-id>
  ```
- **Port already in use.** Change `reasoning_port` in `config/local-ai.yaml`.

## "The local model server is not running"

```bash
./vendor/hermes-venv/bin/python scripts/local_ai/server.py start
./vendor/hermes-venv/bin/python scripts/local_ai/server.py health
```

This message is the no-fallback behavior working correctly. It refused to send your
document to a cloud model. Nothing left your computer.

## Review is very slow

- First run loads the model into memory — that is one-time.
- Check the GPU is being used: the log should mention Metal or CUDA. If not, `-ngl` is
  too low.
- Long documents take longer. `max_pages_per_document` caps this.
- On CPU-only hardware it is simply slow. Use the smallest tier model.

## OCR produces garbage or nothing

```bash
tesseract --version      # macOS: brew install tesseract
```

- Low-quality scans OCR badly. Raise `render_dpi` to 300 in `config/local-ai.yaml`.
- Rotated pages fail. Straighten before scanning.
- Some scans are simply too poor. The system tells you the character count was low
  rather than pretending it read the page — verify that page by hand.

## Numbers are wrong

**This is expected and is why every output carries a verification list.**

Quantized models misread digits, especially on scans. If accuracy matters and you have
the memory, move to a Q8_0 model. Regardless: **check every dollar amount and date
against the source document.** The system is a reading assistant, not a system of
record.

## Fields come back empty

- The document may genuinely not contain them — check the "not found" list.
- Classification may be wrong. Run with `--extract-only` to see the raw text.
- The document may be a variant the schema does not match. Schemas are editable in
  `schemas/`.

## Wrong document type detected

Classification uses keyword signatures. Unusual layouts confuse it.

```bash
./vendor/hermes-venv/bin/python scripts/local_ai/extract.py <file> --classify-only
```

If confidence is `low`, say the type explicitly when you ask the agent.

## Disk is filling up

```bash
./vendor/hermes-venv/bin/python scripts/local_ai/setup_local_ai.py --list
./vendor/hermes-venv/bin/python scripts/local_ai/setup_local_ai.py --remove <model-id>
```

## Verifying nothing left the machine

```bash
./vendor/hermes-venv/bin/python scripts/local_ai/privacy.py status
cat local_data/audit/privacy-audit.jsonl
```

Best proof: turn off wi-fi and run a review. If it completes, it was local.
