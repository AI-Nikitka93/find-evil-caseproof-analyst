# Local-Only Notes Audit

Date: 2026-05-06

Purpose: ensure notes about secrets, credentials, local paths, evidence files, and generated case workspaces stay out of the public release surface.

## Local-Only Surfaces

These paths are intentionally local-only:

```text
.env
.env.*
docs/*.local.md
cases/
fixtures/
evidence/
__pycache__/
.pytest_cache/
```

Shareable exception:

```text
!.env.example
```

## Current Secret Notes Location

Current local secret map:

```text
docs/SECRETS_INDEX.local.md
```

This file matches the ignored `docs/*.local.md` rule and must remain local-only.

## Current Evidence Location

Expected local evidence folder:

```text
M:\Projects\Konkurs\Find Evil!\evidence\
```

Current required file:

```text
M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01
```

The folder is ignored and currently does not contain the selected evidence file.

## Current Case Workspace Location

Expected generated case workspace:

```text
M:\Projects\Konkurs\Find Evil!\cases\CASE-RD01\
```

The folder is ignored because generated logs, exports, indexes, and reports may contain local paths or case-derived material.

## Publicly Safe References

The public docs may mention:

- environment variable names;
- placeholder values such as `your-key`;
- candidate model/provider names;
- expected local path patterns;
- current blocker status;
- source category for evidence.

The public docs must not contain:

- real API key values;
- real bearer tokens;
- copied secret snippets;
- credential files;
- real generated case workspaces;
- large evidence images;
- hidden local account notes.

## Current Scan Result

The executable audit is:

```text
py scripts\audit_release_controls.py --json --strict
```

The current scan found only expected references:

- README setup examples use placeholder text;
- source code reads environment variables without printing values;
- tests use synthetic `secret-value` strings to prove redaction;
- local secret map uses `.local.md` naming;
- readiness checks report configured/missing status only.

## Acceptance

This audit passes when:

- `.gitignore` contains the local-only patterns above;
- secret notes use `.local.md`;
- readiness outputs do not print secret values;
- real evidence and generated case folders are ignored;
- no public document contains a real credential value;
- `scripts/audit_release_controls.py --strict` returns success.
