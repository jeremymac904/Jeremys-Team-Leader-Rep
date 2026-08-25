# Provenance

Where the knowledge in this repository came from, so a future maintainer can trace a skill
back to its source. Local paths are deliberately not recorded — source packages are named,
not located.

## Source packages reviewed

| Package | Reviewed | Verdict |
|---|---|---|
| Complete Coaching Program | 2026-08-25 | Frameworks re-authored; the paid product itself excluded |
| Legends Agent OS (Hermes prior art) | 2026-08-25 | Skill schema and cron-template schema adopted; config generalized |
| **Loan Factory Social Media Assistant (FINAL_REVIEWED)** | **2026-08-25** | **Most authoritative marketing source.** Operational logic extracted; raw libraries excluded |
| **Loan Factory Marketing Content OS** | 2026-08-25 | Workflow, compliance, brand rules, and AI routing extracted |
| **Loan Factory Team Marketing System Knowledge Pack** | 2026-08-25 | Generic patterns extracted only; corporate strategy excluded — see below |
| **Loan Factory Marketing Training Asset Package** | 2026-08-25 | **Excluded** — marked internal, documents proprietary platform internals |
| Official Loan Factory logo | 2026-08-25 | Added to `assets/branding/`, original preserved |

## What became what

| Source concept | Became | Transformation |
|---|---|---|
| Social Media Assistant — content strategy system | `knowledge/marketing/content-strategy.md` | Mix, cadence, weekly structure, and quality bar extracted; generalized to configurable defaults |
| Social Media Assistant — brand and positioning | `knowledge/marketing/brand-voice.md` | Positioning pillars kept; per-LO voice layer added |
| Social Media Assistant — compliance and do-not-say | `knowledge/marketing/marketing-compliance.md` | Guardrails kept nearly intact; disclosure text made configurable rather than hardcoded |
| Social Media Assistant — CTA system | `knowledge/marketing/cta-system.md` | Patterns kept by audience; rationale added |
| Social Media Assistant — video frameworks and hooks | `knowledge/marketing/video-frameworks.md` | Hook patterns and frameworks kept; camera-shy alternatives added |
| Social Media Assistant — Realtor attraction | `knowledge/marketing/realtor-value.md` | Framework kept; RESPA flagging added |
| Marketing Content OS — content workflow | `campaign-builder`, `content-calendar-builder` | Draft → brand pass → compliance pass → human review preserved as skill workflow |
| Marketing Content OS — AI tool routing | `knowledge/marketing/marketing-compliance.md`, `docs/local-ai/privacy-mode.md` | "No secrets or client data into public AI tools" reinforced the existing privacy routing |
| Marketing Content OS — compliance rules and brand rules | `knowledge/marketing/marketing-compliance.md` | Merged with the Social Media Assistant version; the stricter reading kept where they differed |
| Marketing Content OS — GPT instructions | The marketing skills | Converted from GPT system prompts into Hermes skill workflows |
| Team Marketing Knowledge Pack — repurposing and team patterns | `knowledge/marketing/content-repurposing.md` | Generic repurposing logic only |
| Team Marketing Knowledge Pack — team structure patterns | `knowledge/marketing/lo-marketing-profiles.md` | Informed the archetype model; corporate specifics dropped |

## Deduplication decisions

The marketing sources overlapped substantially. What was chosen and why:

| Overlap | Chosen | Why |
|---|---|---|
| Compliance rules — appeared in both the Social Media Assistant and Content OS | Merged, stricter reading wins | Both were sound; where they differed, the more conservative rule was kept |
| Brand rules — appeared in both | Social Media Assistant version | Marked FINAL_REVIEWED and more complete on prohibited language |
| Content workflow — Content OS `Content_Workflow.md` vs Social Media Assistant strategy | Both, at different layers | Content OS supplied the review loop; the Assistant supplied the content model. Not competing. |
| Multiple content libraries (reels, posts, stories) | **None imported** | See exclusions |

There is now **one** marketing architecture, not two.

## Excluded, and why

| Excluded | Reason |
|---|---|
| Raw reels, posts, and stories libraries (~31 KB of ready-made content) | The source material's own `DO_NOT_IMPORT.md` names these as content not to copy into repo examples or prompts. Honored. |
| Exact DM scripts and email follow-up scripts | Same instruction. The *logic* is in `cta-system.md`; the verbatim scripts are not reproduced. |
| Full AI prompt library | Same instruction. |
| **Marketing Training Asset Package (all 28 files)** | Its README says "Treat these as internal Loan Factory training assets." It documents proprietary Loan Factory platform internals with annotated screenshots and contains a corporate email address. **Not appropriate for a public repository.** |
| Team Marketing Knowledge Pack — corporate strategy sections | Internal company initiative attributed to a named Loan Factory executive, describing what "approved teams can receive." Internal corporate material. **Flagged for review.** |
| Marketing Content OS build artifacts (`.next/`, `node_modules/`) | Machine-generated noise, ~500 files |
| Client scenarios and non-public personal information | Named in `DO_NOT_IMPORT.md`; none found in what was extracted |

## Flagged for Jeremy's decision

Two items are useful but were held back pending your review:

1. **Marketing Training Asset Package** — genuinely valuable LO training on Facebook Ads,
   Google Ads/GA4, lead funnels, and the QM Pricer. But it is marked internal and shows
   Loan Factory platform screenshots. If Loan Factory approves public distribution, it
   could become a training module. Until then it stays in the source folder only.

2. **Team Marketing System Knowledge Pack corporate sections** — team structure by
   language and region, shared infrastructure entitlements, podcast and YouTube strategy.
   Reusable in concept, but as written it is internal corporate strategy naming an
   executive. The generic patterns were extracted; the strategy document was not published.

Neither is in the repository. Say the word and either can be adapted.

## Maintaining this

When you add material from a new source, add a row to the tables above: what the source
was, what it became, and what you left out. The goal is that someone can answer "why does
this skill say that?" without asking you.
