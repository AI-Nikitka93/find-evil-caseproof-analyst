# Public Real Traceability Packet

Date: 2026-05-07
Case: `CASE-RD01`
Source: redacted excerpt generated from the local real-run execution log.

## Purpose

This packet gives judges a public-safe view of the real CASE-RD01 tool
sequence without publishing the ignored local `cases/` workspace or the
private `evidence/` directory.

It preserves the information needed for the FIND EVIL audit-trail
requirement: step order, timestamp, tool name, parser status, output
reference, token-usage field, and the visible self-correction reason.

## Public Files

- `docs/public_real_execution_log_sample.jsonl`: sanitized JSONL trace.
- `docs/public_real_traceability_packet.md`: this reviewer walkthrough.

## Sanitization

- Local absolute paths are replaced with repository-relative public labels.
- Original evidence bytes and raw case exports are not included.
- API keys, bearer tokens, and local user or machine identifiers are blocked.
- The per-run internal evidence identifier is replaced with `[RUN_EVIDENCE_ID]`.

## Source Log

- Local source path: `cases/CASE-RD01/logs/agent_execution.jsonl`
- Public replacement path: `docs/public_real_execution_log_sample.jsonl`

## Step Trace

| Step | Tool | Parser | Output | Correction | Intent |
|---:|---|---|---|---|---|
| 1 | `case_open_readonly` | `ok` | `reports/artifact_index.json` | None | Open evidence read-only and verify hash before analysis. |
| 2 | `list_partitions` | `ok` | `reports/evidence_book.md` | None | Identify the analyzable Windows filesystem or volume image boundary. |
| 3 | `filesystem_inventory` | `ok` | `exports/root_inventory.json` | None | Collect root filesystem inventory for case orientation. |
| 4 | `filesystem_inventory` | `ok` | `exports/high_signal_inventory.json` | None | Locate registry hives, event logs, user hives, and security product event artifacts without extracting private content. |
| 5 | `filesystem_inventory` | `ok` | `reports/replay_consistency.md` | None | Replay root inventory to prove the output is reproducible rather than a one-off artifact. |
| 6 | `extract_registry_persistence` | `ok` | `exports/registry_content_summary.json` | None | Extract SOFTWARE Run key content after copying the hive out of the evidence image with icat. |
| 7 | `extract_registry_persistence` | `ok` | `exports/registry_content_summary.json` | None | Extract SYSTEM service content to move beyond artifact presence into bounded registry analysis. |
| 8 | `verify_claim` | `ok` | `reports/correction_ledger.md` | Unsupported compromise claim dropped from confirmed findings. | Challenge an attractive but unsupported compromise claim before final reporting. |

## Self-Correction Signal

The final `verify_claim` step challenges the tempting claim
`Confirmed compromise or persistence on RD01` and records the correction
reason `Unsupported compromise claim dropped from confirmed findings.`
That is the public demo moment: the system refuses to upgrade artifact
presence into a confirmed malicious finding without content-level evidence.

## Limits

- This is a redacted execution-log excerpt, not the full local case workspace.
- Registry Run-key and service content is parsed in this bounded run; event-log,
  timeline, and deeper registry correlation remain future work.
- The public log proves traceability for the bounded real run, not full
  incident reconstruction.