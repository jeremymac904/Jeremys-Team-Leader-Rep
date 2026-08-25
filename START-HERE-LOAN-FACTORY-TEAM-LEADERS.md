<img src="assets/branding/loan-factory-logo-360w.png" alt="Loan Factory" width="200">

# Start here

Five steps. About ten minutes. You do not need to know anything about
programming, Git, or AI.

At the end you will have an AI assistant that knows you, knows your team, and
can coach, plan, and prepare your week.

---

## Step 1 — Install Hermes

Hermes is the AI assistant program. It runs on your own computer.

Open the **Terminal** app and paste this in, then press Return:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

*(On Windows, open PowerShell and run:*
`irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1 | iex`*)*

It takes a few minutes. When it finishes, close Terminal and open a new one.

Then connect it to an AI model:

```bash
hermes setup
```

It will ask which AI provider you want to use and walk you through it. Pick
whichever you already have an account with. If you have none, it will offer
options — any of them work.

---

## Step 2 — Download the Team Leader package

```bash
cd ~/Documents
git clone https://github.com/jeremymac904/Jeremys-Team-Leader-Rep.git
```

This creates a folder called `Jeremys-Team-Leader-Rep` in your Documents.
That folder is the Team Leader package: skills, coaching frameworks,
automations, and templates.

---

## Step 3 — Open the folder in Hermes

```bash
cd ~/Documents/Jeremys-Team-Leader-Rep
hermes skills trust
```

That second command tells Hermes it is allowed to use the skills in this
folder. You should see:

```
35 project skill(s) will load in sessions started inside this repo
```

**That is the whole integration.** Nothing is copied or installed. Hermes
reads the folder directly, so when you update the package later your skills
update with it.

---

## Step 4 — Tell it about you and your team

```bash
python3 scripts/setup.py
```

It asks a short list of questions — your name, your team, your market, your
goals, how you like to coach and communicate. Press Return to accept any
default you do not care about.

Then open the roster file it created and put your real team in it:

```
team-data/team.yaml
```

For each person the fields that matter most are:

- `experience_level` — `new`, `developing`, `established`, or `top-producer`
- `development_areas` — what they actually struggle with, specifically

**Your answers stay on your computer.** `team-data/` and your configuration
files are excluded from Git, so nothing about your team is ever uploaded
anywhere.

---

## Step 5 — Start using it

**Important: start Hermes from inside the folder.** That is how it knows this
is your Team Leader project.

```bash
cd ~/Documents/Jeremys-Team-Leader-Rep
hermes
```

Then ask it something real:

> **Give me my Team Leader morning briefing.**

---

## Your first 10 minutes

Try these in order. Each one shows a different thing it can do.

**1. See what it knows**
> Give me my Team Leader morning briefing.

It will tell you what data it has and what it is missing. That is correct — it
does not invent numbers.

**2. Coach someone specific**
> Help me coach a Loan Officer who is struggling with Realtor outreach.

**3. Prepare your week**
> Build my next team meeting agenda.

**4. Find time savings**
> Tell me the five highest value automations I should implement first.

**5. Marketing for one person**
> Create a 30 day marketing plan for one of my Loan Officers.

**6. Hiring**
> Help me recruit and onboard a new Loan Officer.

Push back on the answers. Tell it *"that's generic — which of these actually
applies to a 5-month LO?"* and it will get more specific.

---

## What it will never do on its own

- Send an email or message to anyone
- Contact a borrower, Realtor, or candidate
- Change anything in your CRM or LOS
- Post or publish anything
- Make a lending, credit, or approval decision
- Quote a rate

It prepares. You review. You decide.

---

## Common problems

**"command not found: hermes"** — close Terminal and open a new one. The
installer adds Hermes to your path, and existing windows do not see it.

**"0 project skills"** — you are not inside the folder. Run
`cd ~/Documents/Jeremys-Team-Leader-Rep` first, then `hermes`.

**It says it does not know my team** — you have not filled in
`team-data/team.yaml` yet, or you started Hermes from a different folder.

**It used a fictional team** — same cause. It falls back to a sample team and
tells you when it does.

More: [docs/troubleshooting.md](docs/troubleshooting.md)

---

## Optional, for later

**Private document review.** There is an optional add-on that reads paystubs,
W-2s, bank statements, and contracts **entirely on your own computer**, so
borrower information never reaches a cloud AI service. It needs a large
download and a bit more setup, and it is not part of getting started.

When you want it: [docs/local-ai/README.md](docs/local-ai/README.md)

---

## Updating later

```bash
cd ~/Documents/Jeremys-Team-Leader-Rep
git pull
```

Your configuration and team roster are never touched by an update.
