# Decisions

## 2026-05-04

Decision: Use a local FastMCP server over stdio for the first hackathon build.

Reason: The server is intended to run inside the SIFT/Claude Code environment
as a local process with constrained read-only tool contracts.

Rejected: Alternative agentic IDE path.

Reason for rejection: It relies more on prompt adherence than architectural
enforcement, which is weaker for evidence safety and judging criteria.

Directive: Keep the eight public tool names stable for P-BACKEND unless a
contract change is recorded here.

## 2026-05-04

Decision: Execute DFIR utilities only through fixed allowlisted wrapper calls
using `subprocess.run` with argument lists, captured output, `check=False`, and
timeouts.

Reason: The MCP server must expose forensic facts without exposing generic shell
access or write-capable command surfaces.

Rejected: Generic command execution tool.

Reason for rejection: It would move spoliation safety from architecture back to
prompt adherence.

Directive: Keep all output writes inside the registered case workspace and
preserve `FileNotFoundError` as a tool-level error for missing SIFT binaries.

## 2026-05-04

Decision: Use a single-agent + tools loop for the MVP agent client.

Reason: The workflow is narrow and sequential: open case, gather evidence,
verify claims, and write report. Multi-agent orchestration would add loop and
debugging risk without clear scoring upside at this stage.

Rejected: Multi-agent analyst/verifier split for MVP.

Reason for rejection: Verification is already enforced by the MCP
`verify_claim` tool and final-report prompt rules; separate agents can be added
after real dataset eval if needed.

Directive: Keep `MAX_ITERATIONS`, global timeout, tool-call budget, token
budget, and mandatory claim verification in place before any broader autonomy.

## 2026-05-04

Decision: Publish the current Accuracy Report as an initial synthetic benchmark
artifact, not as real SIFT image accuracy.

Reason: The dev environment lacks the large SIFT sample image and target VM
runtime, but the hackathon package still needs a transparent Accuracy Report
and Agent Execution Logs artifact.

Rejected: Claiming real 15GB image performance from mock data.

Reason for rejection: That would violate eval discipline and overstate current
evidence.

Directive: Any public packaging must label `docs/accuracy_report.md` and
`agent_execution_log.jsonl` as synthetic MVP validation until real dataset runs
replace them.

## 2026-05-06

Decision: Use `CaseProof Analyst` as the recommended public product name for
the world-class FIND EVIL submission direction.

Reason: The name frames the project as a proof-disciplined analyst rather than
as a generic wrapper or chatbot. It fits the selected strategy: real evidence,
visible self-correction, traceable findings, and an honest accuracy/trust
package.

Rejected: Presenting the project publicly only as `Evidence-Locked
Self-Correcting Disk Triage MCP`.

Reason for rejection: The old name is accurate for architecture, but it reads
like an implementation description. The submission needs a product-level story
that judges and practitioners can understand quickly.

Directive: Use `CaseProof Analyst` for positioning and submission narrative
unless the user explicitly chooses a different final name. Keep the technical
architecture language in docs where the MCP boundary must be precise.
