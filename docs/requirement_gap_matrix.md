# Requirement Gap Matrix

Updated: 2026-05-07  
Purpose: close TODO T005 by mapping contest requirements to current artifacts, gaps, and next concrete results without assigning roles.

| Contest requirement | Current project artifact | Current status | Gap | Next concrete result |
|---|---|---:|---|---|
| Public code repository with open-source license | `README.md`, `LICENSE`, `src/`, `tests/`, https://github.com/AI-Nikitka93/find-evil-caseproof-analyst | Ready | Public GitHub repository is verified with MIT license. | Keep repository unchanged except for final video/Devpost link updates. |
| Demo video | README placeholder | Missing | No live terminal screencast exists. | Public video shows real evidence run, audio narration, and visible self-correction. |
| Architecture diagram | `docs/architecture.md`, `docs/mcp_architecture.md` | Present with verification needed | Mermaid rendering and public trust-boundary readability need final public check. | Public architecture diagram renders correctly and clearly marks evidence boundary. |
| Written project description | `docs/final_submission_package.md` | Ready locally | Public Devpost form is not submitted. | Devpost story is pasted with final public GitHub/video URLs. |
| Dataset documentation | `docs/dataset_documentation.md`, `docs/research_sift_mcp.md` | Present with limits | Event/timeline content and deeper registry correlation remain open. | Dataset doc stays honest after public link audit. |
| Accuracy report | `docs/accuracy_report.md` | Present with limits | Full incident reconstruction and official answer-key comparison remain unavailable. | Real-run accuracy report remains separated from synthetic fixture material. |
| Try-it-out instructions | `README.md`, `docs/judge_try_it_out.md` | Present with limits | Clean external judge machine verification remains external. | Judge can follow instructions in a SIFT-compatible environment and produce expected outputs. |
| Agent execution logs | `cases/CASE-RD01/logs/agent_execution.jsonl`, `docs/public_real_execution_log_sample.jsonl` | Present | Raw `cases/` stays local-only, so public repo uses sanitized real excerpt. | Public excerpt traces final actions and self-correction without leaking local paths. |
| Self-correction | `verify_claim`, `correction_ledger.md`, `docs/public_real_execution_log_sample.jsonl` | Present for bounded run | Video still must show it clearly. | Uploaded demo shows the unsupported compromise claim being dropped. |
| Accuracy validation | `verify_claim` tool, `docs/accuracy_report.md` | Present with limits | Bounded registry content is validated; event/timeline and deeper registry findings are not validated. | Every confirmed bounded-run finding keeps evidence support and verifier status. |
| Analytical narrative | `cases/CASE-RD01/reports/final_analyst_report.md`, `docs/accuracy_report.md` | Present with limits | Raw local case report is not published by default. | Public docs and video show narrative plus public trace excerpt. |
| Constraint implementation | `src/server.py`, `docs/architecture.md`, `docs/mcp_architecture.md` | Strong locally | Public GitHub rendering still needs final verification. | Unsafe action is blocked and documented without risking original evidence. |
| Audit trail quality | Real local log plus public-safe real log excerpt | Strong locally | Public link/render audit remains external. | Judge can trace at least one key finding from report to evidence record and execution action. |
| Usability and documentation | README, architecture, dataset, audit docs | Partial | Public repo, real run, and public link checks remain open. | Another practitioner can understand setup, run path, outputs, and limitations without private context. |

## No-Go Until Closed

- demo video is missing;
- Devpost form is not submitted;
- public video and GitHub link checks are not complete.
