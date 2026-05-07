# Expected Artifact Families

Date: 2026-05-06

Purpose: define what the selected Windows disk-triage case is expected to cover before the real evidence run starts.

## Scope

Selected case lane:

```text
SRL-2018-Compromised Enterprise Network / base-rd-01-cdrive.E01
```

This document defines expected artifact families, not confirmed findings. Nothing here is a claim about the actual evidence until the real run links it to tool output.

## Artifact Families

| Family | Why it matters | Expected result type | Confirmation rule |
|---|---|---|---|
| Partition layout | Establishes readable disk structure before deeper triage. | Partition records, offsets, sizes, filesystem hints. | Confirm only from partition inspection output. |
| Filesystem inventory | Shows high-value files, paths, deleted entries, user areas, and system locations. | Path records with metadata and source references. | Confirm only from filesystem listing or extracted metadata. |
| Timeline | Places activity in order and supports the visible self-correction story. | Normalized events from filesystem and parsed artifacts. | Confirm only when timestamp, source, and parser origin are present. |
| Registry persistence | Supports Windows persistence and execution-trace analysis. | Registry-derived records or conservative evidence blocks. | Confirm only when hive/source path and plugin/parser output are linked. |
| Event records | Provides operational context for logon, service, execution, and system activity where available. | Event records with provider, record ID, timestamp, and rendered fields. | Confirm only when event source and record data are present. |
| Negative controls | Prevents overclaiming when expected artifacts are absent or parser output is empty. | Explicit absence, parser miss, unsupported claim, or human-review note. | Confirm absence only after the relevant tool path ran successfully. |
| Claim verification | Separates confirmed facts from inferences and unsupported findings. | Confirmed, inferred, unsupported, or needs-human-review labels. | Confirm only through `verify_claim` output or equivalent linked evidence review. |
| Execution trail | Gives judges a trace from final finding back to tool execution. | Append-only run records with case, tool, arguments, output reference, and result status. | Confirm only from the real case workspace execution log. |

## Expected High-Value Questions

The real case run should be able to answer or explicitly mark unknown:

- What disk image was analyzed?
- Which partition or filesystem was selected for triage?
- Which files, directories, or artifact locations were high-signal?
- Which events or timestamps support the attack story?
- Which persistence or execution artifacts were confirmed?
- Which initial claims were rejected or corrected?
- Which artifact families were unavailable, empty, or inconclusive?
- Which final findings are supported by specific evidence records?

## Negative Control Requirements

The final report must not hide negative controls. It must show:

- artifact family attempted but no records found;
- parser failed or produced unreadable output;
- evidence unavailable in the selected image;
- claim proposed but unsupported;
- inference kept only as inference, not confirmed fact.

## Completion Standard

This artifact-family set is complete when:

- each family maps to a public MCP tool or documented evidence review path;
- each family has a confirmation rule;
- absence and uncertainty are treated as valid outcomes;
- no expected family is described as already found before the real evidence run.
