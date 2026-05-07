# Audience And Positioning

Updated: 2026-05-06  
Purpose: close TODO T011 and T012.

## Practitioner-Facing Positioning

CaseProof Analyst helps a responder get a defensible first triage faster, without accepting unsupported AI claims.

For a practitioner, the product is useful because it:

- starts from real case evidence, not from generic security advice;
- keeps original evidence as input-only;
- sequences a narrow disk-triage investigation without requiring manual command selection for every step;
- converts raw forensic observations into candidate claims;
- checks candidate claims before they become confirmed findings;
- shows rejected, downgraded, and uncertain claims instead of hiding them;
- gives the analyst a report that can be reviewed from summary down to evidence;
- leaves execution logs that support peer review and later case reconstruction.

The product promise for responders:

> Fast first triage without accepting unsupported AI findings.

The product is not a replacement for a senior analyst. It is a disciplined first responder that accelerates the early investigative pass while preserving the evidence trail a senior analyst needs for review.

## Audience Separation

| Audience | Primary question | Product answer | Required artifact |
|---|---|---|---|
| Judge | Does this agent really self-correct and preserve evidence integrity? | Show real evidence run, visible correction, architectural safety boundary, and traceable logs. | Demo video, architecture diagram, accuracy report, execution logs. |
| Responder | Can this give me a trustworthy first triage faster? | Provide analyst report, evidence book, uncertainty labels, and safe run instructions. | README, analyst report, evidence book, correction ledger. |
| Senior reviewer | Can I audit the conclusions without trusting the model blindly? | Link each finding to evidence references and tool execution records. | Evidence book, execution logs, accuracy report. |
| Open-source contributor | Can I extend this without weakening the trust model? | Explain scope boundary, no-confirmed-without-evidence rule, and contribution guardrails. | Product anchor, architecture docs, contribution guidance. |

## Audience-Specific Success Signals

Judge success:

- understands the project in one sentence;
- sees a live self-correction sequence;
- can trace a finding to a specific action;
- sees why Custom MCP safety is stronger than prompt-only safety.

Responder success:

- can run or inspect the project without private context;
- gets a clear first-pass narrative;
- sees what was checked and what remains unknown;
- can avoid acting on unsupported AI claims.

Senior reviewer success:

- can challenge a conclusion;
- can inspect the supporting evidence chain;
- can see parser failures and uncertainty;
- can separate confirmed facts from inferences.

Contributor success:

- understands why the first release is narrow;
- knows that broad tool wrapping is deferred;
- preserves the read-only evidence boundary;
- does not add features that bypass verification.

## Language Rules For Public Copy

Use:

- evidence-backed;
- self-correcting;
- read-only evidence boundary;
- traceable findings;
- honest accuracy report;
- first triage;
- unsupported claims rejected or downgraded.

Avoid unless real validation supports it:

- production-grade accuracy;
- complete DFIR platform;
- full SIFT coverage;
- guaranteed detection;
- replaces human analysts;
- real-world benchmark proven.
