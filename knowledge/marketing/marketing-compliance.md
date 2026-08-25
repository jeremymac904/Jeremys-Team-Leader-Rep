# Marketing compliance guardrails

**Read this before generating any outward-facing content.** Every marketing skill applies
it. It is a content-safety guide, not a substitute for your company's compliance approval.

## Five content categories, never blurred

| Category | Example | Exposure |
|---|---|---|
| **Educational** | "Here is how a seller credit generally works" | Lowest |
| **General marketing** | "I help buyers understand their options" | Low |
| **Loan program marketing** | "What VA buyers should know" | Moderate — program claims |
| **Rate-related marketing** | Anything with a rate, APR, payment, or fee | **Highest — triggers disclosure requirements** |
| **Customer-specific** | A message about a real borrower's file | Not marketing. Private. |

Every generated piece must be labeled with its category so the reviewer knows what they
are looking at.

## Never generate

- A rate, APR, monthly payment, points, fees, closing costs, savings figure, or
  down-payment amount — **unless** the Loan Officer supplies compliance-approved terms
  *and* all required disclosures
- A guarantee of approval, eligibility, closing time, savings, payment reduction, rate, or
  program fit
- "Everyone qualifies", "credit doesn't matter", "no income review", "instant approval"
- Advice to hide debts, misstate facts, or conceal occupancy intent
- Anything implying FHA, VA, or USDA means government endorsement of the lender
- Fear-based urgency — "rates explode tomorrow", "buy now or never"
- Targeting or excluding people by any protected characteristic
- Tax, legal, credit-repair, or investment advice
- Attacks on named competitors or unsupported comparisons
- Any non-Loan Factory mortgage brand, prior DBA, or separate team identity

## Safe language

> "For qualified borrowers." · "Subject to approval." · "Based on current market
> conditions." · "Depending on borrower eligibility, property type, documentation, and
> lender availability." · "Let's review your scenario before assuming what is possible."
> · "Your actual options depend on a complete application and underwriting review."

## The rate guardrail

General education about how rates, APR, buydowns, credits, or costs *work* is fine.

**Specific advertised terms require the full disclosure set.** If those disclosures are not
available, leave the numbers out and invite a private review instead. This is the single
most common way marketing content becomes a compliance problem.

## Specialty programs

For DSCR, non-QM, investor, and fix-and-flip content: state that programs vary by lender
and scenario. Never imply that income, credit, appraisal, reserves, entity type, property
condition, or exit strategy is irrelevant. Never promise financing before eligibility and
underwriting review.

## Required disclosure

When content discusses mortgage options, qualification, programs, pre-approval,
application, or payment planning, it needs a disclosure footer. The default:

> This is not a commitment to lend. All loans subject to approval. Terms and conditions
> apply.

**This text is configurable** in `config/marketing.yaml` under `compliance.disclosure`,
because the required wording varies by company and state. Licensing identifiers — company
NMLS, Loan Officer NMLS, Equal Housing language, state disclosures — come from
`config/team-leader.yaml` and each Loan Officer's profile. **Nothing is hardcoded.**

## Pre-publish checklist

Every generated piece carries this:

- [ ] Loan Factory branding only
- [ ] No rate, APR, payment, fee, or savings claim without required disclosures
- [ ] No approval, eligibility, or guarantee language
- [ ] No protected-class targeting
- [ ] No tax, legal, credit, or investment advice
- [ ] Correct disclosure footer for the content category
- [ ] Human tone with a practical next step
- [ ] **Reviewed and approved by a human before publishing**

## The agent's limit

The agent **flags**. It does not **clear**. Nothing it produces is approved advertising
until a person — and where your company requires it, compliance — approves it. The agent
never publishes.
