# Unsafe Action Refusal Story

Date: 2026-05-06

Purpose: define how destructive or unsafe requests become visible blocked events instead of hidden behavior.

## Product Story

When the agent asks for an unsafe action, CaseProof Analyst must not silently ignore it and must not pretend it succeeded.

The product should expose the refusal as part of the trust story:

```text
Unsafe action requested -> action not routable through MCP tools -> refusal/correction logged -> final report does not rely on it.
```

## Unsafe Requests

Unsafe requests include:

- delete original evidence;
- overwrite original evidence;
- write output into `evidence/`;
- run arbitrary shell commands;
- bypass `verify_claim`;
- mark a synthetic fixture as real validation;
- continue after parser failure as if results were complete.

## Required Behavior

| Situation | Required behavior |
|---|---|
| Agent asks for destructive action | Reject because no public tool supports it. |
| Agent gives path outside workspace for generated output | Reject through workspace path validation. |
| Agent tries to use different image path after case registration | Reject because image must match registered read-only evidence. |
| Tool binary is missing | Return visible tool-level failure; do not fabricate results. |
| Parser output is partial | Mark parser status partial and keep uncertainty visible. |
| Claim has no evidence support | Mark unsupported or needs human review; do not place in confirmed findings. |

## Visible Artifacts

Unsafe-action handling should appear in:

- execution log;
- correction ledger or dropped-claim section;
- final report limitations if the unsafe/failed action affected coverage;
- accuracy report when the event is part of validation.

## Current Local Proof

Current local proof exists through:

- no generic shell tool in the public MCP surface;
- path traversal test;
- missing SIFT binary test;
- append-only execution log test;
- preflight evidence/workspace separation check;
- release-control audit.

## Real-Run Proof Still Needed

A final demo-quality refusal story still needs a real or controlled run artifact that shows:

- unsafe or unsupported request;
- visible rejection/correction;
- final report excluding the unsupported result.

## Acceptance

This story is complete for the current phase because it defines the visible behavior and maps it to tested controls. It does not claim that a real `.E01` run has already produced the refusal event.
