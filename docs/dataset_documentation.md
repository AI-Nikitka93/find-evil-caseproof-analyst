# Dataset Documentation

Project: Evidence-Locked Self-Correcting Disk Triage MCP  
Status: real bounded CASE-RD01 evidence pass completed; full incident analysis still open  
Last updated: 2026-05-07

## Real Dataset Used

| Field | Value |
|---|---|
| Contest source | FIND EVIL starter case data |
| Source folder | `HACKATHON-2026 / Compromised APT Attack Scenarios / SRL-2018-Compromised Enterprise Network` |
| Evidence filename | `base-rd-01-cdrive.E01` |
| Local path | `M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01` |
| Local file presence | Present as of 2026-05-06 |
| Size on disk | `17,820,145,297` bytes |
| EWF media size from `ewfinfo` | `33,833,353,216` bytes |
| File type | EWF/E01; first bytes show `EVF` signature |
| SHA256 | `12A622AA073DBBDA3A4983014328A6085C8247CE93FE47FD6BA7483ED9D19AAB` |
| EWF MD5 from `ewfinfo` | `391be74b6830344eace7272f697cf1ae` |
| EWF SHA1 from `ewfinfo` | `58dc1e291176dc8f370c936d3a2d6b79f6ecd791` |
| Acquisition date from `ewfinfo` | `Fri Sep 7 01:43:28 2018` |
| Local storage rule | Stored under ignored `evidence/` folder and marked read-only |

## Runtime Used

The 2026-05-07 real bounded pass used WSL Ubuntu with these forensic commands
available:

- `mmls`;
- `fls`;
- `icat`;
- `log2timeline.py`;
- `psort.py`;
- `regripper` as the local RegRipper executable used for the project-level
  `rip.pl` requirement.

The runtime is SIFT-compatible for the required tool families, but it is not the
official SANS SIFT OVA. The local Plaso install currently fails EVTX extraction
with a missing `MacOSLocalTime` artifact definition, so `extract_event_records`
falls back to the committed `python-evtx` dependency for bounded EVTX content
parsing. Public copy must keep that distinction visible.

## Run Scope

Run ID: `real-20260507T101441Z`

Completed scope:

- preflight of evidence path, workspace, local-only evidence rule, and tool
  availability;
- read-only evidence open with expected SHA256 comparison;
- partition/volume boundary detection;
- root filesystem inventory;
- recursive high-signal path inventory for registry hives, event logs, user
  hives, and McAfee agent event paths;
- `icat` extraction of `SOFTWARE` and `SYSTEM` hives from the `.E01` into the
  case workspace;
- bounded RegRipper parsing of SOFTWARE Run keys and SYSTEM services;
- `icat` extraction of `Security.evtx`, `System.evtx`, and `Application.evtx`
  followed by bounded `python-evtx` content parsing;
- root-inventory replay consistency check;
- final analyst report, evidence book, correction ledger, real-run accuracy
  report, execution log review, judge summary, and artifact index generation.

Not completed in this bounded run:

- full Plaso timeline;
- registry parsing beyond SOFTWARE Run keys and SYSTEM services;
- event parsing beyond the first bounded 120 records;
- content-level persistence finding;
- content-level compromise finding;
- official ground-truth scoring.

## Generated Local Artifacts

All generated artifacts are under `cases/CASE-RD01/`, which is intentionally
ignored from public repository packaging.

| Artifact | Path |
|---|---|
| Final analyst report | `cases/CASE-RD01/reports/final_analyst_report.md` |
| Evidence book | `cases/CASE-RD01/reports/evidence_book.md` |
| Correction ledger | `cases/CASE-RD01/reports/correction_ledger.md` |
| Real-run accuracy report | `cases/CASE-RD01/reports/real_run_accuracy_report.md` |
| Replay proof | `cases/CASE-RD01/reports/replay_consistency.md` |
| Real-run summary | `cases/CASE-RD01/reports/real_run_summary.json` |
| Execution log | `cases/CASE-RD01/logs/agent_execution.jsonl` |
| Root inventory export | `cases/CASE-RD01/exports/root_inventory.json` |
| High-signal inventory export | `cases/CASE-RD01/exports/high_signal_inventory.json` |
| Registry content summary | `cases/CASE-RD01/exports/registry_content_summary.json` |
| Event content summary | `cases/CASE-RD01/exports/event_content_summary.json` |
| Preflight export | `cases/CASE-RD01/exports/preflight_report.json` |

## Observed Artifact Counts

From `cases/CASE-RD01/reports/real_run_summary.json`:

| Artifact group | Count |
|---|---:|
| Root inventory records | 33 |
| High-signal inventory records | 617 |
| Registry hive/path records | 201 |
| Event log records located by path | 3 |
| User hive records | 54 |
| McAfee event-path records | 3 |
| SOFTWARE Run key records parsed | 5 |
| SYSTEM service records parsed | 80 |
| EVTX content records parsed | 120 |

## Confirmed Real Findings

The bounded pass confirmed evidence-integrity, artifact-availability, and
bounded registry/event-content facts:

- `F001`: RD01 EWF evidence opened read-only and matched expected SHA256.
- `F002`: RD01 is analyzable as an NTFS volume image at sector `0`.
- `F003`: High-signal Windows artifact families are present for follow-on
  triage.
- `F004`: SOFTWARE Run keys and SYSTEM service entries were extracted from the
  real image and parsed into bounded registry content records.
- `F005`: Security/System/Application EVTX files were extracted from the real
  image and parsed into 120 bounded event records.

No malicious finding is confirmed by this run.

## Synthetic Fixture Status

The older synthetic fixture remains in the repository for regression checks:

- generator: `tests/mock_eval_fixture.py`;
- generated log: `agent_execution_log.jsonl`;
- fixture path reference: `fixtures/mock_sift/rd01-cdrive.E01`.

It must not be described as real CASE-RD01 accuracy.

## Known Limitations

- The real documented CASE-RD01 accuracy pass used a deterministic MCP backend
  path.
- OpenRouter is now implemented and smoke-tested as the current free/low-cost
  autonomous runtime path, but the short smoke run is not a full incident
  reconstruction.
- The WSL toolchain is not the official SANS SIFT OVA.
- No official answer key is available in local project materials.
- Full timeline, registry analysis beyond Run keys/services, and deeper
  registry/event/timeline correlation remain unparsed in this bounded pass.

## Next Dataset Work

- Run a longer OpenRouter/Groq/Anthropic autonomous loop when provider limits
  allow it.
- Expand registry parsing beyond Run keys/services and correlate parsed event
  content into evidence-backed findings.
- Run or bound full timeline generation.
- Update the reviewer-derived manifest from content-level evidence.
- Prepare public-safe excerpts or summaries for submission without publishing
  private evidence or local case workspaces.
