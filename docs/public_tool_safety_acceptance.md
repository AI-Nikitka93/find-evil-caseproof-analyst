# Public Tool Safety Acceptance

Date: 2026-05-06

Purpose: define what each public MCP tool may read, may create, and must never change.

## Safety Table

| Tool | May read | May create | Must never change |
|---|---|---|---|
| `case_open_readonly` | Existing evidence file path and expected hash value. | Case workspace directories. | Original evidence file. |
| `list_partitions` | Registered evidence image. | In-memory partition evidence references. | Evidence image and files outside workspace. |
| `filesystem_inventory` | Registered evidence image through bounded filesystem listing. | In-memory filesystem evidence references. | Evidence image and arbitrary filesystem paths. |
| `build_timeline` | Registered evidence or case workspace artifacts. | Timeline storage/export files inside case workspace. | Original evidence and paths outside workspace. |
| `extract_registry_persistence` | Registry hive paths provided from evidence/workspace context. | Registry export files inside case workspace and evidence references. | Original hives/evidence and external paths. |
| `extract_event_records` | Event log paths provided from evidence/workspace context. | Event export files inside case workspace and event evidence references. | Original event logs/evidence and external paths. |
| `verify_claim` | In-memory evidence references and provided evidence refs. | Verification result object. | Evidence, workspace files, or claim history. |
| `write_execution_log` | Case registry and provided request fields. | Append-only execution log inside case workspace. | Existing log lines, evidence files, external paths. |

## Common Safety Rules

All tools must:

- reject path traversal;
- avoid generic shell access;
- return visible errors for expected forensic failures;
- preserve parser status;
- keep generated outputs inside the case workspace;
- distinguish confirmed, inferred, unsupported, and human-review outcomes where relevant.

## Acceptance Criteria

The current implementation is acceptable when:

- path traversal is tested;
- missing SIFT binary failure is surfaced as a tool-level error;
- append-only logging is tested;
- public tool names are stable;
- original evidence is never exposed as an output target;
- release-control audit passes.
