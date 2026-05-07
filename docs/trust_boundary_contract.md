# Trust Boundary Contract

Date: 2026-05-06

Purpose: keep the evidence-safety boundary in one judge-readable place.

## Contract

CaseProof Analyst uses a constrained Custom MCP Server boundary:

- no generic shell tool;
- fixed public forensic actions;
- original evidence is input-only;
- generated outputs go only into the case workspace;
- unsupported claims are blocked, downgraded, or marked for human review;
- parser and runtime failures become visible uncertainty, not silent success.

## Boundary Surfaces

| Surface | Allowed | Not allowed |
|---|---|---|
| Agent | Request typed evidence actions, verify claims, write report. | Execute arbitrary operating-system commands. |
| MCP server | Run fixed forensic command families through argument lists. | Expose broad shell execution or destructive actions. |
| Original evidence | Read as source input. | Modify, overwrite, delete, or use as output target. |
| Case workspace | Store reports, logs, exports, and generated indexes. | Become the source of truth for original evidence. |
| Final report | Present confirmed/inferred/unknown status with evidence links. | Present unsupported claims as confirmed facts. |
| Execution log | Preserve tool calls, parser status, corrections, and output references. | Hide failed or unsafe action attempts. |

## Fixed Forensic Actions

The first release exposes only:

```text
case_open_readonly
list_partitions
filesystem_inventory
build_timeline
extract_registry_persistence
extract_event_records
verify_claim
write_execution_log
```

## Evidence Rule

Original evidence must never be a write destination.

Generated outputs belong under:

```text
cases/<CASE-ID>/
```

or the configured case workspace.

## Refusal Rule

If the agent requests an unsafe action, the product should produce a visible blocked/unsupported event rather than silently pretending success.

Examples of unsafe actions:

- deleting files;
- overwriting original evidence;
- running arbitrary shell commands;
- writing exports into the evidence folder;
- treating a synthetic fixture as real validation.

## Acceptance

The boundary is acceptable only when:

- the public tool list remains fixed unless a decision is recorded;
- source code contains no generic shell execution surface;
- case workspace path validation is enforced;
- tests prove path traversal and missing-tool failures are blocked;
- docs preserve the synthetic-vs-real validation distinction;
- `py scripts\audit_release_controls.py --json --strict` passes.
