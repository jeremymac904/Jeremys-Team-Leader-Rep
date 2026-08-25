# AI and operations prompts

## Should I automate this?

> I do [task] about [N] times a week and it takes about [N] minutes. The input is
> [describe — where does it come from, is it structured?]. It ends in [a decision I have to
> make / a document / a message]. Should I automate it, assist it, or keep it manual? Be
> willing to tell me to keep it manual.

**"Keep it manual" is a legitimate answer.** Judgment-heavy, low-frequency work usually
should stay manual.

---

## Find the hours

> Here is everything I did this week: [list it]. Which of these did I do more than twice?
> For each repeat, tell me whether it should be automated, delegated, systematized, or
> eliminated — and show me the arithmetic on hours saved.

---

## Turn a good prompt into a reusable one

> I asked: [paste what you asked]. I got: [describe what came back]. I actually wanted:
> [describe]. Rewrite this as a reusable prompt with clear inputs I fill in each time, and
> tell me which file in `prompts/` it belongs in.

---

## Audit a workflow

> Here is our current [lead-to-close / follow-up / new hire onboarding] process, step by
> step: [describe each step and who owns it]. Where does it break, where is it duplicated,
> and what are the three highest-leverage fixes? Rank by effort-to-impact.

---

## Teach the team to use AI

> Build a 30-minute hands-on session teaching my LOs to use AI for [specific task]. Include
> the exact prompts they will copy, and a segment on what they must never paste into an AI
> tool — borrower PII, SSNs, credit reports, income documents. Do not skip that segment.

---

## Evaluate a tool

> I am considering [tool] for [purpose]. Cost: [amount]. What we do today: [describe]. What
> would actually have to be true for this to be worth it, what is the realistic adoption
> risk with a team of [N], and what is the cheapest way to test it before committing?
> Argue the case against it too.

---

## Design a new skill

> I want the agent to be able to [describe the job] reliably every time. Write it as a
> `SKILL.md` following the format in `agent/skills/` — purpose, inputs, allowed tools,
> permission requirements, approval requirements, workflow, evidence rules, output format,
> stop conditions, error behavior, and tests. Be strict about the stop conditions.

---

## Extend the system with a coding assistant

> I am using [Claude Code / Codex / another assistant] on this repository. I want to
> [describe the change]. Read `PROJECT_STATUS.md` and `docs/architecture.md` first, tell me
> which files this touches, and warn me about anything that would break `scripts/validate.py`
> or put private data into a tracked file.
