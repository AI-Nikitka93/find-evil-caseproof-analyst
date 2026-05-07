# AI Skill Stack Decision

Date: 2026-05-06

Decision: skip automatic AI skill installation for the first full release and
use manual, project-specific agent rules instead.

## Decision State

| Area | Decision | Reason |
|---|---|---|
| Automatic install | SKIP | The dry run suggested useful generic skills, but one suggested skill included a security warning and the project is evidence-safety sensitive. |
| Manual skill path | USE | Current project rules are narrower and safer: evidence read-only, no generic shell, no unsupported final findings, and explicit verification before completion. |
| Lock or manifest | NOT CREATED | No skill files were installed, so there is no installed skill set to lock. |
| Future reassessment | ALLOWED | Reassess only if a future agent workflow has a specific gap that current project instructions and tests do not cover. |

## Required Operating Rule

Future agents must not treat generic coding skills as project authority. Project
authority remains:

1. `AGENTS.md`
2. `docs/PRODUCT_ANCHOR.md`
3. `docs/STATE.md`
4. `docs/DECISIONS.md`
5. `docs/trust_boundary_contract.md`
6. `docs/public_tool_safety_acceptance.md`

## Allowed Future Path

A future skill may be installed only when all of the following are true:

- the current README, license, and security model were checked on the date of
  installation;
- the skill does not introduce broad command execution as a hidden default;
- it does not index or expose `evidence/`, `cases/`, local credentials, or
  private run outputs;
- it improves a concrete project task rather than adding generic agent
  capability;
- tests and release-control audit pass after installation.

## Rejected Path

Do not auto-install the dry-run suggestions just because they match Python or
Pydantic. For this project, evidence safety and traceability are stronger than
generic agent convenience.
