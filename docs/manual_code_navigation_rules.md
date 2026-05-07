# Manual Code Navigation Rules

Date: 2026-05-06

Purpose: define the fallback workflow while SocratiCode or another codebase intelligence index is not active.

## Decision

Use manual project navigation for now.

Reason:

- current repo is small enough for exact search;
- Docker daemon is not reachable for SocratiCode setup;
- no shared codebase index is required for the current single-agent workflow;
- manual search avoids indexing local-only evidence and secret files.

## Rules

Use this order:

1. Read `docs/PRODUCT_ANCHOR.md`.
2. Read `docs/STATE.md` and `docs/state.json`.
3. Search before reading broad file sets.
4. Use exact fast local search for identifiers, tool names, task IDs, and command names.
5. Read only the files needed for the current task.
6. Do not read ignored evidence or case folders unless the user explicitly asks and the file is needed.
7. Do not print secret values.
8. Verify with tests or scripts before claiming completion.

## Preferred Commands

```text
rg -n "pattern" .
rg --files
py -m pytest tests
py scripts\check_env.py --json
py scripts\preflight_case.py --case-id CASE-RD01 --evidence-path "M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01" --case-workspace "M:\Projects\Konkurs\Find Evil!\cases\CASE-RD01" --json
py scripts\audit_release_controls.py --json --strict
```

## Stop Conditions

Stop and ask for the missing artifact when:

- the task requires the real `.E01`;
- the task requires SIFT commands that are not available;
- the task requires a real source/hash that is not present locally.

## Acceptance

These rules are usable because they preserve the project anchor, avoid broad blind reading, protect local-only material, and keep exact search as the default.
