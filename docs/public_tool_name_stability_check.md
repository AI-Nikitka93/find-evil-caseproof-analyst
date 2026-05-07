# Public Tool Name Stability Check

Date: 2026-05-06

Purpose: verify that the public MCP tool surface remains stable.

## Required Public Tool Names

```text
case_open_readonly
list_partitions
filesystem_inventory
build_timeline
extract_registry_persistence
extract_event_records
verify_claim
write_execution_log
```

## Current Verification

The repository test suite checks that:

- each required tool name appears in `src/server.py`;
- `@mcp.tool()` count equals the expected tool count;
- the server uses `FastMCP`;
- the server does not use the rejected `MCPServer` bootstrap path.

Verification command:

```text
py -m pytest tests/test_server_contracts.py
py scripts\audit_release_controls.py --json --strict
```

## Change Rule

Tool names must not change unless:

- the change is recorded in `docs/DECISIONS.md`;
- README and architecture docs are updated;
- tests are updated intentionally;
- submission copy explains the changed public surface;
- old names are not silently broken.

## Current Result

Current public tool names match the required eight-tool contract.

## Acceptance

This check is complete when:

- the eight tool names are listed in one place;
- the current test suite enforces them;
- the decision log still says to preserve the public names;
- no unrecorded rename is present.
