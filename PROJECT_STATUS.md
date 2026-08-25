# Project status

The durable record of this build. Any coding agent — Claude Code, Codex, Hermes, or a
person — should be able to read this file and continue without the original conversation.

**Last updated:** 2026-08-25
**Version:** 0.1.0 (pre-release)
**Phase:** 11 of 12 — testing and validation complete; preparing the initial release

---

## 1. What this is

A reusable **Loan Factory Team Leader AI Operating System**: a customized Hermes Agent, a
purpose-built skill library, and an optional privacy-first local AI stack for reviewing
mortgage documents without sending them to a cloud provider.

Three layers, all core:

1. **Team Leader Hermes Agent** — persona, operating instructions, safety profile
2. **Custom skill library** — 22 Hermes skills loaded from this repository
3. **Local AI + document analysis** — llama.cpp, Qwen3-VL, NuExtract 3, Local Privacy Mode

Source material: the local Loan Factory Coaching Build. Target:
`https://github.com/jeremymcdonald-prog/Jeremys-Team-Leader-Rep` (public).

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
| 12 | Paid coaching program not republished | It is a commercial product marked internal. Frameworks were re-authored; the verbatim product was excluded. |

---

## 3. Repository layout

```
AGENTS.md                    agent operating instructions (Hermes auto-injects)
agent/team-leader/           SOUL template, Hermes profile template
skills/
  team-leadership/           14 skills
  mortgage-documents/        8 skills
config/                      *.example.yaml templates (real configs gitignored)
automations/                 catalog.yaml (35 automations) + schema + index
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
examples/synthetic-documents/ 7 fictional PDFs
tests/run_tests.py           327 tests
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
- **Phase 6** 35-automation library with a validated schema, all inactive
- **Phase 7** 9 prompt files, 7 coaching frameworks
- **Phase 8** 9 templates, 7 synthetic documents, fictional sample team
- **Phase 9** setup / validate / privacy-scan / sync / install / hermes launcher
- **Phase 10** Documentation including the full `docs/local-ai/` set
- **Phase 11** 327 tests passing; local AI validated (see `local-ai/VALIDATION.md`)
- **Local AI** hardware detection, 4 tiers, manifest, llama.cpp integration, privacy mode,
  extraction pipeline, OCR, 8 schemas, 8 mortgage skills

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

---

## 6. Tests and security checks

- `tests/run_tests.py` — **327/327 passing** with `--local-ai`
- `scripts/validate.py` — 10 structural checks
- `scripts/privacy_scan.py` — secret and PII scan over everything git would commit
- Gitignore protection asserted in the test suite for models, borrower docs, and configs
- Hermes profile validated against the installed Hermes: real config keys, real toolset names

---

## 7. Known issues

1. **32 GB tier untested.** Qwen3-VL 30B-A3B is a documented recommendation only.
   Marked `recommended-untested`.
2. **Vision path untested end to end.** OCR handled every test document, so the
   `mmproj` fallback never triggered.
3. **Only macOS / Apple Silicon validated.** Windows, Linux, NVIDIA, and AMD code paths
   are written but unexercised.
4. **The model reformats values.** `8,412.55` came back as `8412.55`. Values correct,
   formatting not preserved.
5. **25–35 s per document** on an M4 Pro. Not suitable for bulk processing.
6. **No synthetic tax return or Closing Disclosure** yet, though both schemas exist.
7. **Push blocked:** neither authenticated `gh` account has push access to the target repo.

---

## 8. Deferred work

- Hardened offline mode (firewall / network namespace) — documented as not implemented
- Hybrid redaction workflow — config keys exist, defaults off, deliberately unbuilt
- Income calculation engine — out of scope; underwriting determination
- Multi-document set review against a real file
- Windows and Linux validation
- Synthetic tax return, Closing Disclosure, insurance, and HOA documents

---

## 9. Next actions

1. Resolve GitHub push access (see §7.7)
2. Finish remaining root documentation (README, CHANGELOG, CONTRIBUTING, SECURITY)
3. Final privacy and secret audit over the full tracked file list
4. Initial commit and push
5. Post-release: validate the 32 GB tier and the vision path

---

## 10. How to continue this work

```bash
bash scripts/install_hermes.sh          # fresh isolated Hermes into vendor/
python3 scripts/sync_agent.py           # load the agent into hermes-home/
python3 scripts/setup.py                # configure identity and team
python3 scripts/local_ai/setup_local_ai.py   # optional local AI
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
