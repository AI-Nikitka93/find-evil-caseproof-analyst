# Submission Release Contract

Updated: 2026-05-07  
Purpose: close TODO T013 and T020.

## Release Contract

The first full release is not submission-ready unless every required contest artifact exists, is linked from the public package, and matches the actual validated behavior of the project.

| Required artifact | Release-ready condition | Current blocker |
|---|---|---|
| Public code repository | Public URL is available, license is visible, setup instructions work, no secrets or private evidence are included. | Satisfied at https://github.com/AI-Nikitka93/find-evil-caseproof-analyst. |
| Demo video | Live terminal screencast shows real evidence, audio narration, and visible self-correction. | Demo video is not created. |
| Architecture diagram | Diagram clearly shows agent, SIFT tools, MCP server, evidence source, output flow, and trust boundary. | Public rendering still needs final verification. |
| Written project description | Story explains what it does, how it works at product level, challenges, learnings, tradeoffs, and next steps. | Devpost form is not submitted. |
| Dataset documentation | Real evidence source, tested scope, observed findings, and limitations are documented. | Bounded registry, event, and correlation content are documented; full Plaso timeline and deeper process/account corroboration remain open. |
| Accuracy report | Real-run findings, false positives, missed artifacts, hallucinated claims, and evidence integrity are documented. | Full incident reconstruction and official answer-key comparison remain unavailable. |
| Try-it-out instructions | A judge can follow setup, readiness checks, run path, expected outputs, and troubleshooting. | Clean external judge machine verification remains external. |
| Agent execution logs | Logs from the real case trace findings to actions and source references. | Full local log is under ignored `cases/`; public repo uses `docs/public_real_execution_log_sample.jsonl`. |

## Program-Level Phase Acceptance

The program cannot be called ready for final submission until:

- a real SIFT-compatible evidence run is completed;
- the real run produces analyst report, evidence book, correction ledger, accuracy report, and execution logs;
- a public-safe real execution-log excerpt is generated for the public repository;
- at least one self-correction sequence is visible in the real run or a controlled verification challenge;
- every confirmed finding in the final report has evidence support;
- original evidence remains input-only;
- synthetic artifacts are clearly separated from real validation artifacts;
- public README and Devpost copy do not overstate readiness;
- all eight contest artifacts are present and linked.

## No-Go Conditions

Submission remains blocked if any of these are true:

- final demo uses only synthetic fixture data;
- final accuracy report still describes only synthetic results;
- public package has missing or broken artifact links;
- execution logs do not support finding traceability;
- public-safe real execution-log excerpt is missing from the public package;
- unsupported claims appear as confirmed findings;
- public repository contains secrets, private evidence, or local-only files;
- setup instructions have not been validated in a SIFT-compatible environment.

## Release Use Rule

This contract is the gate for public submission. A checked TODO item in the master plan does not override this contract; evidence and verification artifacts do.
