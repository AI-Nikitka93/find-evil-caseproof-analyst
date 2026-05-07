# Future Agent Project Instructions

Purpose: give future agents a stable, evidence-first entry path before changing
code, docs, or release materials.

## Required Read Order

Before editing, future agents must read:

1. `AGENTS.md`
2. `docs/PRODUCT_ANCHOR.md`
3. `docs/STATE.md`
4. `docs/EXEC_PLAN.md`
5. `docs/DECISIONS.md`
6. `docs/hackathon_strategy.md`
7. `docs/research_sift_mcp.md`

Then inspect only the files directly related to the current task.

## Operating Boundary

- Preserve the eight public MCP tool names unless `docs/DECISIONS.md` records a
  deliberate change.
- Keep the original evidence path read-only.
- Do not add generic shell access.
- Do not describe synthetic accuracy as real SIFT accuracy.
- Do not claim final submission readiness until video, Devpost text, public
  repository readiness, and real SIFT validation are complete.
- Do not treat configured candidate provider keys as implemented runtime
  support.

## Task Start Checklist

For every non-trivial task:

1. Identify the relevant master-plan item or documented blocker.
2. Check whether the task depends on the local-only `.E01` image, WSL
   SIFT-compatible runtime, or external public submission gates.
3. Check whether the result needs a document, code change, test, or release
   audit update.
4. Preserve unrelated user changes.
5. Verify with tests or targeted audits before marking the task complete.

## Completion Rule

A task is complete only when the result exists in the repository, is linked or
discoverable from project docs, passes relevant checks, and does not overstate
runtime, evidence, or submission readiness.
