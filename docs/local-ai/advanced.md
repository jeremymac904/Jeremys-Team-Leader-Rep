# Advanced: architecture and tuning

## Pipeline

```
                 local_data/borrower_documents/  (gitignored)
                                |
                    +-----------v-----------+
                    |   privacy routing     |  LOCAL_REQUIRED? fail closed
                    +-----------+-----------+
                                |
                    +-----------v-----------+
                    |  file type detection  |  pdf / docx / xlsx / image
                    +-----------+-----------+
                                |
          +---------------------+---------------------+
          |                     |                     |
   native text layer?      scanned page?         image file?
   (pymupdf)               (tesseract OCR)       (OCR, then vision)
          |                     |                     |
          +---------------------+---------------------+
                                |
                    +-----------v-----------+
                    |  table extraction     |  pdfplumber
                    +-----------+-----------+
                                |
                    +-----------v-----------+
                    | document classification|  keyword signatures
                    +-----------+-----------+
                                |
                    +-----------v-----------+
                    |   schema selection     |  schemas/*.schema.json
                    +-----------+-----------+
                                |
                    +-----------v-----------+
                    |  PRIVACY GATE          |  endpoint must be loopback
                    +-----------+-----------+
                                |
                    +-----------v-----------+
                    | structured extraction  |  llama-server 127.0.0.1
                    +-----------+-----------+
                                |
                    +-----------v-----------+
                    |  Hermes skill routing  |  paystub-review, etc.
                    +-----------+-----------+
                                |
                     structured output + page refs
                     + confidence + verification list
```

Cheapest method first. A native text layer is read directly; OCR only runs when a page
has fewer than `min_chars_for_native` characters; the vision model is the last resort.
Handing every page to a vision model would be slower and less accurate than reading
text that is already there.

## Hermes integration

Local document inference uses llama.cpp directly. No Hermes source was modified.

`llama-server` exposes an OpenAI-compatible API on loopback. The documented local tiers
are intended for private document review, not Hermes chat: current Hermes releases require
at least 64K model context, while these tiers use 8K-32K to fit safely in memory. Use your
chosen cloud provider for Hermes chat workflows and the local server for borrower documents.

Check the current compatibility guidance for your setup:
```bash
./vendor/hermes-venv/bin/python scripts/local_ai/server.py hermes-config
```

Skills load through `skills.external_dirs`, also a supported Hermes mechanism —
see [../hermes.md](../hermes.md).

## llama-server flags used

```bash
llama-server \
  -m local_data/models/<id>/<model>.gguf \
  --mmproj local_data/models/<id>/mmproj-<model>.gguf \
  --host 127.0.0.1 \
  --port 8080 \
  -c <context> \
  -ngl 99
```

| Flag | Why |
|---|---|
| `--mmproj` | The vision projector. Without it the model is text-only and scanned pages fail. |
| `--host 127.0.0.1` | Loopback only. Not reachable from your network. |
| `-c` | Context window. Set from your tier. Larger uses more memory. |
| `-ngl 99` | Offload all layers to the GPU — Metal on Apple Silicon, CUDA on NVIDIA. Lower it if you run out of memory. |

Adjust in `config/local-ai.yaml` under `engine`.

## Performance tuning

**Apple Silicon.** Metal is used automatically; `-ngl 99` puts everything on the GPU.
Unified memory means GPU and CPU share the same pool, which is why total RAM is what
matters. Do not run a 19 GB model on 24 GB while Chrome has forty tabs open.

**NVIDIA.** `-ngl 99` offloads to CUDA. If the model exceeds VRAM, lower `-ngl` to
split between GPU and CPU — slower, but it runs.

**CPU only.** Expect it to be slow. Use the 8 GB tier model regardless of memory, and
set `threads` to your physical core count.

**Context.** The most common cause of running out of memory is too much context, not
too big a model. Halve `-c` before dropping to a smaller model.

## Choosing a different model

The manifest is the single source of truth. To evaluate something new:

1. Confirm it has GGUF files and an `mmproj` if you need vision
2. Check the license permits commercial use
3. Add an entry to `local-ai/models.manifest.yaml` with `status: experimental`
4. `./vendor/hermes-venv/bin/python scripts/local_ai/setup_local_ai.py --model <your-id>`
5. Test it against `examples/synthetic-documents/` before trusting it

Hermes ships a built-in `llama-cpp` skill that helps pick GGUF quantizations from the
Hugging Face Hub — ask the agent about it.

## Why llama.cpp rather than Ollama

Both work with Hermes. Ollama is easier to install and Hermes even has native support
for reading its model catalogue.

llama.cpp was chosen as the primary engine because this is a **document privacy**
system, and llama.cpp gives direct control over the things that matter here: the exact
GGUF and quantization, the `mmproj` vision projector, the context size, and the bind
address. Nothing is managed by a background service.

If you already run Ollama, you can point this at it — it also serves an
OpenAI-compatible API on `127.0.0.1:11434/v1`. Set that as `base_url`. The privacy
gate checks for loopback, not for a particular engine.

## What is NOT implemented

Stated plainly so nobody assumes otherwise:

- **OS-level network isolation.** Routing is enforced in application code. No firewall
  rules are installed. See [privacy-mode.md](privacy-mode.md).
- **The redaction / hybrid workflow.** The config keys exist and default to off.
  Detecting every PII field reliably enough to promise a sanitized document is a hard
  problem, and shipping it half-done would be worse than not shipping it.
- **An income calculation engine.** Deliberately out of scope. Qualifying income is an
  underwriting determination.
- **Forgery or tamper detection.** Not attempted, and not implied.
