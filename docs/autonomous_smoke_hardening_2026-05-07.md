# Autonomous Smoke Hardening

Date: 2026-05-07

## Purpose

Record the concrete agent-loop hardening done after live OpenRouter smoke runs
against `base-rd-01-cdrive.E01`.

## Observed Failure Modes

1. The system prompt told the model to call `write_execution_log` manually even
   though the runtime already logs MCP tool calls. Some model-generated log
   calls were incomplete and wasted iterations.
2. The model generated an invalid MCP tool name, `None`, during one smoke run.
   The agent previously passed that request to the MCP server.
3. A broad `filesystem_inventory` result was returned to the model context in
   full. The next OpenRouter request failed with HTTP 400 because the request
   approached 1.2 million tokens.
4. The final report prompt did not provide exact stop-limit numbers, allowing a
   short-run report to say the tool-call budget was exhausted when the actual
   stop reason was the iteration limit.

## Hardening Added

- `src.agent` now repairs incomplete `write_execution_log` inputs with run,
  case, evidence, step, parser-status, and intent defaults.
- The prompt now states that the runtime automatically logs every MCP tool call;
  manual `write_execution_log` is reserved for extra rationale around
  self-correction, unsupported claims, parser failures, and final decisions.
- Unknown model-generated tool names are rejected before the MCP server is
  called.
- Large MCP tool outputs are compacted before being returned to the model. Full
  outputs remain available through exported files and execution logs.
- Common model argument mistakes are repaired before tool execution:
  `filesystem_inventory` gets a safe default `partition_start_sector=0` and a
  bounded root inventory when the model omits scope; `build_timeline` receives
  `source_path` and drops unsupported `image_path`.
- The final no-tools report prompt now includes exact iteration and tool-call
  counts and forbids claiming tool-call exhaustion unless that actually
  happened.

## Latest Smoke Evidence

`CASE-RD01-AUTO-SHORT-PASS` completed and wrote a report after a short
OpenRouter run. It demonstrated that the agent can open the evidence, list the
volume, and stop without promoting unsupported findings.

`CASE-RD01-AUTO-SHORT-TRUTH` also completed cleanly, but the selected free model
returned fallback-level output before calling tools. This confirms the project
should present OpenRouter as a bounded smoke/runtime path, not as proof of full
autonomous incident reconstruction.

The judge-facing demo should therefore keep the deterministic real evidence run
as the primary proof path and use the autonomous smoke only as a bounded model
loop demonstration.
