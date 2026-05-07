# Accuracy Report

Project: Evidence-Locked Self-Correcting Disk Triage MCP  
Evaluation date: 2026-05-07  
Eval mode: real bounded CASE-RD01 evidence pass plus historical synthetic fixture  
Dataset: `base-rd-01-cdrive.E01`

## 1. Evaluation Scope

This report now separates two things:

- the real bounded evidence pass under `cases/CASE-RD01/`;
- the older synthetic fixture `agent_execution_log.jsonl`, which remains useful
  only for regression testing trajectory and safety behavior.

The real pass used the selected FIND EVIL starter evidence file:

- filename: `base-rd-01-cdrive.E01`;
- SHA256: `12A622AA073DBBDA3A4983014328A6085C8247CE93FE47FD6BA7483ED9D19AAB`;
- runtime: WSL Ubuntu forensic toolchain with `mmls`, `fls`, `icat`,
  `log2timeline.py`, `psort.py`, and `regripper` as the local RegRipper
  executable;
- output workspace: `cases/CASE-RD01/`.

The real pass used the MCP backend deterministically. After that pass,
OpenRouter was implemented and smoke-tested as the current free/low-cost
autonomous runtime path; the smoke run is not counted here as full incident
accuracy because it used a short iteration limit.

## 2. Real Run Outputs

The real run produced these local artifacts:

- `cases/CASE-RD01/reports/final_analyst_report.md`;
- `cases/CASE-RD01/reports/evidence_book.md`;
- `cases/CASE-RD01/reports/correction_ledger.md`;
- `cases/CASE-RD01/reports/real_run_accuracy_report.md`;
- `cases/CASE-RD01/reports/replay_consistency.md`;
- `cases/CASE-RD01/reports/real_run_summary.json`;
- `cases/CASE-RD01/logs/agent_execution.jsonl`;
- `cases/CASE-RD01/exports/root_inventory.json`;
- `cases/CASE-RD01/exports/high_signal_inventory.json`;
- `cases/CASE-RD01/exports/registry_content_summary.json`;
- `cases/CASE-RD01/exports/preflight_report.json`.

`py scripts\audit_real_validation.py --case-workspace "M:\Projects\Konkurs\Find Evil!\cases\CASE-RD01" --json --strict`
passes against these artifacts.

## 3. Real Findings Accuracy

Confirmed evidence-backed findings from the real run:

| Finding | Status | Evidence |
|---|---|---|
| `F001` | confirmed | EWF evidence opened read-only and matched expected SHA256. |
| `F002` | confirmed | Evidence is analyzable as an NTFS volume image at sector `0`; `mmls` had no useful partition table and `fsstat` provided the volume fallback. |
| `F003` | confirmed | High-signal Windows artifact families are present: registry hives, event logs, user hives, and McAfee agent event paths. |
| `F004` | confirmed | `SOFTWARE` Run keys and `SYSTEM` service entries were extracted from the real image with `icat` and parsed through RegRipper into bounded registry content records. No malicious classification is asserted from this alone. |

Confirmed compromise findings:

- None.

Unsupported claims promoted to confirmed output:

- None.

Rejected unsupported claim:

- `Confirmed compromise or persistence on RD01` was challenged and dropped
  because the bounded registry content did not establish compromise and the run
  did not parse event or timeline content into compromise-level evidence.

## 4. Reviewer-Derived Manifest Comparison

Official ground truth is not available in the local project materials. The
comparison below is against the reviewer-derived manifest, not an official
answer key.

| Manifest item | Real outcome | Result |
|---|---|---|
| `RD01-PARTITION-001` | The image behaves as a mounted/analyzable NTFS volume image at sector `0`; `mmls` is not the right source for a partition table here. | matched with limitation |
| `RD01-FS-001` | Root inventory and high-signal path inventory produced records from the real `.E01`. | matched |
| `RD01-TIME-001` | Full timeline content was not parsed in this bounded run. | unknown |
| `RD01-REG-001` | SOFTWARE Run keys and SYSTEM services were extracted and parsed into bounded registry content records; deeper registry correlation remains open. | matched with limitation |
| `RD01-EVT-001` | Event log paths were located, but event content was not parsed into findings. | unknown |
| `RD01-CORR-001` | One unsupported compromise/persistence claim was visibly challenged and dropped. | matched |
| `RD01-NEG-001` | Unknowns were preserved instead of upgraded into compromise claims. | matched |

## 5. False Positives And Hallucination Controls

Real bounded run:

- unsupported compromise claims tested: 1;
- unsupported compromise claims promoted to confirmed findings: 0;
- confirmed findings without evidence references: 0;
- parser/runtime limitations hidden from the report: 0.

The synthetic fixture still contains three historical unsupported-claim checks,
but those are no longer presented as real CASE-RD01 accuracy.

## 6. Missed Artifacts And Unknowns

Known unresolved real artifact families:

- full Plaso timeline;
- registry parsing beyond SOFTWARE Run keys and SYSTEM services;
- event log content parsing;
- content-level event, timeline, persistence-correlation, and execution findings;
- official ground-truth comparison.

These are not counted as confirmed negatives. They remain unknowns or next
analysis actions.

## 7. Replay And Evidence Integrity

Replay consistency:

- root filesystem inventory sample replayed successfully;
- first sample size: 25;
- replay sample size: 25;
- result recorded in `cases/CASE-RD01/reports/replay_consistency.md`.

Evidence integrity:

- original evidence was opened as input-only;
- output files were written under `cases/CASE-RD01/`;
- post-run evidence snapshot did not detect size, modified-time, or SHA256
  change.

## 8. Verdict

Verdict: **PARTIAL REAL VALIDATION PASSED**.

This is now a real evidence pass, not only a synthetic fixture. It proves
read-only evidence access, SIFT-compatible tool availability, bounded
filesystem triage, bounded registry Run-key/service parsing, evidence-backed
reporting, correction-ledger behavior, and replay consistency.

It does **not** prove full incident reconstruction or final contest readiness.
The next hard blockers are:

- longer autonomous AI run with provider limits accounted for;
- event-log content, full timeline, and deeper registry correlation;
- demo video;
- Devpost description;
- public repository publication and link verification.
