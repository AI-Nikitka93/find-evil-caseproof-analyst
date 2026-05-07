# FIND EVIL! Hackathon Strategy

Date: 2026-05-04  
Internal delivery freeze: 2026-06-15, using the user's earlier deadline as the planning constraint. The local brief shows the Devpost deadline as 2026-06-16 06:45 GMT+3, so the strategy keeps one buffer day.  
Source of truth: `УСЛОВИЯ.txt` and the judging criteria in that file.

## 1. Executive Verdict

Build a narrow, evidence-safe **Custom MCP Server** for one deep use case:

> **Evidence-Locked Self-Correcting Disk Triage MCP**: a Protocol SIFT extension that performs read-only initial triage on a mounted disk image, produces artifact-backed findings, rejects unsupported claims, and re-runs targeted checks when evidence conflicts or confidence is too low.

This is a synthesis of starter idea **#6 Purpose-Built MCP Server** and the most judge-relevant part of **#1 Self-Correcting Triage Agent**, with a minimal scoring harness inspired by **#5 Accuracy Benchmarking Framework** only where it is needed for the required Accuracy Report.

The winning bet is not broad SIFT coverage. The winning bet is a demonstrable system where:

- the model cannot mutate evidence because destructive commands are not exposed;
- every finding has a specific tool call, artifact path, timestamp/offset where available, and parsed evidence record;
- hallucinations are caught by a claim verifier before the final report;
- the demo shows at least one autonomous correction sequence;
- the Accuracy Report and Agent Execution Logs are generated from the same run data judges can inspect.

Status: **DONE for strategy handoff.** This document intentionally does not choose implementation libraries or MCP SDK details; that belongs to the next research/architecture step.

## 2. Goal And Constraint Clarity

Goal clarity: **High.** The hackathon rewards autonomous incident response quality, not generic AI chat. The brief explicitly emphasizes self-correction, evidence integrity, accuracy validation, and traceability.

Constraint clarity: **Medium-High.** The allowed architecture families and submission components are clear. The unknowns are exact Protocol SIFT interfaces, exact SIFT tool availability in the target workstation, sample dataset structure, and MCP packaging details. These unknowns affect implementation, not the strategic choice.

Key resolved decision:

- Do **not** attempt to wrap 200+ SIFT tools during the MVP.
- Do **not** build a general multi-agent DFIR platform.
- Do **not** rely on prompt-only safety controls.
- Do **not** choose Alternative Agentic IDEs because the brief says their evidence protection relies on prompt adherence instead of architectural enforcement.

## 3. Active P-10X Modules

ACTIVE MODULES: M2, M3, M4-light, M5-light, M6, M7

- M2: Segment and job are the judges plus DFIR practitioners evaluating trustable autonomous triage.
- M3: Positioning and wedge are architectural evidence safety plus traceable self-correction.
- M4-light: No pricing work is needed; business model is irrelevant for this hackathon.
- M5-light: Market sizing is irrelevant; strategic shape matters because depth beats shallow breadth.
- M6: Risk and validation are central because hallucination, spoliation, and auditability decide the score.
- M7: Handoff is needed for P-18 and P-20 after this strategy document.

## 4. Observed / Inferred / Hypothesis

### Observed

- Four supported approaches are allowed: Direct Agent Extension, Custom MCP Server, Multi-Agent Frameworks, and Alternative Agentic IDEs.
- The brief calls Custom MCP Server the most sound architecture in the evaluation and also the most work.
- The brief states that Alternative Agentic IDEs rely on prompt adherence for evidence protection, not architectural enforcement.
- All eight submission components are mandatory; missing any one means elimination.
- Required submission artifacts include Accuracy Report and Agent Execution Logs.
- Judging criteria include Autonomous Execution Quality, IR Accuracy, Breadth and Depth, Constraint Implementation, Audit Trail Quality, and Usability/Documentation.
- Breadth and Depth explicitly says depth on fewer types beats shallow coverage of many.
- Constraint Implementation asks whether guardrails are architectural or prompt-based and whether bypass was tested.
- Audit Trail Quality asks whether judges can trace findings back to specific tool executions.

### Inferred

- A narrow Custom MCP Server should score better on Constraint Implementation than prompt-only Direct Agent Extension because the tool boundary physically limits what the model can execute.
- A single deep disk-triage lane is more competitive than shallow coverage across disk, memory, network, SIEM, and endpoint sources because the brief explicitly favors depth.
- A built-in claim verifier is more judge-aligned than a polished final report alone because the IR Accuracy criterion asks whether hallucinations are caught and flagged.
- Structured execution logs should be treated as a first-class product surface, not an afterthought, because Agent Execution Logs are both mandatory and central to Audit Trail Quality.

### Hypothesis

- Judges will reward a smaller, safer, reproducible triage path over a broader demo that depends on prompt discipline.
- A two-month build can deliver a high-quality narrow MCP server plus self-correction loop, but not a credible 200+ tool wrapper suite.
- The best first dataset target is a Windows disk image because common DFIR artifacts can be cross-checked across filesystem metadata, timelines, registry-derived persistence, event records, and executable traces.

## 5. Architecture Comparison

| Approach | Winning upside | Main risk | Constraint Implementation | Audit Trail Quality | Verdict |
|---|---|---|---|---|---|
| Direct Agent Extension | Fastest path to a working demo; natural fit for improving Protocol SIFT loop, prompts, sequencing, and self-correction. | Safety and evidence integrity depend heavily on agent behavior unless tool access is restricted elsewhere. Can look like prompt engineering instead of a stronger system. | Medium. Guardrails can be written into prompts and workflows, but the model may still have broad shell access if not architecturally limited. | Medium. Logs can be added, but traceability depends on disciplined wrapper design. | Rejected as primary architecture. Useful as the agent shell around the MCP server, not as the core differentiator. |
| Custom MCP Server | Strongest fit for evidence integrity: expose typed read-only DFIR functions instead of generic shell commands. Can parse output before returning to the model and reduce context overload. | Most work. Full 200+ tool wrapping is unrealistic for the deadline. | High. The server does not expose destructive tools, writes only to a case workspace, and validates allowed paths/actions before execution. | High. Every MCP function can emit structured run records with tool name, arguments, evidence path, output hash, parser status, and finding links. | **Selected.** Narrow scope makes it feasible while preserving the strongest judging advantage. |
| Multi-Agent Frameworks | Good for decomposing complex cases and producing structured agent-to-agent logs. Helps context management. | Adds orchestration complexity, loop failure risk, and more moving parts before the evidence boundary is solved. | Medium. Multi-agent design does not automatically enforce evidence safety; it still needs restricted tools underneath. | High for conversation logs, but weaker if raw tool executions are not normalized and linked to findings. | Rejected for MVP. Could be a later extension after the MCP safety boundary exists. |
| Alternative Agentic IDEs | Strong UX and fast iteration for software development workflows. | Brief explicitly warns these tools are not designed for incident response and rely on prompt adherence for evidence protection. | Low-Medium. Prompt-based restrictions are weaker and must document what happens when ignored. | Medium. IDE logs/diffs are not the same as DFIR evidence provenance. | Rejected by constraint. It directly conflicts with the requested strategy and the judging emphasis on architectural guardrails. |

## 6. Idea Selection

### Selected Idea

**Evidence-Locked Self-Correcting Disk Triage MCP**

Base idea: **#6 Purpose-Built MCP Server**  
Self-correction mechanism: focused subset of **#1 Self-Correcting Triage Agent**  
Accuracy evidence: minimal internal benchmark/report mechanism inspired by **#5 Accuracy Benchmarking Framework**

This is one use case, not three separate products. The product surface is a disk-triage agent with a read-only MCP evidence boundary and verifier loop.

### Why Not The Other Starter Ideas

| Starter idea | Decision | Reason |
|---|---|---|
| #1 Self-Correcting Triage Agent | Partially absorbed | Strong for Autonomous Execution, but too weak on Constraint Implementation if built as prompt/workflow only. Used as the correction loop inside the selected MCP approach. |
| #2 Multi-Source Correlation Engine | Rejected for MVP | Disk+memory correlation is valuable but doubles dataset/tool complexity. It risks shallow coverage and delays the core safety boundary. |
| #3 MCP-Connected Live Triage | Rejected for MVP | Live endpoint/SIEM integration adds environment and access risk. Harder for judges to reproduce locally. |
| #4 Analyst Training Loop | Rejected for MVP | Strong documentation/training angle, but less direct scoring leverage on architectural constraints and evidence integrity. |
| #5 Accuracy Benchmarking Framework | Partially absorbed | Critical for Accuracy Report, but a benchmark alone may not look like a fully autonomous incident response agent. Use it as validation infrastructure, not the main product. |
| #6 Purpose-Built MCP Server | Selected, narrowed | Best fit for architectural enforcement, audit trail, and practitioner trust. Narrowing avoids the 200+ tool trap. |
| #7 Persistent Learning Loop | Rejected for MVP | Useful idea, but persistent learning across iterations can become hard to bound. A deterministic verifier/correction loop is safer for judges and easier to audit. |

## 7. MVP Scope

### Target Case Type

One deep lane: **Windows disk image initial triage**.

The MVP should not claim full DFIR coverage. It should claim:

- initial triage of one mounted/acquired disk image;
- read-only artifact extraction;
- suspicious activity timeline and persistence indicators;
- claim verification against specific artifacts;
- autonomous retry/correction when findings are unsupported or conflicting;
- structured report plus execution logs.

### First SIFT Tool Wrappers

Wrap capabilities, not every tool. The initial MCP server should expose typed functions around these SIFT-level tool surfaces:

| MCP function family | SIFT/tool surface to validate in P-18 | Purpose | Evidence returned to model |
|---|---|---|---|
| `case_open_readonly` | mount/image metadata commands available on SIFT | Register evidence source, enforce read-only mode, create case workspace outside original evidence. | Evidence ID, image path, read-only status, hash/check metadata where available. |
| `list_partitions` | Sleuth Kit partition/filesystem inspection such as `mmls` and `fsstat` | Identify partitions and filesystem context before analysis. | Partition table, filesystem type, offsets, parser status. |
| `filesystem_inventory` | Sleuth Kit file listing/stat extraction such as `fls`, `istat`, `icat` | Enumerate high-value paths without giving the model shell access. | File paths, inode/metadata records, timestamps, hashes when generated. |
| `build_timeline` | SIFT timeline tooling such as Plaso/log2timeline + psort or bodyfile-compatible fallback | Produce normalized activity timeline for a bounded time range. | Timeline rows with timestamp, source, artifact path, description, parser confidence. |
| `extract_registry_persistence` | SIFT registry artifact tooling such as RegRipper-style plugins or Plaso parsers | Detect common Windows persistence and execution traces. | Run keys/services/scheduled-task related records with registry path and source hive. |
| `extract_event_records` | SIFT EVTX parsing surface | Pull selected security/system/application event records relevant to logon, service changes, process execution if present. | Event ID, timestamp, provider, record ID, rendered fields, source path. |
| `verify_claim` | Internal verifier over normalized evidence store | Check whether a proposed finding is supported by at least one evidence record. | `confirmed`, `inferred`, or `unsupported`, with linked evidence IDs. |
| `write_execution_log` | Internal append-only logging surface | Persist full run trace for Agent Execution Logs. | Tool calls, arguments, timestamps, output references, parser errors, token usage if available. |

P-18 must validate exact command names and versions inside SIFT before implementation. The strategy decision is the wrapper boundary and evidence contract, not a commitment to a specific library.

### Explicit Non-Scope

- No full 200+ SIFT tool wrapping.
- No memory capture analysis in the first MVP.
- No network pcap lane in the first MVP.
- No live SIEM or remote endpoint integration.
- No multi-agent framework in the first MVP.
- No broad shell access for the LLM.
- No final finding without linked evidence.

## 8. Autonomous Execution Design

The agent loop should be judged as autonomous because it performs a bounded analysis cycle without human correction:

1. Opens case through the MCP read-only boundary.
2. Builds initial filesystem and timeline context.
3. Extracts selected artifact families.
4. Drafts findings as structured claims.
5. Runs each claim through `verify_claim`.
6. If a claim is unsupported, the agent either drops it or runs a targeted follow-up wrapper call.
7. If evidence conflicts, the agent records the conflict and asks the wrapper for the next bounded artifact check.
8. Emits final report with labels: `Confirmed`, `Inferred`, `Unsupported dropped`, and `Needs human review`.

Hard execution limits:

- max iterations per finding;
- max total tool calls per case;
- max output rows per wrapper call unless paginated;
- no write access to original evidence path;
- all generated outputs stored in a separate case workspace;
- parser errors become reportable uncertainty, not hidden failures.

This gives judges a visible self-correction sequence without relying on an unbounded persistent learning loop.

## 9. Accuracy Report Mapping

The Accuracy Report should be generated from the same normalized evidence store and logs used by the agent.

Required report sections:

| Accuracy Report section | How this strategy supports it |
|---|---|
| Findings accuracy | Every finding must link to evidence IDs produced by MCP wrappers. |
| False positives | Unsupported or contradicted claims are counted and shown as dropped or corrected. |
| Missed artifacts | A small test manifest for the chosen dataset lists expected artifact families; missed categories are documented honestly. |
| Hallucinated claims | Any claim with no supporting evidence link is blocked from final `Confirmed` output and counted. |
| Evidence integrity | Original evidence path is never exposed to write-capable commands; MCP functions are read-only by design. |
| Spoliation testing | Include a bypass test where the agent attempts or requests a destructive action and the server refuses because no destructive function exists. |
| Confidence discipline | Final report separates `Confirmed`, `Inferred`, and `Needs human review`. |

## 10. Agent Execution Logs Mapping

Agent Execution Logs are a core deliverable, not a debug file.

Each run should emit structured records with:

- run ID and case ID;
- step number;
- timestamp;
- agent intent;
- MCP function name;
- sanitized arguments;
- evidence source ID;
- output reference path;
- parser status;
- output row count;
- output hash or checksum where practical;
- claim IDs created from that output;
- verification result for each claim;
- retry/correction reason;
- token usage if available from the agent framework.

Judges should be able to click from:

`final finding -> claim ID -> evidence record -> MCP function call -> original artifact path/offset/timestamp where available`.

## 11. Judging Criteria Fit

| Criterion | Strategy fit | Why this can score |
|---|---|---|
| Autonomous Execution Quality | High | The agent plans, extracts, verifies, drops unsupported claims, and re-runs targeted checks under bounded iteration rules. |
| IR Accuracy | High | Findings are not accepted unless supported by parsed evidence; unsupported claims are explicitly counted and suppressed from confirmed output. |
| Breadth and Depth | High for depth, intentionally narrow breadth | One disk-image lane is deep enough to show real DFIR reasoning. This aligns with "depth on fewer types beats shallow coverage of many." |
| Constraint Implementation | Very high | The Custom MCP Server enforces read-only typed functions. Guardrails live at the tool boundary, not only in prompts. |
| Audit Trail Quality | Very high | Every wrapper call creates structured logs and every finding links back to tool execution and evidence records. |
| Usability and Documentation | Medium-High | A narrow local SIFT workflow is easier for judges to run and reproduce than live endpoint/SIEM integrations. |

## 12. Main Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Custom MCP scope still grows too large | High | Freeze to one case type and the listed wrapper families. Any new artifact family must replace an existing one, not add breadth. |
| Exact SIFT command availability differs from assumptions | High | P-18 validates command names, versions, output formats, and fallback paths before P-20 architecture. |
| Parser output is noisy or too large for the model | Medium-High | MCP server returns normalized, bounded, paginated records and stores full raw outputs outside model context. |
| Self-correction becomes performative | Medium | Require a visible correction event in demo: unsupported claim -> verifier rejection -> targeted tool call -> corrected final report. |
| Accuracy baseline is weak | Medium | Use a small known-answer dataset or manually documented ground-truth manifest for the MVP lane. |
| Judges expect broader coverage | Medium | The brief explicitly rewards depth over shallow breadth; documentation must say the product is a deep safety-first slice, not a full DFIR replacement. |

## 13. MVP Deliverable Shape

The MVP should produce these artifacts from a single run:

- `report.md`: final analyst-readable triage report.
- `accuracy_report.md`: false positives, missed artifacts, hallucinated/dropped claims, evidence integrity approach, spoliation/bypass test result.
- `agent_execution_log.jsonl`: append-only structured tool execution and correction trace.
- `evidence_index.json`: normalized evidence records and IDs.
- `architecture_diagram.md` or image source: shows agent, MCP boundary, read-only evidence source, parser/output store, and report pipeline.
- `dataset_documentation.md`: dataset source, expected artifact families, and what was found.

These artifacts map directly to the required submission components and reduce last-week scramble risk.

## 14. Handoff To P-18

P-18 should research and verify:

- exact Protocol SIFT MCP integration model and supported server/client patterns;
- exact SIFT Workstation command availability for Sleuth Kit, timeline, registry, and EVTX workflows;
- safe read-only mounting or evidence access pattern in the SIFT environment;
- sample case datasets available from the hackathon resources and which one supports the Windows disk triage lane;
- output formats for chosen tools and how stable they are for parsing;
- how to capture token usage from the selected agent framework if available;
- what a credible spoliation/bypass test should include without risking real evidence mutation.

P-18 should not reopen the strategic architecture choice unless it finds a hard blocker that makes Custom MCP infeasible inside the deadline.

## 15. Handoff To P-20

P-20 should turn this strategy into architecture after P-18 verifies the technical facts:

- MCP server boundary and function contracts;
- evidence store schema;
- execution log schema;
- claim verifier contract;
- read-only evidence access model;
- bounded agent loop;
- report generation pipeline;
- test plan for accuracy, spoliation refusal, and traceability.

P-20 should preserve the core strategy: narrow disk triage, architectural guardrails, evidence-linked findings, and visible self-correction.

## 16. Final Self-Check

- Selected architecture is one of the four supported approaches: **Yes, Custom MCP Server.**
- Alternative Agentic IDE was not selected: **Yes, rejected.**
- One concrete idea was selected: **Yes, Evidence-Locked Self-Correcting Disk Triage MCP.**
- MVP respects "Depth on fewer types beats shallow coverage": **Yes, one Windows disk image lane.**
- Constraint Implementation is architectural, not prompt-only: **Yes, typed read-only MCP functions.**
- Accuracy Report is explicitly supported: **Yes, section 9.**
- Agent Execution Logs are explicitly supported: **Yes, section 10.**
- No code implementation or library commitment was made: **Yes, deferred to P-18/P-20.**
