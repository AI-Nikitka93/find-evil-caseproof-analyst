# Product Anchor

Date locked: 2026-05-06  
Project name: CaseProof Analyst  
Contest: FIND EVIL!

## One-Liner

CaseProof Analyst is a machine-speed first responder with human-grade evidence discipline: it investigates real SIFT evidence autonomously, but releases only evidence-checked findings with visible self-correction, traceable evidence references, and an honest accuracy/trust package.

## Core Value

Give an incident responder a fast first triage without accepting unsupported AI conclusions.

The product must help a practitioner move quickly while preserving forensic trust:

- every confirmed finding must connect to concrete evidence;
- unsupported claims must be rejected, downgraded, or marked for human review;
- self-correction must be visible in the run artifacts;
- uncertainty must remain explicit;
- original evidence must remain read-only by product boundary.

## Core User

Primary user:

- DFIR / incident response practitioner who needs a defensible first triage of case evidence.

Primary judge user:

- FIND EVIL! judge evaluating autonomous execution, IR accuracy, constraint implementation, audit trail quality, and usability.

Secondary users:

- senior analyst reviewing first-pass conclusions;
- junior analyst learning how evidence-backed investigation is sequenced;
- open-source contributor extending the project without weakening the trust model.

## Correct End-State

The first full release is correct only when it can be used without manual unfinished work to:

- run against real SIFT-compatible evidence;
- show an autonomous investigation sequence;
- show at least one real or controlled self-correction sequence;
- generate an analyst-readable report;
- generate an evidence book;
- generate a correction ledger;
- generate an accuracy report based on real validation;
- generate replayable execution logs;
- preserve original evidence as input-only;
- package all required contest submission artifacts honestly.

## Do Not Drift Into

The project must not drift into:

- a generic AI security chatbot;
- broad wrapping of all SIFT tools before the first evidence lane is trusted;
- prompt-only evidence safety;
- synthetic-only demo or synthetic-only accuracy claim;
- a decorative dashboard that hides missing real validation;
- unsupported claims presented as confirmed findings;
- public copy that overstates readiness;
- runtime-provider exploration as a substitute for DFIR product value.

## Product Scope Stop Rule

A new task, feature, or document belongs in the first release only if it strengthens at least one of these:

- real evidence validation;
- visible self-correction;
- evidence traceability;
- architectural evidence safety;
- accuracy reporting;
- execution-log replayability;
- required contest submission readiness;
- practitioner usability.

If it does not strengthen one of those, it belongs in future scope or out of scope.

See also: [`scope_stop_rule.md`](scope_stop_rule.md).

## First-Release Shape

Recommended shape: terminal-first autonomous investigation product with generated evidence dossier.

Required output surfaces:

- analyst report;
- evidence book;
- correction ledger;
- accuracy report;
- execution logs;
- dataset documentation;
- architecture/trust-boundary documentation;
- public README and submission story.

A full visual cockpit is not part of the first release unless the evidence workflow is already validated.
