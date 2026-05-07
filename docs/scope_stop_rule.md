# Product Scope Stop Rule

Updated: 2026-05-06  
Purpose: close TODO T018.

## Rule

A new feature, task, artifact, or integration belongs in the first release only if it directly strengthens at least one of these outcomes:

- real SIFT-compatible evidence validation;
- visible self-correction;
- traceable findings;
- original-evidence safety;
- accuracy reporting;
- execution-log replayability;
- required contest artifact readiness;
- practitioner usability.

If it does not strengthen one of these outcomes, it is not part of the first release.

## Accept Into First Release

Accept the work if it:

- helps complete the real evidence run;
- makes unsupported claims easier to detect or reject;
- improves the evidence book;
- improves the correction ledger;
- improves the accuracy report;
- improves traceability from finding to evidence;
- clarifies safe setup and try-it-out instructions;
- removes public overclaiming;
- reduces judge setup failure;
- protects original evidence from mutation.

## Defer

Defer the work if it:

- adds a new evidence family before the first lane is validated;
- improves visual polish without strengthening reviewability;
- introduces a new runtime provider without tested adapter behavior;
- expands contributor convenience while final submission blockers remain open;
- adds broad platform features unrelated to the required contest package.

## Reject

Reject the work if it:

- exposes broad command execution;
- allows writes to original evidence;
- hides unsupported claims;
- presents synthetic fixture results as real accuracy;
- makes the demo look stronger than the software actually is;
- weakens the no-confirmed-finding-without-evidence rule.

## First-Release Decision Test

Before accepting any new task, answer:

1. Does this make the real evidence run more credible?
2. Does this make self-correction more visible?
3. Does this make findings more traceable?
4. Does this protect evidence integrity?
5. Does this close a required submission artifact?

If all five answers are no, the task is out of first-release scope.
