# Evidence-Locked Disk Triage MCP Architecture

Verification date: 2026-05-04
Status: contract bootstrap for P-BACKEND handoff

## 1. Scope

This document defines the Custom MCP Server contract for the FIND EVIL! project.
It is intentionally limited to interface design, typed schemas, error policy,
Claude Code / Protocol SIFT integration, and read-only safety boundaries.

The implementation of CLI execution, parsing, artifact storage, and parser
confidence scoring belongs to P-BACKEND.

## 2. Source Basis

Confirmed from project artifacts:

- `docs/hackathon_strategy.md`: the server exposes eight focused SIFT wrapper
  families for a narrow Windows disk triage use case.
- `docs/research_sift_mcp.md`: use the official `mcp` Python package, FastMCP
  v1.x style, typed input and output models, `ToolError` for expected tool
  failures, and stdio-safe logging discipline.

Working hypothesis:

- Protocol SIFT is treated as a Claude Code configuration and skill baseline,
  not as a separate MCP framework. The Custom MCP Server should therefore be
  launched as a local MCP server from Claude Code.

## 3. Integration Model

Target runtime:

- Host: SANS SIFT Workstation or a compatible local analysis environment.
- MCP transport: `stdio`.
- Client: Claude Code configured with Protocol SIFT guidance and this custom
  server.
- Server entrypoint: `python -m src.server`.

Expected Claude Code registration pattern:

```bash
claude mcp add find-evil-disk-triage --transport stdio -- python -m src.server
```

The exact command should be smoke-tested in the final SIFT workstation image,
but the architectural assumption is a local process-spawned server that speaks
MCP over stdio.

Stdio discipline:

- MCP protocol messages use stdout.
- Operational logs must go to files or stderr, never plain stdout.
- Tool output should return structured content through typed models, not loose
  terminal transcript text.

## 4. Read-Only Boundary

The server enforces evidence safety by architecture, not by prompt adherence.

Boundary rules:

- No generic shell execution tool is exposed.
- Only the eight fixed forensic tools are available.
- The original evidence path is an input source, never an output target.
- Case work products are written only under the configured case workspace.
- Backend command builders must use allowlisted SIFT commands for each tool.
- Backend path validation must reject writes outside the case workspace.
- Backend command builders must reject destructive flags and mutating workflows.
- Every tool returns parser status and must preserve enough source reference to
  support later claim verification.
- `write_execution_log` is append-only and records tool calls, arguments,
  parser failures, output references, and self-correction reasons.

The design is intentionally hostile to spoliation risk: the agent can ask for
forensic facts through constrained tools, but cannot freely run system commands.

## 5. Tool Contract Summary

| Tool | Purpose | Primary backend family | Input model | Output model |
|---|---|---|---|---|
| `case_open_readonly` | Register an evidence image and create analysis workspace binding. | image metadata, hash check, read-only mount plan | `CaseOpenReadonlyInput` | `CaseOpenReadonlyOutput` |
| `list_partitions` | Identify partitions, filesystem hints, offsets, and parser status. | Sleuth Kit `mmls`, `fsstat` | `ListPartitionsInput` | `ListPartitionsOutput` |
| `filesystem_inventory` | Enumerate bounded file metadata and high-value paths. | Sleuth Kit `fls`, `istat`, `icat` | `FilesystemInventoryInput` | `FilesystemInventoryOutput` |
| `build_timeline` | Produce normalized timeline records. | Plaso/log2timeline, psort, bodyfile fallback | `BuildTimelineInput` | `BuildTimelineOutput` |
| `extract_registry_persistence` | Extract autorun and persistence evidence from hives. | RegRipper, Plaso where useful | `ExtractRegistryPersistenceInput` | `ExtractRegistryPersistenceOutput` |
| `extract_event_records` | Extract selected Windows event records. | SIFT EVTX parsing surface | `ExtractEventRecordsInput` | `ExtractEventRecordsOutput` |
| `verify_claim` | Verify findings against normalized evidence. | internal evidence index | `VerifyClaimInput` | `VerifyClaimOutput` |
| `write_execution_log` | Persist audit trail for agent actions. | append-only local log writer | `WriteExecutionLogInput` | `WriteExecutionLogOutput` |

## 6. Shared Schema Concepts

`CommandPlan` records the intended backend command family, arguments, parser,
and expected output format. It is not a license for the model to execute shell
commands.

`EvidenceReference` links claims and extracted records back to source paths,
offsets, timestamps, record IDs, and evidence IDs.

`ParserStatus` is one of:

- `not_started`
- `ok`
- `partial`
- `failed`

Claim verification status is one of:

- `confirmed`
- `inferred`
- `unsupported`
- `needs_human_review`

## 7. Error Handling

Expected forensic failures should be returned as MCP tool errors, not as
fabricated successful results. The bootstrap uses `ToolError` around contract
stubs so the failure path is explicit.

Backend examples of expected failures:

- unsupported image format;
- missing partition offset;
- parser produced partial output;
- output cap reached;
- evidence hash mismatch;
- event log or hive cannot be parsed.

The agent should self-correct by narrowing scope, selecting another partition,
requesting a different parser mode, or marking a claim as unsupported.

## 8. Backend Handoff

P-BACKEND should implement the function bodies without changing public tool
names or schema field meanings unless a contract change is recorded in
`docs/DECISIONS.md`.

Required backend work:

- command allowlists for `mmls`, `fsstat`, `fls`, `istat`, `icat`,
  `log2timeline.py`, `psort.py`, and `rip.pl`;
- path validation for evidence inputs and workspace outputs;
- bounded parsing and truncation reporting;
- structured parser confidence for timeline, registry, and event records;
- append-only execution log writer;
- claim verifier over normalized evidence references;
- smoke tests against sample or synthetic Windows disk triage artifacts.
