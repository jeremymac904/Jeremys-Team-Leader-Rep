# Your first hour

You do not need to understand the whole repository to get value. This is the shortest path
to something useful.

## 0–10 min — install

```bash
git clone https://github.com/jeremymcdonald-prog/Jeremys-Team-Leader-Rep.git
cd Jeremys-Team-Leader-Rep
bash scripts/install_hermes.sh
python3 scripts/setup.py
bash scripts/hermes.sh setup      # choose a model
```

## 10–20 min — add your team

Open `team-data/team.yaml`. Replace the fictional Northstar Lending Team with your real
people. For each, the fields that change the coaching are:

- `experience_level` — `new`, `developing`, `established`, or `top-producer`
- `development_areas` — what they actually struggle with, specifically
- `goals`

That file is gitignored. It never reaches GitHub.

## 20–25 min — first briefing

```bash
bash scripts/hermes.sh
```

Ask:

> Give me my Team Leader morning briefing.

It will tell you what data it has and what it is missing. That is correct behavior — it
does not invent numbers.

## 25–35 min — a real pipeline review

Export your pipeline from your LOS or CRM. Useful columns: file ID, assigned LO, stage,
days in stage, contract closing date, last borrower contact, conditions outstanding.

Paste it and ask:

> Run a pipeline review on this export. Flag closings within 10 days with conditions
> outstanding, files past our 3-day borrower contact SLA, and stages running long.
> Group by LO.

This is usually the moment the system proves itself.

## 35–45 min — prepare a real one-on-one

Pick someone you are coaching this week. Paste their recent numbers:

> Prep my one-on-one with [name]. Here are their numbers: [paste]. Diagnose which funnel
> stage is actually broken, pick one skill to drill, and give me the questions to ask.

Notice it tells you what the problem is *not*. That is usually the useful part.

## 45–55 min — try a role-play

> Role-play with me. You are a Realtor who already has a lender. Difficulty: difficult.
> Stay in character until I say stop, then score me and rewrite my weakest line.

Now you know what to hand your team.

## 55–60 min — pick one automation

Open [`automations/README.md`](../automations/README.md) and choose one. Copy its prompt.
That is the entire installation for most of them.

Good first choices: `daily-morning-brief`, `pipeline-weekly-review`,
`meeting-weekly-agenda`.

---

## If you want local document review

Separate, optional, and worth 20 minutes:

```bash
brew install llama.cpp
python3 scripts/local_ai/setup_local_ai.py
python3 scripts/local_ai/server.py start
python3 scripts/local_ai/review.py examples/synthetic-documents/synthetic-paystub.pdf
```

That reviews a fictional paystub included here. Once you have seen it work, point it at a
real document in `local_data/borrower_documents/` — which never leaves your machine.

## What to do next

- Edit [`AGENTS.md`](../AGENTS.md) if the tone is not yours
- Read [automation-safety.md](automation-safety.md) before scheduling anything
- Read [privacy.md](privacy.md) before adding real data
