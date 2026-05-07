# FIND EVIL Contest Freshness Audit

Checked: 2026-05-06  
Primary source: https://findevil.devpost.com/  
Purpose: close TODO T003 and T004 by comparing the current live contest page with local `УСЛОВИЯ.txt`.

## Live Facts Verified On 2026-05-06

| Area | Live fact |
|---|---|
| Contest name | FIND EVIL! |
| Tagline | AI threats strike in minutes. Build the defender that responds in seconds. |
| Deadline | Jun 15, 2026 @ 11:45pm EDT |
| Format | Online, public |
| Prize pool | $22,000 in cash |
| Participants visible on live page | 2639 participants |
| Sponsor | SANS |
| Main mission | Make Protocol SIFT a fully autonomous incident response agent. |
| Required platform direction | Build autonomous AI agents on SANS SIFT Workstation / Protocol SIFT. |
| Supported approaches | Direct Agent Extension, Custom MCP Server, Multi-Agent Frameworks, Alternative Agentic IDEs. |
| Custom MCP note | Live page calls Custom MCP Server the most sound architecture in the evaluation and also the most work. |
| Required components | Code repository, demo video, architecture diagram, written project description, dataset documentation, accuracy report, try-it-out instructions, agent execution logs. |
| Demo requirement | Live terminal screencast with audio narration, real case data, and at least one self-correction sequence. |
| Judging criterion 1 | Autonomous Execution Quality, marked as tiebreaker. |
| Judging criterion 2 | IR Accuracy. |
| Judging criterion 3 | Breadth and Depth of Analysis; depth on fewer types beats shallow coverage of many. |
| Judging criterion 4 | Constraint Implementation; architectural vs prompt-based guardrails and bypass testing. |
| Judging criterion 5 | Audit Trail Quality; trace findings back to specific tool execution. |
| Judging criterion 6 | Usability and Documentation. |

## Local Snapshot Comparison

| Topic | Local `УСЛОВИЯ.txt` | Live page on 2026-05-06 | Impact |
|---|---|---|---|
| Deadline timezone | 16 Jun 2026 @ 6:45am GMT+3 in the localized header; official rules also state Jun 15, 2026 11:45pm EDT. | Jun 15, 2026 @ 11:45pm EDT. | Use the EDT deadline as public source of truth and keep the Minsk/GMT+3 equivalent only as internal planning context. |
| Participants | Local snapshot showed 2549 participants. | Live page shows 2639 participants. | Participant count is volatile and should not be used as a stable claim in submission copy. |
| Prize pool | $22,000 in cash. | $22,000 in cash. | No change. |
| Required components | Eight components listed. | Same eight components listed. | No change. |
| Judging criteria | Six criteria listed with autonomy first. | Same criteria; autonomy explicitly tiebreaker. | No change; autonomy remains highest tie-break priority. |
| Custom MCP framing | Most sound architecture, most work. | Same framing. | Confirms selected architecture remains strategically strong. |
| Demo requirement | Live terminal execution, real evidence, self-correction. | Same requirement. | Synthetic-only demo remains unacceptable. |

## Freshness-Sensitive Items To Recheck Before Release

- contest deadline and submission page requirements;
- demo video visibility and length rules;
- required repository/license wording;
- starter evidence availability;
- Protocol SIFT install guidance;
- SIFT Workstation download/install page;
- public participant count if mentioned anywhere;
- AI runtime availability and limits if runtime choices are described publicly.

## Current Product Implication

The live contest page supports the CaseProof Analyst direction:

- real evidence and real tools matter more than a toy demo;
- Custom MCP remains the strongest safety architecture;
- depth on fewer evidence types is explicitly acceptable;
- visible self-correction is mandatory for the demo;
- execution logs and traceability are not optional;
- public copy must not imply final readiness until real SIFT validation replaces synthetic-only artifacts.
