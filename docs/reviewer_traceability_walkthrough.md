# Reviewer Traceability Walkthrough

Date: 2026-05-07  
Case: `CASE-RD01`  
Purpose: give a judge a no-private-help path from a final finding to the tool
execution that produced the supporting evidence.

## Quick Path

Start with the public docs:

1. `README.md` for the project promise, current validation status, and run
   commands.
2. `docs/dataset_documentation.md` for the tested evidence and run scope.
3. `docs/accuracy_report.md` for what the real bounded run proves and does not
   prove.
4. `docs/architecture.md` for the trust boundary and correction-loop diagrams.

Then inspect the local real-run package if available:

1. `cases/CASE-RD01/reports/final_analyst_report.md`
2. `cases/CASE-RD01/reports/evidence_book.md`
3. `cases/CASE-RD01/reports/correction_ledger.md`
4. `cases/CASE-RD01/reports/real_run_accuracy_report.md`
5. `cases/CASE-RD01/logs/agent_execution.jsonl`

`cases/` is intentionally ignored from the public repository because it can
contain local evidence-derived outputs. The public repo should include the
summary docs above and should not publish the raw local case workspace unless a
separate public-safe review approves it.

Public-safe real execution excerpt:

1. `docs/public_real_execution_log_sample.jsonl`
2. `docs/public_real_traceability_packet.md`

These public files preserve the real step sequence, parser statuses, output
references, and self-correction reason without publishing raw `cases/` outputs
or local absolute paths.

## Finding F001 Chain

Final finding:

- `F001`: RD01 EWF evidence opened read-only and matched the expected SHA256.

Trace chain:

| Layer | What to inspect |
|---|---|
| Final report | `cases/CASE-RD01/reports/final_analyst_report.md`, finding `F001` |
| Evidence book | `cases/CASE-RD01/reports/evidence_book.md`, `F001` entry |
| Source action | `case_open_readonly` |
| Evidence reference | `case_open_readonly:sha256` reference in the evidence book |
| Execution log | `cases/CASE-RD01/logs/agent_execution.jsonl`, `tool_name=case_open_readonly` |
| Public excerpt | `docs/public_real_execution_log_sample.jsonl`, `tool_name=case_open_readonly` |
| Integrity check | `docs/dataset_documentation.md` SHA256 and read-only storage rule |

Expected result:

- the evidence hash is recorded;
- the run does not write to `evidence/base-rd-01-cdrive.E01`;
- generated outputs stay under the case workspace;
- this finding is safe to present as confirmed because it is an integrity fact,
  not a compromise claim.

## Finding F002 Chain

Final finding:

- `F002`: RD01 is analyzable as an NTFS volume image at sector `0`.

Trace chain:

| Layer | What to inspect |
|---|---|
| Final report | `cases/CASE-RD01/reports/final_analyst_report.md`, finding `F002` |
| Evidence book | `cases/CASE-RD01/reports/evidence_book.md`, `F002` entry |
| Source action | `list_partitions` with `fsstat` fallback |
| Accuracy note | `docs/accuracy_report.md`, reviewer-derived manifest comparison |
| Execution log | `cases/CASE-RD01/logs/agent_execution.jsonl`, `tool_name=list_partitions` |
| Public excerpt | `docs/public_real_execution_log_sample.jsonl`, `tool_name=list_partitions` |

Expected result:

- the project does not fake a partition table when `mmls` is not useful;
- the fallback is documented as a volume-image boundary result;
- the limitation remains visible in the accuracy report.

## Finding F003 Chain

Final finding:

- `F003`: high-signal Windows artifact families are present for follow-on
  triage: registry hives, event logs, user hives, and McAfee agent event paths.

Trace chain:

| Layer | What to inspect |
|---|---|
| Final report | `cases/CASE-RD01/reports/final_analyst_report.md`, finding `F003` |
| Evidence book | `cases/CASE-RD01/reports/evidence_book.md`, `F003` entry |
| Source action | `filesystem_inventory` |
| Export | `cases/CASE-RD01/exports/high_signal_inventory.json` |
| Dataset summary | `docs/dataset_documentation.md`, observed artifact counts |
| Execution log | `cases/CASE-RD01/logs/agent_execution.jsonl`, `tool_name=filesystem_inventory` |
| Public excerpt | `docs/public_real_execution_log_sample.jsonl`, `tool_name=filesystem_inventory` |

Expected result:

- artifact families are confirmed as present;
- no malicious finding is inferred from presence alone;
- bounded registry Run-key/service content, bounded EVTX event content, and
  bounded registry/event correlation are parsed, but full Plaso timeline and
  deeper process/account corroboration remain open until parsed into
  content-level evidence.

## Finding F005 Chain

Final finding:

- `F005`: Windows EVTX records were extracted from the real image and parsed
  into bounded event content records.

Trace chain:

| Layer | What to inspect |
|---|---|
| Final report | `cases/CASE-RD01/reports/final_analyst_report.md`, finding `F005` |
| Evidence book | `cases/CASE-RD01/reports/evidence_book.md`, `F005` entry |
| Source action | `extract_event_records` after `icat` extraction of EVTX files |
| Export | `cases/CASE-RD01/exports/event_content_summary.json` |
| Accuracy note | `docs/accuracy_report.md`, `RD01-EVT-001` row |
| Execution log | `cases/CASE-RD01/logs/agent_execution.jsonl`, `tool_name=extract_event_records` |
| Public excerpt | `docs/public_real_execution_log_sample.jsonl`, `tool_name=extract_event_records` |

Expected result:

- event records are confirmed as parsed content, not only as paths;
- the local Plaso dependency issue is made survivable by the `python-evtx`
  fallback;
- no compromise finding is inferred from event presence alone.

## Finding F006 Chain

Final finding:

- `F006`: bounded registry/event correlation was performed and kept compromise
  status unconfirmed pending deeper timeline and process/account corroboration.

Trace chain:

| Layer | What to inspect |
|---|---|
| Final report | `cases/CASE-RD01/reports/final_analyst_report.md`, finding `F006` |
| Evidence book | `cases/CASE-RD01/reports/evidence_book.md`, `F006` entry |
| Source action | bounded correlation over registry and event summaries |
| Export | `cases/CASE-RD01/exports/correlation_summary.json` |
| Accuracy note | `docs/accuracy_report.md`, `RD01-CORR-002` row |
| Execution log | `cases/CASE-RD01/logs/agent_execution.jsonl`, `output_reference=exports/correlation_summary.json` |
| Public excerpt | `docs/public_real_execution_log_sample.jsonl`, step `9` |

Expected result:

- Event ID 1102 remains visible as a high-signal review item;
- registry persistence surfaces remain visible for reviewer correlation;
- `confirmed_compromise` stays `false` because the bounded evidence does not
  yet establish malicious intent or full attack reconstruction.

## Self-Correction Chain

Rejected candidate claim:

- `Confirmed compromise or persistence on RD01`.

Trace chain:

| Layer | What to inspect |
|---|---|
| Correction ledger | `cases/CASE-RD01/reports/correction_ledger.md` |
| Accuracy report | `docs/accuracy_report.md`, rejected unsupported claim |
| Execution log | `cases/CASE-RD01/logs/agent_execution.jsonl`, `tool_name=verify_claim` |
| Public excerpt | `docs/public_real_execution_log_sample.jsonl`, `tool_name=verify_claim`, `correction_reason=Unsupported compromise claim dropped from confirmed findings.` |
| Public explanation | `docs/demo_video_script.md`, self-correction moment |

Expected result:

- the tempting compromise claim is challenged;
- the claim is dropped from confirmed findings;
- the final report keeps compromise status unknown rather than overstating.

## Reviewer Verdict

A reviewer can trace the bounded real run from final report to evidence and
tool execution. The local case package contains the full generated outputs; the
public repository now also contains a sanitized real execution-log excerpt for
judges who cannot inspect `cases/` directly.
