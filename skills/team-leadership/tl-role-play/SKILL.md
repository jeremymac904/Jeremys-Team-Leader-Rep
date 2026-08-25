---
name: tl-role-play
description: "Run a live sales role-play as the borrower, Realtor, or candidate, then score it against a rubric."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [team-leader, coaching, sales, training, role-play]
---

# Sales Role-Play

## Purpose
Give Loan Officers live reps. Talking about a script does not build the skill; saying it
out loud under mild pressure does. You play the other side, stay in character, then score.

## When Hermes should use it
Use when a Loan Officer needs live practice — in a one-on-one, a team meeting, or on
request. Prefer it over explaining a script.
## Required information
- Scenario type: buyer consultation, rate objection, "I'm already working with someone,"
  Realtor first call, agent objection, past-client reactivation, recruiting conversation
- Difficulty: warm / neutral / difficult
- The LO's development areas from the roster
- Optionally a script from `coaching/frameworks/` to practice against

## Tools and commands it may use
Conversation only. No contact with any real person. No CRM/LOS access.

## Safety boundaries
None — this is entirely simulated. Every character is fictional.

## Human approval requirements
None.

## Workflow
1. Confirm scenario, difficulty, and what specifically is being drilled.
2. State the setup in two lines, then **stay in character**. Do not narrate, do not coach
   mid-scene, do not break to explain.
3. Play realistically for the difficulty level. Difficult means genuinely resistant —
   vague answers, price pressure, "let me think about it" — not abusive.
4. End the scene when the LO either gets the commitment, loses the prospect, or calls time.
5. Then, and only then, score against the rubric below.
6. Offer one specific rewrite of the single weakest moment, with the exact words.
7. Offer to run it again at the same or higher difficulty.

## Evidence rules
Feedback quotes what the LO actually said. "You said 'we have great rates' — that is a
claim, not a question" is coaching. "Be more consultative" is not.

## Expected output
```
SCENARIO: <type> — <difficulty>
Drilling: <the specific skill>

--- SCENE ---
<in character, no narration>

--- SCORE ---
Opened / earned the right to ask         [ /5 ]
Discovery before pitching                [ /5 ]
Handled the objection without arguing    [ /5 ]
Asked for a specific next step           [ /5 ]
Sounded human, not scripted              [ /5 ]

STRONGEST MOMENT
"<quote>" — why it worked

REWRITE THIS
You said: "<quote>"
Try:      "<exact replacement words>"
Because:  ...

RUN IT AGAIN? <same | harder>
```

## Stop conditions
Break character immediately if: the LO asks a real compliance or guideline question; the
scenario drifts toward quoting an actual rate to an actual borrower; or the LO asks for
help with a real live file. Answer that separately.

## Error behavior
If the scenario is underspecified, pick a sensible default, state the assumption in one
line, and start. Do not interview the user for five turns before beginning.

## Related skills
- `tl-lo-coaching-prep` — identifies which skill to drill
- `tl-training-plan` — team-level skill sessions

## What this skill must not assume
- **Do not assume the LO wants encouragement.** They asked for practice.
- **Do not assume a scripted answer is a good answer.**
- **Do not assume the scenario is hypothetical** — if it becomes a real live file, stop and say so.
- **Do not assume difficulty level** without asking.

## Tests
- Stays in character for the whole scene.
- Feedback quotes actual words spoken.
- Provides an exact replacement phrasing, not a general note.
- Never quotes a real rate.
