# Spoliation Threat Model

Date: 2026-05-06

Purpose: explain, in product language, how an AI agent could damage evidence and how the current CaseProof Analyst boundary blocks that risk.

## Core Risk

Forensic value is lost if the original evidence can be modified, overwritten, deleted, mixed with generated output, or misrepresented as analyzed when it was not.

CaseProof Analyst treats evidence integrity as a product requirement, not a prompt preference.

## Threats And Controls

| Threat | How it could happen | Current control | Required visible result |
|---|---|---|---|
| Evidence overwrite | Agent writes logs, exports, or report into the evidence path. | Output paths are constrained to case workspace. | Run is blocked or redirected before evidence is touched. |
| Evidence deletion | Agent asks for cleanup or destructive command. | No generic shell/delete tool exists in the public MCP surface. | Unsafe request becomes a blocked/refused event. |
| Evidence mutation by tool | Tool family runs a mutating command or unsafe flag. | Fixed command families and argument-list execution only. | Unsafe command family is not routable. |
| Synthetic evidence overclaim | Fixture result is presented as real SIFT validation. | Docs and state separate synthetic and real validation. | Final submission remains no-go until real run. |
| Output/evidence mixing | Case workspace overlaps evidence folder. | Preflight checks workspace and evidence separation. | Preflight returns blocked. |
| Unsupported claim promotion | Agent states a conclusion without evidence. | `verify_claim` must run before confirmed findings. | Claim becomes confirmed, inferred, unsupported, or human-review. |
| Parser failure hidden | Tool failure is ignored and report still sounds confident. | Parser status and tool errors are surfaced. | Failure becomes uncertainty or correction trigger. |
| Raw output overload | Huge tool output causes context loss and sloppy conclusions. | Analyst-facing output is bounded; raw outputs stay in workspace. | Report remains explainable and traceable. |

## Current Proof Points

Current controls that can be checked locally:

- `.gitignore` excludes `evidence/`, `cases/`, fixtures, and local secret notes;
- `scripts/preflight_case.py` blocks missing evidence, tiny fixtures, overlapping paths, and missing SIFT runtime;
- `scripts/audit_release_controls.py` checks local-only rules, public tool stability, schema markers, and obvious public token leaks;
- `tests/test_server_contracts.py` checks path traversal rejection, missing-tool surfacing, and append-only logging;
- `tests/test_release_controls.py` checks release-control audit behavior.

## Remaining Real-Run Proof

The threat model is not fully proven against real evidence until:

- selected `.E01` exists locally;
- SIFT-compatible tools are available;
- real case workspace outputs are produced;
- execution log shows any unsafe/corrected/unsupported events from the real run;
- accuracy report is updated with real validation.

## Acceptance

This model is acceptable when it:

- identifies how evidence can be harmed;
- maps each risk to a current product control;
- keeps missing real validation visible;
- avoids claiming that absent evidence was tested.
