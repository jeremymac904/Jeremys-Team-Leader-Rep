# Loan Factory Team Leader OS

An AI operating system for a mortgage Team Leader, built on the
[Hermes Agent](https://github.com/NousResearch/hermes-agent).

Clone it, answer a few questions, and you have an assistant that knows your team, coaches
the way you coach, prepares your meetings, and reviews loan documents **on your own
computer** so borrower information never reaches a cloud AI service.

```bash
git clone https://github.com/jeremymcdonald-prog/Jeremys-Team-Leader-Rep.git
cd Jeremys-Team-Leader-Rep
bash scripts/install_hermes.sh
python3 scripts/setup.py
bash scripts/hermes.sh
```

Then ask: **"Give me my Team Leader morning briefing."**

---

## What is this?

A repository containing a configured AI agent, 22 purpose-built skills, 35 automation
recipes, coaching frameworks, prompts, templates, and an optional local AI stack for
mortgage document review.

It is not a SaaS product. Nothing is hosted. It runs on your machine, and your data stays
in files you control.

## Who is it for?

A Loan Factory Team Leader who is still producing — leading a team *and* closing their own
loans, with no time for administration.

You do not need to be a programmer. You need to be willing to copy and paste a few
commands. Where this README mentions something technical, it explains it.

## What can it do?

**Leadership and coaching**
- A ranked morning briefing — the three things that actually need you today
- One-on-one prep with the diagnosis already done
- 30/60/90 development plans, ramp plans, recovery plans
- Live sales role-play, scored, with an exact rewrite of your weakest line
- Team meeting agendas built from this week's real pattern, not a topic rotation
- Your own weekly and monthly review, including your own production

**Pipeline and partners**
- Pipeline review: stalled files, closings at risk, borrowers who have gone silent
- Referral partner review, including the agent who quietly stopped referring
- Recruiting pipeline, interview prep, candidate comparison

**Mortgage documents — processed locally**
- Read a PDF, including a scanned one, entirely on your computer
- Extract structured fields from paystubs, W2s, bank statements, purchase contracts,
  Loan Estimates, Closing Disclosures, and mortgage statements
- Compare income documents against each other
- Find what is missing or contradictory across a whole file

**Automation**
- 35 documented automation recipes, all inactive until you choose one
- An advisor that will tell you when something should *stay* manual

## Why would a Team Leader use it?

Because the work that eats your week is repetitive, and the work that grows your team is
not. This automates the first so you have time for the second.

And because your team handles documents full of Social Security numbers and account
numbers. Pasting those into a cloud AI tool is a real problem. This gives you a way to use
AI on them without that.

## What is Hermes?

[Hermes Agent](https://github.com/NousResearch/hermes-agent) is an open-source AI agent
from Nous Research that runs on your own computer. It can use different AI models — cloud
ones like Claude or GPT, or a local model running on your machine.

This repository does not replace Hermes. It **configures** it: an identity, a skill
library, a safety profile, and an optional local model.

`bash scripts/install_hermes.sh` pulls a fresh, private copy of Hermes into this folder.
If you already run Hermes for something else, **it is not touched** — this copy is
completely isolated.

---

## Before you install

| Requirement | Notes |
|---|---|
| macOS, Windows, or Linux | Apple Silicon Macs are the best-tested platform |
| Python 3.11 or newer | `python3 --version` |
| Git | macOS: `xcode-select --install` |
| An AI model | Either an API key for a cloud model, or ~15 GB of disk for a local one |

Optional, only for local document review:

| Requirement | Install |
|---|---|
| llama.cpp | `brew install llama.cpp` |
| tesseract (for scanned documents) | `brew install tesseract` |
| 16 GB+ memory | 8 GB works with a smaller model |

## Install

**1. Get the repository**
```bash
git clone https://github.com/jeremymcdonald-prog/Jeremys-Team-Leader-Rep.git
cd Jeremys-Team-Leader-Rep
```

**2. Install a private copy of Hermes**
```bash
bash scripts/install_hermes.sh
```
Downloads Hermes into `vendor/` inside this folder. Takes a few minutes. Touches nothing
else on your computer.

**3. Configure yourself and your team**
```bash
python3 scripts/setup.py
```
An interview: your name, team, market, goals, KPIs, coaching style, schedule. Everything
has a sensible default — press Enter to accept.

**4. Choose a model**
```bash
bash scripts/hermes.sh setup
```

**5. Check everything**
```bash
python3 scripts/validate.py
```

**6. Start**
```bash
bash scripts/hermes.sh
```

## Your first hour

See **[docs/first-hour.md](docs/first-hour.md)**. Short version:

1. Open `team-data/team.yaml` and replace the fictional team with your real one
2. Ask: *"Give me my Team Leader morning briefing."*
3. Export your pipeline, paste it, ask: *"Run a pipeline review on this."*
4. Ask: *"Prep my one-on-one with [name]."*
5. Pick one automation from [`automations/README.md`](automations/README.md)

## Customize it

Three levers, easiest first:

1. **Configuration** — `config/team-leader.yaml`, `team-data/team.yaml`,
   `config/coaching.yaml`. Identity, goals, KPIs, roster, coaching style, permissions.
2. **Instructions** — edit [`AGENTS.md`](AGENTS.md). Plain English. Change the tone, add a
   rule, add a boundary.
3. **Skills** — add a directory under `skills/` with a `SKILL.md`. See
   [`skills/README.md`](skills/README.md).

## Local AI for loan documents

Optional, and the reason this repository exists in its current form.

```bash
brew install llama.cpp
python3 scripts/local_ai/setup_local_ai.py
python3 scripts/local_ai/server.py start
python3 scripts/local_ai/review.py examples/synthetic-documents/synthetic-paystub.pdf
```

That last command reviews a **fictional** paystub included in this repository, so you can
watch the whole pipeline work before pointing it at anything real.

With **Local Privacy Mode** on (the default), borrower documents are processed entirely on
your machine. If a local step fails, the system stops and tells you — it never quietly
sends your document to a cloud service.

Read: **[docs/local-ai/](docs/local-ai/README.md)** · what was actually tested:
**[local-ai/VALIDATION.md](local-ai/VALIDATION.md)**

## Keeping your information private

This repository is **public**. Your team's information must never end up in it.

| Location | Contents | Committed? |
|---|---|---|
| `team-data/` | Your roster, coaching notes, scorecards | **Never** |
| `local_data/` | Borrower documents, model weights, audit log | **Never** |
| `config/*.yaml` | Your filled-in configuration | **Never** |
| `.env` | API keys | **Never** |
| `config/*.example.yaml` | Fictional templates | Yes |

Check before every commit:
```bash
python3 scripts/privacy_scan.py
```

**Never put in GitHub:** borrower documents or data, Social Security numbers, credit
reports, bank statements, income documents, your real roster, API keys, tokens, passwords,
private emails, or production exports. See [SECURITY.md](SECURITY.md).

## Connecting other tools

**Honestly: this repository ships no working connector to Gmail, Google Calendar, your
CRM, or your LOS.** Nothing here logs into anything.

What works today is local files and pasting. Exporting a pipeline report and pasting it is
the most reliable integration available, and it is what the automations assume.
[`config/integrations.example.yaml`](config/integrations.example.yaml) is where real
connectors get declared once built. See [docs/integrations.md](docs/integrations.md).

## Updating

```bash
git pull
python3 scripts/sync_agent.py
python3 scripts/validate.py
```

Your configuration is gitignored, so a pull never overwrites it. Skills load directly from
the repository, so a pull updates them with no further action.

## Troubleshooting

- General: [docs/troubleshooting.md](docs/troubleshooting.md)
- Local AI: [docs/local-ai/troubleshooting.md](docs/local-ai/troubleshooting.md)
- Check the build: `python3 scripts/validate.py`

## Extending it with a coding assistant

This repository is designed to be handed to Claude Code, Codex, or Hermes itself. Point
them at [`PROJECT_STATUS.md`](PROJECT_STATUS.md) — it records the architecture, the
decisions, what is tested, and what is not.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Improvements to skills, automations, and coaching
frameworks are welcome. Never contribute anything containing real borrower, employee, or
candidate information.

## Important limitations

This system is an **assistant**. It is not the underwriter, the lender, the compliance
department, an attorney, an accountant, the credit bureau, or the insurer.

It does not make lending decisions. It does not calculate qualifying income. It does not
quote rates. Document extraction can misread figures, especially from scans — **every
number it reports must be verified by a person.**

Mortgage guidelines change. Anything it tells you about a guideline must be checked against
the current authoritative source.

## License

MIT — see [LICENSE](LICENSE). Bundled models are Apache-2.0; Hermes Agent is MIT.
