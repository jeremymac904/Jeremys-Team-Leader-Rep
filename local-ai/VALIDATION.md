# Local AI validation record

What was actually tested, on what hardware, and what was not. Claims here are limited
to what was observed.

**Validated on:** 2026-08-25 (updated after Qwen3-VL validation)
**Machine:** Apple M4 Pro, 12 CPU cores, 16 GPU cores, 24 GB unified memory, macOS 25.4
**Detected tier:** `tier-24gb`
**Engine:** llama.cpp `version 0.3.0 (build 10621, commit c1d0e7a00)`, installed via Homebrew
**Hermes:** Agent v0.20.5, freshly cloned into `vendor/hermes-agent`

---

## Verified working

| Item | Evidence |
|---|---|
| Hardware detection | Correctly read M4 Pro, 24 GB, 16 GPU cores, arm64, Metal backend |
| Tier selection | All 9 mapping cases pass, including 12→8 GB, 18→16 GB, 28→24 GB round-down |
| Manifest integrity | All 5 models and 4 tiers parse; every tier reference resolves; all licenses Apache-2.0 |
| Model download | NuExtract 3 (3.46 GB) and **Qwen3-VL 8B Q8 (9.87 GB)** from their official Hugging Face repos |
| **Qwen3-VL 8B Q8 loads** | `llama-server` loaded it as a **multimodal** model, `n_ctx_slot = 32768`, **11.43 GB resident** |
| **Vision path end to end** | A PDF with a **0-character text layer** and OCR disabled was classified AND extracted correctly by the vision model reading the page image |
| **Cheapest-method routing** | Same file with OCR enabled used OCR (14.2 s) and did **not** invoke vision (41.1 s). Vision is a genuine fallback, not the default. |
| Model loads in llama.cpp | `llama-server` loaded it as a **multimodal** model, `n_ctx_slot = 8192` |
| Local inference | Round trip returned `LOCAL INFERENCE OK` in 1.3 s |
| Loopback binding | `lsof` shows `TCP 127.0.0.1:8080 (LISTEN)` and **no** established external connections |
| Native PDF extraction | 7/7 synthetic documents classified correctly at high confidence |
| Scanned PDF + OCR | Image-only PDF (0-character text layer) → tesseract 5.5.2 → correct values |
| Structured extraction | paystub, W2, bank statement, purchase contract — all fields correct against source |
| Privacy routing | 11 classification cases pass; unknown workflows fail closed to LOCAL_REQUIRED |
| Cloud blocking | Cloud endpoint raises `PrivacyViolation` for a paystub; loopback is permitted |
| No silent fallback | With the model stopped, the pipeline halted, explained, and offered choices without acting |
| Hermes skill loading | 22 skills load from the repo via `skills.external_dirs` |
| Gitignore protection | Model, borrower-document, and config paths are all confirmed ignored |
| Test suite | **327/327 passing** with `--local-ai` |

### Measured performance (24 GB M4 Pro, NuExtract3 Q4_K_M, 8k context)

**NuExtract 3 Q4_K_M, 8k context**

| Document | Total |
|---|---|
| Paystub (native text) | 35.4 s |
| W2 | 30.2 s |
| Bank statement | 24.6 s |
| Purchase contract | 33.9 s |
| Paystub (scanned, OCR) | 33.0 s |

Memory: ~3.5 GB resident.

**Qwen3-VL 8B Q8, 32k context** — roughly twice as fast, and it preserves number
formatting that NuExtract 3 normalized away.

| Document | Path | Total |
|---|---|---|
| Paystub | native text | 16.4 s |
| W2 | native text | 11.9 s |
| Tax return | native text | 13.1 s |
| W2 (scanned) | OCR | 14.2 s |
| **W2 (scanned, OCR off)** | **vision** | **41.1 s** |

Memory: **11.43 GB resident** on a 24 GB machine — comfortable, but it is the reason
the 24 GB tier does not also try to hold a larger model.

---

## NOT validated

Stated plainly. Do not read the sections above as covering these.

| Item | Why not | Risk |
|---|---|---|
| **Qwen3-VL 8B Q4_K_M** | Only the Q8_0 variant was downloaded and tested. | Low. Same repo and format, differing only in quantization. |
| **Qwen3-VL 30B-A3B (32 GB tier)** | This machine has 24 GB. Cannot run it. Marked `recommended-untested` in the manifest. | **Medium.** The 32 GB tier is a documented recommendation, not a tested one. |
| **Qwen3-VL 4B (8 GB tier)** | Not downloaded. | Low. |
| ~~Vision path~~ | **Now validated.** See above. | Resolved. |
| **Windows and Linux** | Only macOS was available. Detection code for both is written but unexercised. | Medium. |
| **NVIDIA / AMD GPU detection** | No such hardware present. | Medium. |
| **Multi-page and multi-document sets** | All synthetic documents are one page. `document-set-review` has not been run against a real set. | Medium. |
| ~~Tax return extraction~~ | **Now validated** against a synthetic return with Schedule C and E. | Resolved. |
| ~~Closing Disclosure~~ | Synthetic CD added and classifies correctly. Field extraction not yet run against it. | Low. |
| **Hybrid redaction workflow** | Deliberately not implemented. Config keys exist and default to off. | None — it is off. |
| **OS-level network isolation** | Not implemented and not claimed. Routing is application-level only. | See `docs/local-ai/privacy-mode.md`. |
| **Real borrower documents** | Never used, by design. Only synthetic data. | Real documents have messier layouts than these. |

---

## Defects found and fixed during this validation

1. **The vision path was documented but never wired.** `needs_vision` was flagged on
   pages with no text layer, but no image was ever sent to the model, and an early
   "no text extracted" guard returned before vision could run. Pages are now rendered
   to `local_data/working/pages/` and passed to the multimodal endpoint, and a scanned
   document with no text layer is now classified *and* extracted by the vision model.

2. **The extraction prompt sent field names without types**, so the model guessed. A
   field declared as an array of schedule names came back as the boolean `true`. The
   prompt now states the expected type per field; arrays now return arrays with real
   content.

3. **A Closing Disclosure misclassified as a purchase contract.** Both matched three
   generic markers and the tie resolved by dictionary order. Replaced with weighted
   markers plus a margin requirement.

4. **Three document types routed to skills that did not exist** — `tax-return-review`,
   `closing-disclosure-review`, `mortgage-statement-review`. All three were built, and
   a validation check now blocks dangling routes.

## Known limitations found during testing

1. **NuExtract 3 is a reasoning model.** It emits a chain of thought into
   `reasoning_content` before the answer. A small `max_tokens` returns empty content and
   looks like a failure. Both `server.py` and `review.py` now budget 512 / 4096 tokens
   and fall back to `reasoning_content`. Anyone adding a new call site must do the same.

2. **The model normalizes formatting despite instructions to copy exactly.** On the bank
   statement it returned `8412.55` for `8,412.55` and `2026-06-01` for `06/01/2026`. Values
   were correct; formatting was not preserved. Do not rely on verbatim formatting.

3. **Extraction takes 25–35 s per document** on this hardware. Fine for a handful of
   documents, too slow for bulk processing.

4. **Classification uses keyword signatures, not a model.** Fast and predictable, but an
   unusual layout can be misclassified. Confidence is reported so a low score is visible.

5. **OCR quality caps everything downstream.** A poor scan produces poor fields. The
   pipeline reports a low character count rather than pretending it read the page.

6. **The model does not always populate judgment fields.** `human_verification_items`
   and `requires_underwriting_analysis` sometimes come back empty even when the document
   warrants entries. Extraction fidelity is good; editorial judgment is weaker. Treat an
   empty verification list as "the model had nothing to add", never as "nothing needs
   checking".

7. **Vision costs roughly 3x the time of OCR** (41 s vs 14 s on the same page). The
   pipeline prefers OCR for that reason, and falls back only when there is no text.

---

## How to re-run this

```bash
python3 scripts/local_ai/hardware.py
python3 scripts/local_ai/setup_local_ai.py --dry-run
python3 scripts/local_ai/server.py start --model qwen3-vl-8b-q8 --context 32768
python3 scripts/local_ai/server.py test
./vendor/hermes-venv/bin/python tests/run_tests.py --local-ai
./vendor/hermes-venv/bin/python scripts/local_ai/review.py examples/synthetic-documents/synthetic-paystub.pdf
```

If you validate a tier or platform listed as untested, please update this file.
