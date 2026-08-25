# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning is [Semantic](https://semver.org/): breaking changes to configuration or skill
structure bump the major version.

## [0.2.0] — 2026-08-25

Marketing system, built from four Loan Factory marketing source packages.

### Added
- **10 marketing skills**: Loan Officer marketing coach, content calendar builder, Realtor
  marketing coach, video script builder, content repurposing, campaign builder, social post
  review, brand voice builder, marketing accountability, marketing performance review
- **9 shared marketing knowledge files** in `knowledge/marketing/` — content strategy,
  brand voice, compliance, CTAs, video frameworks, Realtor value, repurposing, campaign
  planning, and Loan Officer archetypes. Skills reference these rather than duplicating them.
- **10 Loan Officer marketing archetypes** so coaching is specific to the person — from
  `no-audience` to `camera-shy` to `has-content-needs-systems`
- **11 marketing automations**, bringing the library to 46
- `config/marketing.example.yaml` — team defaults, configurable compliance disclosures, and
  per-Loan-Officer marketing profiles
- `assets/branding/` — the official Loan Factory logo, original preserved, plus one scaled
  derivative for documentation
- `docs/marketing.md` and `docs/provenance.md`

### Changed
- 8 existing team leadership skills cross-linked to the new marketing skills so Hermes
  routes correctly
- Automation approval rule made substantive: every marketing automation that produces
  publishable content now requires approval, rather than depending on whether a keyword
  appeared in its description
- `scripts/validate.py` — 11 checks; added archetype drift detection and content-mix totals
- Test suite expanded to **432 tests**

### Excluded
- Marketing Training Asset Package — marked internal, shows proprietary platform internals
- Team Marketing Knowledge Pack corporate strategy — internal, names an executive
- Raw content libraries, exact DM and email scripts, and the full prompt library, on the
  instruction of the source material's own `DO_NOT_IMPORT.md`

Both excluded packages are flagged in `docs/provenance.md` for review.

## [0.1.0] — 2026-08-25

Initial release.

### Team Leader Agent
- Hermes Agent profile with operating instructions in `AGENTS.md` and identity in a
  templated `SOUL.md`
- Locked-down safety profile: manual approvals, `cron_mode: deny`, secret and PII
  redaction, action-taking toolsets disabled
- Isolated install — a fresh Hermes clone in `vendor/` with its own `HERMES_HOME`, leaving
  any existing Hermes installation untouched

### Skills (22)
- 14 team leadership skills: morning brief, pipeline review, coaching prep, development
  plans, meeting prep, role-play, recruiting, partners, training, weekly and monthly
  review, automation advisor, guideline research, content planning
- 8 mortgage document skills: local document review, paystub, W2, bank statement, purchase
  contract, Loan Estimate, income comparison, document set review
- Loaded from the repository via `skills.external_dirs` — no copying, `git pull` updates

### Customization
- Five configuration templates covering identity, team, coaching, integrations, local AI
- Interview-style `scripts/setup.py` with sensible defaults

### Automations
- 35-recipe library across 10 categories, all inactive by default
- Machine-readable catalog with a validated schema and a generated index

### Local AI
- llama.cpp integration through supported Hermes provider configuration
- Four hardware tiers (8 / 16 / 24 / 32 GB) with round-down selection
- Curated model manifest: Qwen3-VL 4B / 8B / 30B-A3B and NuExtract 3, all Apache-2.0
- Hardware detection for macOS, Windows, Linux, Apple Silicon, NVIDIA, AMD
- **Local Privacy Mode** with fail-closed routing and no silent cloud fallback
- Document pipeline: native text, table extraction, local OCR, vision fallback
- 8 mortgage document JSON schemas with source traceability and confidence
- 7 fictional test documents

### Content
- 7 coaching frameworks, 9 prompt files, 9 fill-in templates

### Tooling
- `validate.py` (10 checks), `privacy_scan.py`, `sync_agent.py`, `install_hermes.sh`
- Dependency-free YAML reader so setup works without `pip install`
- 327-test suite

### Known limitations
- 32 GB tier and the vision path are untested — see `local-ai/VALIDATION.md`
- Only macOS / Apple Silicon validated
- No working connectors to Gmail, Calendar, CRM, or LOS — by design, and stated plainly
- Hybrid redaction workflow deliberately not implemented
