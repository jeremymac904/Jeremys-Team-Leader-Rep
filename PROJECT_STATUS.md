# Project status

The durable record of this build. Any coding agent — Claude Code, Codex, Hermes, or a
person — should be able to read this file and continue without the original conversation.

**Last updated:** 2026-08-25
**Version:** 0.3.0
**Phase:** 12 of 12 — **PUBLISHED**. Initial release is live on GitHub.

---

## 1. What this is

A reusable **Loan Factory Team Leader AI Operating System**: a customized Hermes Agent, a
purpose-built skill library, and an optional privacy-first local AI stack for reviewing
mortgage documents without sending them to a cloud provider.

Three layers, all core:

1. **Team Leader Hermes Agent** — persona, operating instructions, safety profile
2. **Custom skill library** — 35 Hermes skills loaded from this repository
3. **Local AI + document analysis** — llama.cpp, Qwen3-VL, NuExtract 3, Local Privacy Mode
4. **Marketing system** — 10 marketing skills over a shared knowledge base, with
   per-Loan-Officer archetypes so coaching is specific rather than generic

Source material: the local Loan Factory Coaching Build.

**Repository:** `https://github.com/jeremymac904/Jeremys-Team-Leader-Rep` (public)

### GitHub status
- **Authorization restored:** 2026-08-25. Account `jeremymac904` — admin and push.
- **Repository changed:** the original target `jeremymcdonald-prog/Jeremys-Team-Leader-Rep`
  was owned by a different GitHub user, and neither authenticated account was ever a
  collaborator on it. Jeremy supplied `jeremymac904/Jeremys-Team-Leader-Rep` instead, which
  the authenticated account owns.
- **First push:** 2026-08-25, commit `c202f10`, 151 files.
- The remote had been initialized with a LICENSE-only commit on an unrelated history. That
  commit was **merged, not force-pushed** — the LICENSE was byte-identical, so nothing was
  discarded and the repository's own initial commit is preserved.
- **Verified after push:** local HEAD matches `origin/main`; GitHub reports 151 blobs and
  **0 restricted paths** (no model weights, vendor, hermes-home, borrower documents,
  internal training assets, or `.env`).

---

## 2. Architecture decisions

| # | Decision | Why |
|---|---|---|
| 1 | Hermes pulled fresh into `vendor/`, isolated by `HERMES_HOME` | The user has existing Hermes installs that must not be touched. `HERMES_HOME` is Hermes's own documented isolation mechanism. |
| 2 | Skills loaded via `skills.external_dirs`, not copied | Supported Hermes mechanism. `git pull` updates skills instantly; external dirs are read-only so agent-created skills never write back into the repo. |
| 3 | Operating instructions at repo-root `AGENTS.md` | Hermes auto-injects a project-root `AGENTS.md`; Claude Code and Codex read it too. |
| 4 | Identity in `SOUL.md`, generated from a template | `$HERMES_HOME/SOUL.md` is the documented identity file. Templated so the leader's name is configurable. |
| 5 | No Hermes source modified | Extension via config, skills, and a local endpoint only. |
| 6 | llama.cpp as the primary local engine | User-approved. Direct control over GGUF, quantization, `mmproj`, context, and bind address — all of which matter for a document-privacy product. Ollama documented as an alternative. |
| 7 | Two local models, not one | A purpose-built extractor (NuExtract 3) is faster and more reliable at pulling fields than a general model. Qwen3-VL reasons about what the fields mean. |
| 8 | 24 GB tier uses higher precision, not a bigger model | Digit fidelity matters more than reasoning breadth for document extraction. |
| 9 | Privacy routing fails closed | An unrecognized workflow is treated as LOCAL_REQUIRED. Over-permissive failure is unrecoverable; over-restrictive failure is a question. |
| 10 | Dependency-free YAML reader (`scripts/lib/miniyaml.py`) | Setup and validation must work on a stock machine with no `pip install`. Uses PyYAML when present. |
| 11 | Model weights never committed | `local_data/**` plus extension-level ignores for `*.gguf`, `*.safetensors`, etc. |
| 13 | Marketing knowledge is shared, not duplicated per skill | Nine files in `knowledge/marketing/` that skills reference. One source of truth per idea; a rule changes once. |
| 14 | Loan Officer marketing **archetypes** | Generic marketing advice is why most LO marketing coaching fails. Ten archetypes drive differentiated plans; validation blocks config/doc drift. |
| 15 | Raw content libraries deliberately not imported | The source material's own `DO_NOT_IMPORT.md` names them. Operational logic was extracted instead. |
| 16 | Compliance disclosures configurable, never hardcoded | Required wording varies by company and state; hardcoding Jeremy's would break reuse. |
| 12 | Paid coaching program not republished | It is a commercial product marked internal. Frameworks were re-authored; the verbatim product was excluded. |

---

## 3. Repository layout

```
AGENTS.md                    agent operating instructions (Hermes auto-injects)
agent/team-leader/           SOUL template, Hermes profile template
skills/
  team-leadership/           14 skills
  mortgage-documents/        11 skills
  marketing/                 10 skills
knowledge/marketing/         9 shared knowledge files
assets/branding/             official Loan Factory logo + derivative
config/                      *.example.yaml templates (real configs gitignored)
automations/                 catalog.yaml (46 automations) + schema + index
coaching/frameworks/         7 coaching methodology documents
prompts/                     9 topic prompt files
templates/                   9 fill-in artifacts
schemas/                     8 mortgage document JSON schemas
local-ai/                    models.manifest.yaml, VALIDATION.md
scripts/
  lib/miniyaml.py            dependency-free YAML subset reader
  local_ai/                  hardware, privacy, extract, review, server, setup, synthetic docs
  setup.py validate.py privacy_scan.py sync_agent.py
  install_hermes.sh hermes.sh
examples/synthetic-documents/ 9 fictional PDFs
tests/run_tests.py           public test suite
docs/                        including docs/local-ai/
local_data/                  GITIGNORED — models, borrower documents, audit
vendor/                      GITIGNORED — fresh Hermes clone + venv
hermes-home/                 GITIGNORED — isolated HERMES_HOME
```

---

## 4. Completed work

- **Phase 1–2** Audit and classification of the source build
- **Phase 3** Architecture
- **Phase 4** Hermes agent: AGENTS.md, SOUL template, locked-down profile
- **Phase 5** Customization: 5 config templates + interview-style `setup.py`
- **Phase 6** 46-automation library with a validated schema, all inactive
- **Phase 7** 9 prompt files, 7 coaching frameworks
- **Phase 8** 9 templates, 7 synthetic documents, fictional sample team
- **Phase 9** setup / validate / privacy-scan / sync / install / hermes launcher
- **Phase 10** Documentation including the full `docs/local-ai/` set
- **Phase 11** 327 tests passing; local AI validated (see `local-ai/VALIDATION.md`)
- **Local AI** hardware detection, 4 tiers, manifest, llama.cpp integration, privacy mode,
  extraction pipeline, OCR, 8 schemas, 8 mortgage skills
- **Marketing integration (v0.2.0)** — audited four new Loan Factory marketing source
  packages; created 9 shared knowledge files, 10 marketing skills, 11 marketing
  automations, `config/marketing.example.yaml` with LO archetypes, brand assets, and
  `docs/provenance.md`; cross-linked 8 existing skills to the new marketing skills

---

## 5. Material excluded for privacy or relevance

| Excluded | Reason |
|---|---|
| `Legends Mortgage Team.csv` | Real roster: names, emails, phones, NMLS numbers |
| `00-local-secrets/` | Live `.env` values and a production secrets map |
| Legends Agent OS runtime auth and session files | Live auth tokens and session state |
| `Loan_Factory_Paid_Coaching_Complete_Program.pdf/.docx` and 12-week curricula | Commercial product marked internal. **Flagged for Jeremy's decision.** Frameworks re-authored instead. |
| Absolute paths from the Legends profile | Replaced with `${REPO_PATH}`; a validation check now fails on `/Users/` or `/Volumes/` in tracked files |
| Jeremy's identity (email, NMLS 1195266) | Replaced with fictional Avery Sample / Northstar Lending Team |
| Next.js coaching site, Gamma decks, video transcripts | Different products, out of scope |
| **Marketing Training Asset Package** (28 files) | Marked "internal Loan Factory training assets"; documents proprietary platform internals with annotated screenshots and contains a corporate email. **Flagged for review.** |
| **Team Marketing Knowledge Pack — corporate strategy sections** | Internal company initiative naming a Loan Factory executive and describing team entitlements. Generic patterns extracted; the strategy document not published. **Flagged for review.** |
| Raw reels / posts / stories libraries, exact DM and email scripts, full AI prompt library | Excluded on the instruction of the source material's own `DO_NOT_IMPORT.md` |
| Marketing Content OS build artifacts (`.next/`, ~500 files) | Machine-generated noise |

---

## 6. Tests and security checks

- `tests/run_tests.py` — **477/477 passing**
- `scripts/validate.py` — 12 structural checks, including marketing archetype drift,
  content-mix totals, and document-type skill/schema routing
- `scripts/privacy_scan.py` — secret and PII scan over everything git would commit
- Gitignore protection asserted in the test suite for models, borrower docs, and configs
- Hermes profile validated against the installed Hermes: real config keys, real toolset names

---

## 7. Known issues

1. **32 GB tier untested.** Qwen3-VL 30B-A3B is a documented recommendation only.
   Marked `recommended-untested`.
2. **Vision path untested end to end.** OCR handled every test document, so the
   `mmproj` fallback never triggered.
   *(Qwen3-VL 8B Q8 download in progress to close this.)*
3. **Only macOS / Apple Silicon validated.** Windows, Linux, NVIDIA, and AMD code paths
   are written but unexercised.
4. **The model reformats values.** `8,412.55` came back as `8412.55`. Values correct,
   formatting not preserved.
5. **25–35 s per document** on an M4 Pro. Not suitable for bulk processing.
6. ~~No synthetic tax return or Closing Disclosure~~ — **resolved.** Both added; all 9
   synthetic documents classify correctly at high confidence.
7. ~~Push blocked~~ — **resolved.** Published to `jeremymac904/Jeremys-Team-Leader-Rep`.
8. **Marketing output not yet validated against a live model.** The marketing skills are
   structurally tested — archetype differentiation, knowledge references, compliance
   linkage — but no generated marketing content has been reviewed for quality by a human.
9. **Two source packages held pending your review** — see the exclusions table.

---

## 8. Deferred work

- Hardened offline mode (firewall / network namespace) — documented as not implemented
- Hybrid redaction workflow — config keys exist, defaults off, deliberately unbuilt
- Income calculation engine — out of scope; underwriting determination
- Multi-document set review against a real file
- Windows and Linux validation
- Synthetic tax return, Closing Disclosure, insurance, and HOA documents
- Marketing Training Asset Package, if Loan Factory approves public distribution
- Live-model quality review of generated marketing content

---

## 9. Next actions

1. ~~Resolve GitHub push access~~ — done
2. ~~Initial commit and push~~ — done, `c202f10`
3. **In progress:** download Qwen3-VL 8B Q8 and validate the reasoning/vision layer,
   which has never been loaded
4. Validate the vision path on a page OCR cannot read
5. Validate the 32 GB tier — requires hardware this project does not have
6. Live-model quality review of generated marketing content

---

## 10. How to continue this work

```bash
bash scripts/install_hermes.sh          # fresh isolated Hermes into vendor/
python3 scripts/sync_agent.py           # load the agent into hermes-home/
python3 scripts/setup.py                # configure identity and team
./vendor/hermes-venv/bin/python scripts/local_ai/setup_local_ai.py   # optional local AI
./vendor/hermes-venv/bin/python tests/run_tests.py --local-ai
python3 scripts/validate.py
python3 scripts/privacy_scan.py
```

**Rules that must not be broken:**
- Never commit anything from `local_data/`, `vendor/`, or `hermes-home/`
- Never commit a real roster, borrower document, or credential
- Never modify Hermes source in `vendor/` — extend via config and skills
- Never claim an integration works without testing it
- Keep `local-ai/VALIDATION.md` honest about what is untested
