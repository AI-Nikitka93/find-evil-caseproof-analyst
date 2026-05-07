# DESIGN.md

## Product Summary

CaseProof Analyst is a terminal-first DFIR product for FIND EVIL judges and
incident responders. Its visual layer must make evidence discipline easier to
inspect, not make the product look like a decorative AI dashboard.

The design principle is: forensic clarity over decorative AI dashboard,
evidence-first reading, trust through hierarchy.

## Design Principle

- Evidence is the primary visual object.
- Claims never look stronger than their proof.
- Uncertainty, blocked states, parser degradation, and unsupported claims stay
  visible.
- The project must not get a plastic AI dashboard feeling: no glowing cards, no
  fake command centers, no decorative gradients, no green status theater.
- The visual system supports the terminal-first product and generated evidence
  dossier; it does not imply that a full cockpit exists.

## Visual Direction

The design should feel like a forensic case room: structured, calm, reviewable,
and serious. It should borrow the discipline of audit documents and security
operations tools without copying any third-party layout, wording, icons, or
brand.

Required tone:

- precise;
- restrained;
- evidence-first;
- readable under time pressure;
- honest about incomplete validation.

Avoid:

- generic AI assistant chat visuals;
- purple-blue AI gradients;
- glass panels;
- fake threat-map drama;
- oversized marketing hero treatment;
- status colors that hide blockers.

## Color Palette

tokens:

- evidence-ink: #101820
- paper: #F7F4ED
- panel: #FFFFFF
- boundary: #D8D2C4
- verified: #176B4D
- inferred: #8A5A00
- unsupported: #A33A2A
- blocked: #5A6472
- trace: #2F5D8C
- caution-fill: #FFF3D6

Usage:

- use evidence-ink for primary text;
- use paper for documentation background;
- use panel only for repeated evidence items and not as nested decoration;
- use verified only for evidence-linked confirmed findings;
- use inferred for supported but uncertain claims;
- use unsupported for dropped or rejected claims;
- use blocked for environment blockers and unsafe action refusals;
- use trace for links between finding, claim, evidence, action, and source.

## Typography

typography:

- headings: compact, clear, low-drama, sentence-readable;
- body: high legibility over personality;
- code and paths: monospace with wrapping;
- evidence IDs: monospace labels;
- status labels: short words, never full sentences inside pills;
- line length: optimized for repository markdown review and generated reports.

Do not use oversized hero typography inside report surfaces.

## Information Hierarchy

Primary reading order:

1. Current readiness truth.
2. Confirmed findings.
3. Evidence chain.
4. Correction ledger.
5. Limitations and unknowns.
6. Reproducibility path.

Every output surface must answer:

- what is claimed;
- what proves it;
- what was rejected or downgraded;
- what remains unknown;
- what the reviewer should inspect next.

## Report Surfaces

Final Analyst Report:

- executive summary first;
- confirmed findings separated from inferred findings;
- rejected claims and limitations visible;
- no raw log dump;
- no confident language without evidence references.

Evidence Book:

- one evidence record per reviewable item;
- clear source reference;
- extraction action;
- parser status;
- review note;
- link back to a finding.

Correction Ledger:

- original candidate claim;
- reason challenged;
- follow-up action;
- final disposition;
- language that does not look staged.

Real Run Accuracy Report:

- real dataset identity;
- methodology;
- false positives;
- missed artifacts;
- untested families and unknowns;
- rejected unsupported claims;
- fair baseline comparison only when reproducible evidence exists.

Judge Summary:

- what to inspect first;
- where self-correction appears;
- where evidence chain appears;
- how to separate historical synthetic fixture material from real-run output.

## Diagrams

Required diagram language:

- simple left-to-right flow;
- original evidence shown as input-only;
- server and forensic tools shown inside a read-only boundary;
- generated workspace shown separately;
- final outputs shown as report, evidence book, correction ledger, accuracy
  report, and execution logs;
- unsafe or destructive actions shown outside available capability.

Evidence chain diagram:

- Final finding;
- Candidate claim;
- Evidence record;
- Execution action;
- Source reference.

Correction loop diagram:

- Unsupported candidate;
- verifier challenge;
- targeted follow-up;
- corrected, downgraded, dropped, or human-review outcome.

## States And Edge Cases

Required states:

- no evidence file: show exact missing input and do not imply validation;
- missing SIFT runtime: show blocked environment without blaming the analyst;
- no confirmed finding: make absence explicit and point to inspected scope;
- parser partial output: show degraded artifact state;
- unsupported claim: show rejected or downgraded status;
- unsafe request: show refusal and safety boundary;
- real run not complete: keep synthetic fixture language separated.

## Components

components:

- evidence-card: evidence reference, source reference, artifact family, parser
  status, linked finding;
- finding-row: finding ID, status, confidence, evidence references;
- correction-row: candidate, challenge, follow-up, final disposition;
- readiness-strip: real validation status, blockers, next safe action;
- trace-link: finding to claim to evidence to action to source;
- limitation-callout: clear unknowns and untested families.

## Iconography Direction

Iconography is state labeling, not decoration. Text labels must stay visible
next to every symbol so meaning is not conveyed by color alone.

| State | Label | Symbol | Color token | Evidence rule |
|---|---|---:|---|---|
| evidence | Evidence | EVD | trace | Must point to a source reference. |
| correction | Correction | COR | caution-fill | Must show challenge and final outcome. |
| verified | Verified | VER | verified | Allowed only after evidence-linked verification. |
| inferred | Inferred | INF | inferred | Requires support plus visible uncertainty. |
| unsupported | Unsupported | UNS | unsupported | Must not appear as confirmed. |
| blocked unsafe action | Blocked Unsafe Action | BLK | blocked | Must name the unavailable unsafe capability. |
| human review | Human Review | HRV | blocked | Requires analyst review before promotion. |

## AI-Assisted Visual Asset Cycle

Production cycle:

1. Reference search for forensic, audit, and security documentation patterns.
2. Style brief based on this DESIGN.md.
3. Individual generation or drawing of one metaphor at a time.
4. Manual curation for meaning, line weight, consistency, and forensic tone.
5. AI critique against this design contract.
6. Rejection of artifacts that look decorative, misleading, or inconsistent.

No generated asset enters public docs unless it passes the full cycle.

## Fallback No-AI Visual Plan

The first-release fallback is clean typography, Mermaid diagrams, compact
tables, evidence IDs, and the text-symbol state catalog. If AI-generated
assets look cheap, noisy, or misleading, they are not used.

## Stitch Usage

This file is structured for Google Stitch or for an AI design agent to generate
documentation visuals and lightweight review surfaces. The generated output must
stay consistent with the terminal-first product and cannot imply a full visual
cockpit.

Stitch prompt anchor:

Use this DESIGN.md to create evidence-first DFIR documentation surfaces for
CaseProof Analyst. Prioritize report readability, traceability, correction
visibility, and honest blocked states. Avoid generic AI dashboard visuals.

## Accessibility And Repository Review

- Maintain high contrast for text and status labels.
- Do not use color as the only state cue.
- Keep diagrams readable in repository markdown.
- Make code paths wrap safely.
- Keep status labels short and stable.
- Avoid clipped text in narrow repository views.

## Non-goals

- Full visual investigation cockpit.
- Decorative AI command center.
- Marketing landing page as the primary surface.
- Copied security product screenshots.
- Generated images that hide real validation gaps.
- Visual polish used as a substitute for real evidence validation.
