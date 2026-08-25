# team-data — your private information

**Nothing in this folder is ever committed.** It is gitignored, except this README.

Your real roster contains names, emails, phone numbers, and NMLS IDs. Your coaching notes
are employee performance records. Neither belongs in a public repository.

## What goes here

| File or folder | Contents |
|---|---|
| `team.yaml` | Your real roster, standards, and recruiting pipeline |
| `coaching/` | One-on-one prep sheets and session recaps |
| `scorecards/` | Weekly scorecards per Loan Officer |
| `notes/` | Anything else — partner lists, pipeline exports, working notes |

## Getting started

`scripts/setup.py` creates `team-data/team.yaml` from the fictional template. Open it and
replace the Northstar Lending Team with your own people.

```bash
cp config/team.example.yaml team-data/team.yaml
```

## What the agent does with this

It reads these files to answer questions about your team — who needs coaching, who has gone
quiet, what to cover in the next meeting. It will not copy anything from here into a
tracked file, an example, or anything shareable.

## Checking

```bash
git status              # nothing from team-data/ should appear
python3 scripts/privacy_scan.py
```
