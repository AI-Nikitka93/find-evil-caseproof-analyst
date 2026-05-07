# Final Quality Gate Matrix

Date: 2026-05-07  
Project: CaseProof Analyst / Evidence-Locked Self-Correcting Disk Triage MCP

## Gate Summary

| Gate | Status | Evidence | Remaining risk |
|---|---:|---|---|
| Autonomous execution quality | PARTIAL | `src/agent.py`, OpenRouter smoke runs, bounded loop constants, execution logs | Full long-run autonomous investigation is not complete. |
| IR accuracy | PARTIAL | `docs/accuracy_report.md`, `cases/CASE-RD01/reports/real_run_accuracy_report.md`, `cases/CASE-RD01/exports/registry_content_summary.json` | SOFTWARE Run keys and SYSTEM services are parsed; event-log content, full timeline, and deeper registry correlation remain open. |
| Breadth and depth | PARTIAL | Real bounded RD01 pass, high-signal inventory, reviewer-derived manifest | Depth is honest but intentionally narrow. |
| Constraint implementation | STRONG | Eight fixed MCP tools, no generic shell, read-only evidence boundary | Final public docs must not imply broad SIFT coverage. |
| Audit trail quality | STRONG | `cases/CASE-RD01/logs/agent_execution.jsonl`, `docs/public_real_execution_log_sample.jsonl`, evidence book, correction ledger | Public excerpt is sanitized; raw local case outputs are ignored from public repo by policy. |
| Usability and documentation | READY FOR PUBLIC PACKAGE | README, `docs/judge_try_it_out.md`, troubleshooting, recovery instructions | Clean external judge machine run and public GitHub URL still need final verification. |
| Submission media | NOT COMPLETE | `docs/demo_video_script.md` | Actual video recording and public upload remain external actions. |
| Public release hygiene | READY LOCALLY | release-control audit, ignored-file policy, secret scans | Current folder is not a git repository, so GitHub publication cannot be verified locally. |

## Judging Criteria Mapping

### Autonomous Execution Quality

Evidence:

- `src.agent` keeps `MAX_ITERATIONS`, global timeout, tool-call budget, token
  budget, and provider selection.
- OpenRouter is the current working free/low-cost implemented runtime path.
- Groq returned HTTP 403 in live testing and must not be presented as working
  for the final demo unless re-tested successfully.
- Deterministic MCP backend run exists for the real RD01 evidence package.

Final wording:

- say "bounded autonomous agent and deterministic backend validation";
- do not say "full autonomous incident reconstruction".

### IR Accuracy

Evidence:

- confirmed real findings include evidence integrity, filesystem/artifact availability, and bounded SOFTWARE Run-key/SYSTEM service registry content;
- no compromise finding is claimed;
- unsupported compromise/persistence claim is dropped;
- unknowns are preserved.

Final wording:

- say "partial real validation passed";
- say "event-log content, full timeline, and deeper registry correlation remain future work";
- do not say "APT activity found" unless content-level evidence is added later.

### Breadth And Depth

Evidence:

- one Windows disk-image lane;
- read-only evidence open;
- filesystem boundary and high-signal artifact discovery;
- bounded registry content parsing for Run keys and services;
- replay consistency.

Final wording:

- position the project as a defensible first triage slice;
- do not claim memory, pcap, SIEM, endpoint, or full 200-tool SIFT wrapping.

### Constraint Implementation

Evidence:

- no generic shell MCP tool;
- fixed Pydantic schemas;
- output workspace containment;
- original evidence read-only;
- unsafe/destructive actions are not routable.

Final wording:

- emphasize architectural guardrails;
- distinguish them from prompt-only behavior.

### Audit Trail Quality

Evidence:

- execution logs include timestamps, tool names, parser statuses, token usage
  where available, and correction reasons;
- evidence book links findings to evidence refs;
- correction ledger records rejected unsupported claim.
- public trace now includes `extract_registry_persistence` before final claim verification.
- public-safe real execution excerpt is available at
  `docs/public_real_execution_log_sample.jsonl`, with the walkthrough in
  `docs/public_real_traceability_packet.md`.

Final wording:

- show one trace chain in the demo;
- point judges to `docs/reviewer_traceability_walkthrough.md`.

### Usability And Documentation

Evidence:

- setup commands in README;
- readiness checks;
- judge try-it-out instructions;
- troubleshooting and recovery path;
- release checklist.

Final wording:

- "local SIFT-compatible run path is documented";
- "official SANS SIFT OVA still requires final clean-machine verification".

## Final Gate Decision

The project is locally package-ready after verification passes, but the final
submission remains blocked until:

1. a public GitHub repository URL exists and is verified;
2. the demo video is recorded, uploaded, and publicly visible;
3. the Devpost submission is filled using the prepared English text;
4. final links are checked from a non-private browser session.
