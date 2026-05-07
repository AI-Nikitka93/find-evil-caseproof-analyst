# Output Size Discipline

Date: 2026-05-06

Purpose: keep analyst-facing output bounded and explainable while preserving raw/noisy data in the case workspace.

## Product Rule

Large raw forensic output should not be pushed directly into the analyst narrative or model context.

The product must separate:

- raw or noisy tool output;
- normalized evidence records;
- bounded analyst-facing summaries;
- final verified findings.

## Output Surfaces

| Surface | Intended content | Size behavior |
|---|---|---|
| Raw exports | Full parser/tool output where needed. | Stored under case workspace, not pasted into final report. |
| Normalized records | Parsed partition, filesystem, timeline, registry, event, and evidence references. | Bounded by tool-specific max record limits. |
| Execution log | Tool actions, parser status, output references, corrections. | Append-only and structured. |
| Final report | Confirmed/inferred/unsupported/human-review summary. | Analyst-readable and evidence-linked. |
| Accuracy report | Evaluation counts and limitations. | Summarized, with links to evidence/log artifacts. |

## Current Bounded Controls

Current implementation exposes max limits in tool contracts:

- filesystem inventory record cap;
- timeline record cap;
- registry persistence record cap;
- event record cap;
- bounded stderr detail for failed tool calls;
- append-only log records instead of unbounded transcript dumps.

## UX Rule

Analyst-facing output should answer:

- what was checked;
- what was found;
- what was unsupported;
- what failed or stayed unknown;
- where the evidence can be traced.

It should not force the reader to inspect huge raw outputs to understand the result.

## Acceptance

This discipline is complete when:

- raw output is stored separately;
- analyst-facing output is bounded;
- truncation or partial status remains visible;
- final findings link back to evidence/log references;
- no broad raw dump is treated as a finished report.
