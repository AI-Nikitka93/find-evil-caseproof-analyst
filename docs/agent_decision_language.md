# Agent Decision Language

Purpose: standardize claim labels so reports, correction ledgers, accuracy
summaries, and demo narration use the same truth language.

## Labels

| Label | Meaning | Allowed in final confirmed findings |
|---|---|---:|
| Confirmed | `verify_claim` returned confirmed and supporting evidence references exist. | Yes |
| Inferred | Evidence is related but incomplete, indirect, or not strong enough for confirmed. | No |
| Unsupported | Evidence was checked and did not support the claim. | No |
| Needs human review | Evidence is missing, ambiguous, conflicted, or parser output is not reliable enough. | No |
| Dropped | Claim is excluded from findings because support is absent or unsafe to infer. | No |
| Corrected | Claim changed after verifier challenge, parser failure, conflict, or bounded follow-up. | Only if re-verified as Confirmed |

## Required Wording Discipline

- Use `Confirmed` only when evidence support is explicit.
- Use `Inferred` when the analyst should see a lead but not treat it as fact.
- Use `Unsupported` before `Dropped` when the product checked evidence and found
  no support.
- Use `Needs human review` when the product cannot safely resolve the claim.
- Use `Corrected` only when the before-and-after state is visible.

## Forbidden Wording

- Do not call a claim "likely confirmed".
- Do not call an unsupported claim "maybe true".
- Do not hide unsupported claims from the output trail.
- Do not use confident language when parser status is failed or partial.
