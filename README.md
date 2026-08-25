<img src="assets/branding/loan-factory-logo-360w.png" alt="Loan Factory" width="220">

# Loan Factory Team Leader OS

**An AI assistant that knows you, knows your team, and helps you lead them.**

> ### 👉 New here? Read **[START HERE](START-HERE-LOAN-FACTORY-TEAM-LEADERS.md)**
> Five steps, about ten minutes, no technical background needed.

---

## What is this?

A **customization package** for [Hermes Agent](https://github.com/NousResearch/hermes-agent),
a free AI assistant that runs on your own computer.

Hermes on its own is a general assistant. This package turns it into a **Loan
Factory Team Leader's assistant** — 35 skills, coaching frameworks, 46
automation recipes, prompts, and templates, all built around the actual job of
leading a mortgage team while still closing your own loans.

You install Hermes normally. You download this folder. Hermes reads it. That's the
whole architecture.

## What does it help me do?

**Lead the day**
- A ranked morning briefing — the three things that actually need you
- Pipeline review: stalled files, closings at risk, borrowers gone silent
- Your own weekly and monthly review, including your own production

**Coach**
- One-on-one prep with the diagnosis already done
- 30/60/90 development plans — ramp, recovery, or growth
- Live sales role-play, scored, with an exact rewrite of your weakest line
- Team meeting agendas built from this week's real pattern

**Grow the team**
- Recruiting pipeline, interview prep, candidate comparison
- Referral partner review, including the agent who quietly stopped referring
- Marketing plans matched to how each Loan Officer actually works

**Find leverage**
- 46 automation recipes, all inactive until you choose one
- An advisor that will tell you when something should *stay* manual

**Optional: private document review** — read paystubs, W-2s, bank statements,
and contracts entirely on your own machine, so borrower data never reaches a
cloud AI service.

## What do I install?

| Step | What |
|---|---|
| 1 | **Hermes Agent** — the official installer, one command |
| 2 | **This package** — `git clone`, one command |
| 3 | **`hermes skills trust`** — one command, run inside the folder |

That's it. No developer tools, no build step, no configuration files to hand-edit.

## What folder do I open?

The folder this repository creates. Start Hermes **from inside it**:

```bash
cd ~/Documents/Jeremys-Team-Leader-Rep
hermes
```

Being inside the folder is how Hermes knows this is your Team Leader project.

## What command do I run?

```bash
# once, to set up
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes setup
git clone https://github.com/jeremymac904/Jeremys-Team-Leader-Rep.git
cd Jeremys-Team-Leader-Rep
hermes skills trust
python3 scripts/setup.py

# every time after that
cd ~/Documents/Jeremys-Team-Leader-Rep
hermes
```

## What should I ask first?

> **Give me my Team Leader morning briefing.**

Then:

> Help me coach a Loan Officer who is struggling with Realtor outreach.
> Build my next team meeting agenda.
> Tell me the five highest value automations I should implement first.
> Create a 30 day marketing plan for one of my Loan Officers.
> Help me recruit and onboard a new Loan Officer.

Full walkthrough: **[START HERE](START-HERE-LOAN-FACTORY-TEAM-LEADERS.md)**

---

## Is my team's information private?

Yes. Your configuration and roster live in files that Git is told to ignore:

| Stays on your computer | Shared publicly |
|---|---|
| `team-data/` — your roster, coaching notes | The skills and frameworks |
| `config/*.yaml` — your settings | Fictional example configs |
| `local_data/` — any documents you review | Nothing from here, ever |

Check any time:

```bash
python3 scripts/privacy_scan.py
```

**Never put in a public repository:** borrower documents, Social Security
numbers, credit reports, your real roster, or API keys. See
[SECURITY.md](SECURITY.md).

## What's in the package

| | |
|---|---|
| **[35 skills](.hermes/skills/README.md)** | 14 team leadership · 10 marketing · 11 mortgage documents |
| **[46 automations](automations/README.md)** | All inactive by default |
| **[Coaching frameworks](coaching/README.md)** | Diagnosis, scorecards, weekly rhythm, scripts, partner strategy |
| **[Marketing knowledge](knowledge/marketing/README.md)** | Content strategy, brand voice, compliance, campaigns |
| **[Prompt library](prompts/README.md)** | For the situations between the scheduled work |
| **[Templates](templates/README.md)** | Scorecards, prep sheets, development plans, agendas |

## Customizing it

Three levers, easiest first:

1. **Answer the setup questions** — `python3 scripts/setup.py`
2. **Edit the instructions** — [`AGENTS.md`](AGENTS.md) is plain English. Change
   the tone, add a rule, add a boundary.
3. **Add a skill** — see [`.hermes/skills/README.md`](.hermes/skills/README.md)

## Optional: private local document review

Not part of getting started, and not needed for anything above.

An add-on that runs an AI model **on your own computer** so borrower documents
never leave it. Reads paystubs, W-2s, bank statements, tax returns, purchase
contracts, Loan Estimates, and Closing Disclosures — including scanned ones.

It needs a multi-gigabyte model download and a few extra Python packages. Set it
up when you actually want it: **[docs/local-ai/README.md](docs/local-ai/README.md)**

Note: the local model is for **document review**, not for chatting with Hermes.
Keep using your normal cloud provider for conversation — see
[docs/hermes.md](docs/hermes.md#optional-running-a-model-locally).

## Updating

```bash
git pull
```

Your configuration and roster are never overwritten.

## Documentation

- **[START HERE](START-HERE-LOAN-FACTORY-TEAM-LEADERS.md)** — the walkthrough
- [All documentation](docs/README.md)
- [Troubleshooting](docs/troubleshooting.md)
- [How Hermes and this package fit together](docs/hermes.md)
- [Before activating an automation](docs/automation-safety.md)
- [What the agent will not do](docs/mortgage-compliance.md)

## Important limitations

This is an **assistant**. It is not the underwriter, the lender, the compliance
department, an attorney, or an accountant.

It does not make lending decisions, calculate qualifying income, or quote rates.
Document extraction can misread figures, especially from scans — **verify every
number.** Mortgage guidelines change; anything it says about one must be checked
against the current source.

## License

MIT — see [LICENSE](LICENSE). Hermes Agent is MIT. Bundled model
recommendations are Apache-2.0.
