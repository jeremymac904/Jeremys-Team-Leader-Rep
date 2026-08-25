# Hardware and models

## Plain-language glossary

**Model** — the AI itself: a large file of learned numbers. Bigger models are
generally smarter and need more memory.

**Parameters** — how big the model is. "8B" means 8 billion parameters. More
parameters, more memory.

**GGUF** — the file format llama.cpp uses. When you see a `.gguf` file, that is a
model packaged to run on your own machine.

**Quantization** — compression for models. The original is stored at high precision;
quantization stores it more compactly so it fits in less memory, at a small cost in
accuracy.

- **Q4_K_M** — about a quarter of the original size. The usual choice. Good quality.
- **Q8_0** — about half. Noticeably better with digits and tables. Twice the memory.
- **F16** — uncompressed. Rarely worth it locally.

For mortgage documents, quantization matters more than usual, because the difference
between a `3` and an `8` in an income figure is not a rounding error. That is why the
24 GB tier spends its extra memory on **higher precision of the same model** rather
than on a bigger model.

**Context length** — how much the model can consider at once. A 30-page contract
needs more context than a one-page paystub. More context uses more memory.

**Local vs cloud inference** — local means the model runs on your computer and your
data never leaves. Cloud means your data is sent to a company's servers. Cloud models
are smarter; local models are private.

**Hugging Face** — the site where open models are published. Everything here comes
from official publisher accounts (`Qwen`, `numind`), not random re-uploads.

**llama.cpp vs Llama** — easy to confuse. **llama.cpp** is the *engine* that runs
models. **Llama** is a *model family* from Meta. This system uses llama.cpp the
engine, with **Qwen3-VL** models — not Meta's Llama.

## The four tiers

Your memory decides your tier. Non-standard sizes round **down**: 12 GB gets the 8 GB
tier, 18 GB gets 16 GB, 28 GB gets 24 GB. Rounding up would leave too little room for
the operating system, Hermes, and document extraction.

| Tier | Memory | Reasoning model | Quant | Download | What it handles |
|---|---|---|---|---|---|
| Basic | 8 GB | Qwen3-VL 4B Instruct | Q4_K_M | ~2.9 GB | Paystubs, W2s, simple statements, short contracts |
| **Standard** | **16 GB** | **Qwen3-VL 8B Instruct** | **Q4_K_M** | **~5.8 GB** | **The mainstream recommendation** — multiple paystubs, W2 comparison, statements, contracts, Loan Estimates |
| Higher quality | 24 GB | Qwen3-VL 8B Instruct | Q8_0 | ~9.9 GB | Same model, better precision. More context, more pages |
| Advanced | 32 GB+ | Qwen3-VL 30B-A3B Instruct | Q4_K_M | ~19.3 GB | Cross-document comparison, long contracts, complex income |

Every tier also downloads **NuExtract 3** (~3.5 GB), a small model built specifically
for pulling structured fields out of documents.

## Why two models

Using one large general model for everything is wasteful. Pulling "Box 1 = 74,218.66"
off a W2 is a narrow, mechanical job — a purpose-built extraction model does it faster
and more reliably than a general reasoning model.

So the pipeline is:

```
document -> local text extraction -> NuExtract 3 (structured fields)
                                  -> Qwen3-VL (what the fields mean)
                                  -> Team Leader skill (structured output)
```

Qwen3-VL is also a **vision** model, which is what makes scanned documents work when
OCR alone is not enough.

## About the 32 GB tier

Qwen3-VL 30B-A3B is a **Mixture of Experts** model: 30 billion parameters total, but
only about 3 billion are active for any given token. It reasons better than a dense 8B
while running much lighter than a dense 30B.

The catch: **the whole model still has to fit in memory.** That is why it needs 32 GB
even though it computes like a small model.

This tier is marked `recommended-untested` in the manifest. It was not validated on
this project's hardware (a 24 GB machine). See `local-ai/VALIDATION.md` for exactly
what was and was not tested.

## Licensing

Every model here is **Apache 2.0**, which permits commercial use. That was checked
before anything was recommended, and the check date is recorded in the manifest.

## Changing models

The manifest at `local-ai/models.manifest.yaml` is the single source of truth. Better
models will come out. Edit that file — nothing else needs to change.

```bash
./vendor/hermes-venv/bin/python scripts/local_ai/setup_local_ai.py --list
./vendor/hermes-venv/bin/python scripts/local_ai/setup_local_ai.py --model <id>
./vendor/hermes-venv/bin/python scripts/local_ai/setup_local_ai.py --remove <id>
```
