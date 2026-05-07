# Visual Asset Policy

Date: 2026-05-06

Purpose: define the visual state system and production rules for report/docs
assets without turning the product into a decorative dashboard.

## Iconography Direction

Icons are optional supporting labels. Text and evidence references remain the
primary meaning carriers.

State catalog:

| State | Label | Symbol | Rule | Usage |
|---|---|---:|---|---|
| evidence | Evidence | EVD | Must point to a source reference. | Evidence book and trace links. |
| correction | Correction | COR | Must show challenge and final outcome. | Correction ledger. |
| verified | Verified | VER | Only after evidence-linked verification. | Confirmed findings. |
| inferred | Inferred | INF | Requires support plus uncertainty. | Supported but uncertain findings. |
| unsupported | Unsupported | UNS | Must not appear as confirmed. | Dropped or rejected claims. |
| blocked unsafe action | Blocked Unsafe Action | BLK | Must name the unavailable unsafe capability. | Spoliation refusal states. |
| human review | Human Review | HRV | Requires analyst review before promotion. | Ambiguous or degraded evidence. |

Style rules:

- monoline or text-symbol marks only for the first release;
- consistent stroke weight if icons are later generated;
- no mascot, threat-map, glowing AI, or decorative command-center metaphor;
- no state conveyed by color alone;
- every symbol must have a text label next to it.

## AI-Assisted Asset Production Cycle

Reference search:

- collect forensic, audit, security, and documentation references only for
  evidence of patterns;
- record provenance and licensing status;
- reject any reference that would require copying another brand, layout, icon,
  screenshot, or text.

Style brief:

- define line weight, corner style, label behavior, color tokens, and forbidden
  metaphors before generating anything;
- use `DESIGN.md` as the source of truth.

Individual generation:

- generate or draw one metaphor at a time;
- never batch-generate an entire icon family and accept it unreviewed;
- compare every asset against the state catalog.

Manual curation:

- reject inconsistent line weight;
- reject unclear metaphors;
- reject visual noise;
- reject fake AI gloss;
- reject icons that can be confused with confirmed evidence.

AI critique:

- ask a separate critique pass to compare the candidate asset against
  `DESIGN.md`, the state catalog, and accessibility requirements;
- record only the decision and selected asset path, never secrets or prompts
  containing private paths.

Rejection rule:

- if an asset weakens forensic clarity, implies unavailable UI, hides a
  blocker, or looks decorative, it is rejected.

## Manual Metaphor Selection

Approved first-release metaphors:

- Evidence: source-linked record.
- Correction: challenged claim with visible final outcome.
- Verified: evidence-checked result.
- Inferred: supported but uncertain result.
- Unsupported: rejected or dropped claim.
- Blocked Unsafe Action: capability outside product boundary.
- Human Review: analyst decision required.

Each metaphor must preserve:

- the same compact tone;
- the same label style;
- the same evidence-first reading order;
- no unsupported claim as a success state.

## Fallback No-AI Visual Plan

Fallback no-AI visual plan:

- use clean typography;
- use Mermaid diagrams;
- use text-symbol labels from the state catalog;
- use tables and evidence IDs;
- avoid generated illustrations entirely until real assets pass review.

This fallback is the default for the first release unless generated assets pass
manual curation and AI critique.
