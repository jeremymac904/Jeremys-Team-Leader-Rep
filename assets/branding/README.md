# Brand assets

## Loan Factory logo

`loan-factory-logo-transparent.png` is the **approved official Loan Factory logo**,
supplied for this project by the repository owner.

| File | Size | Purpose |
|---|---|---|
| `loan-factory-logo-transparent.png` | 900 × 300, RGBA | **The original. Do not modify.** |
| `loan-factory-logo-360w.png` | 360 × 120, RGBA | Scaled derivative for README and docs |

The derivative is a straight proportional downscale — no recolouring, cropping, or
restyling. The original is preserved untouched.

## Rules

- **Do not modify the original.** If you need another size, generate a new derivative
  file and leave `loan-factory-logo-transparent.png` alone.
- **Do not create unofficial variations.** No recolouring, no added text, no lockups with
  other marks, no restyled versions. Something that looks official but is not causes real
  problems for a regulated brand.
- **Do not imply endorsement.** This repository is a Team Leader's working toolkit. The
  logo marks it as Loan Factory-related; it does not make its output official Loan Factory
  material.
- **Loan Factory branding only.** The brand knowledge in
  [`../../knowledge/marketing/brand-voice.md`](../../knowledge/marketing/brand-voice.md)
  is explicit that individual team DBAs, prior group identities, and non-Loan Factory
  mortgage brands are not used in marketing content.

## Adding your own team assets later

Approved team assets go in `assets/team/`, which is gitignored — your team's graphics are
yours and may be licensed, so they do not belong in a public repository.

```bash
mkdir -p assets/team
cp ~/my-team-logo.png assets/team/
```

Point `config/marketing.yaml` at them under `brand.assets`.
