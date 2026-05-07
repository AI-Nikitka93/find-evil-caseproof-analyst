# FIND EVIL Judging 17/17 Readiness Map

Date: 2026-05-07

Purpose: map the project to the strongest judge-facing proof for each FIND
EVIL criterion without overstating completion. This is a submission prep
artifact, not a claim that judges must award a perfect score.

## Rule Snapshot Used

Live rules checked on 2026-05-07:

- Devpost rules: `https://findevil.devpost.com/rules`
- SIFT Workstation overview: `https://www.sans.org/tools/sift-workstation/`
- Project public repository:
  `https://github.com/AI-Nikitka93/find-evil-caseproof-analyst`

## Maximum-Score Narrative

CaseProof Analyst should be presented as a narrow but strong Custom MCP Server
submission:

- evidence safety is architectural, not prompt-only;
- original evidence is input-only;
- the model cannot call arbitrary shell commands through the MCP server;
- every confirmed bounded finding links to evidence references;
- unsupported compromise claims are visibly rejected;
- the public trace shows real evidence opening, artifact extraction, bounded
  registry/event correlation, and final claim verification.

## Criterion Map

| Criterion | 17/17 proof to show | Current evidence | Residual risk |
|---|---|---|---|
| Autonomous Execution Quality | Bounded agent loop, hard budgets, real tool calls, visible correction. | `src/agent.py`, `src/prompts.py`, `docs/autonomous_smoke_hardening_2026-05-07.md`, `docs/public_real_traceability_packet.md` | Full long-run autonomous incident reconstruction is not claimed. |
| IR Accuracy | No confirmed finding without evidence; unsupported compromise claim dropped; no clean/no-evil overclaim. | `cases/CASE-RD01/reports/final_analyst_report.md`, `cases/CASE-RD01/reports/real_run_accuracy_report.md`, `src/real_validation.py` | No official answer key is available locally. |
| Breadth And Depth | One deep Windows disk lane with filesystem, registry, event, bounded correlation, and replay proof. | `cases/CASE-RD01/exports/registry_content_summary.json`, `cases/CASE-RD01/exports/event_content_summary.json`, `cases/CASE-RD01/exports/correlation_summary.json` | Full Plaso timeline and deeper process/account corroboration remain future work. |
| Constraint Implementation | Eight fixed MCP tools, no generic shell, read-only evidence boundary, workspace-only outputs. | `src/server.py`, `docs/architecture.md`, `docs/mcp_architecture.md`, `docs/trust_boundary_contract.md` | Public demo must explain this in plain language. |
| Audit Trail Quality | Judge can trace finding -> evidence book -> execution log -> public trace. | `docs/public_real_execution_log_sample.jsonl`, `docs/public_real_traceability_packet.md`, `docs/reviewer_traceability_walkthrough.md` | Raw local case workspace is intentionally not published. |
| Usability And Documentation | README, judge runbook, preflight, final gate, troubleshooting. | `README.md`, `docs/judge_try_it_out.md`, `scripts/check_env.py`, `scripts/final_submission_audit.py` | Clean external judge-machine verification remains outside this local run. |

## Demo Must Show

1. Run `py scripts\demo_rehearsal.py --strict`.
2. Show real evidence path and read-only/open/hash proof.
3. Show `registry_content_summary.json`, `event_content_summary.json`, and
   `correlation_summary.json`.
4. Open `correction_ledger.md` and show the unsupported compromise claim was
   dropped.
5. Open `docs/public_real_traceability_packet.md` and show the 10-step public
   trace.
6. Say clearly: no confirmed malicious finding is claimed because the bounded
   evidence does not prove compromise.

## Submission-Critical Boundary

Do not say:

- full incident reconstruction;
- full SIFT coverage;
- official ground-truth accuracy;
- clean machine or no evil found;
- demo video complete before the public URL exists.

Say instead:

- bounded real evidence validation;
- read-only Custom MCP boundary;
- evidence-linked first triage;
- visible self-correction;
- bounded registry/event correlation with compromise kept unconfirmed.
