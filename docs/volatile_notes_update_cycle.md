# Volatile Notes Update Cycle

Date: 2026-05-07

Purpose: keep contest, dataset, runtime, and submission assumptions current until final submission.

## Update Register Location

Primary register:

```text
docs/freshness_dependency_register_2026-05-06.md
```

Current release checklist:

```text
docs/pre_release_freshness_checklist.md
```

History log:

```text
docs/PROJECT_HISTORY.md
```

## What To Recheck

Recheck these facts as volatile:

- contest deadline and schedule;
- required submission components;
- demo video constraints;
- public repository and license rules;
- starter evidence link availability;
- selected evidence file availability;
- SIFT Workstation download path and version notes;
- Protocol SIFT install instructions;
- AI runtime and local key readiness;
- public documentation claims about real vs synthetic validation.

## When To Recheck

Recheck at these points:

- before any final evidence download;
- before the first real SIFT validation run;
- before recording the final demo video;
- before publishing final README/release notes;
- before submitting Devpost;
- after any failed evidence, SIFT, or API run that may indicate a changed external dependency.

## Update Entry Format

Each update entry must include:

```text
date_checked:
source_or_command:
fact_checked:
previous_value:
current_value:
changed: yes/no
release_impact:
document_updates_required:
owner_note:
```

## Staleness Labels

Use these labels:

- `current`: checked in the current release window;
- `watch`: likely to change, but not blocking now;
- `stale`: must be rechecked before use;
- `changed`: changed from prior assumption;
- `blocked`: change prevents release or real validation.

## Documentation Rule

If a volatile fact changes:

- update the source document that depends on it;
- update the readiness audit if release impact changes;
- update dataset documentation if evidence access changes;
- update README only after the new fact is verified;
- preserve the old fact in history instead of silently rewriting the past.

## Current Baseline

As of 2026-05-07:

- FIND EVIL overview and rules were live-checked again.
- Protocol SIFT repository HEAD is still `40bed7a96bfd986ea048c3b2aeb9d788b2f3400c`.
- Official MCP Python SDK `mcp 1.27.0` is the current project dependency target and is installed in the active Python runtime.
- The selected `base-rd-01-cdrive.E01` evidence file is present locally under the ignored `evidence/` folder.
- SIFT-compatible commands are available through WSL for the current local validation path.
- Public Devpost submission remains blocked only by the missing public demo video URL and submitted Devpost URL.

## Stop Conditions

Stop release or real validation if:

- required contest components change and local artifacts no longer satisfy them;
- starter evidence becomes inaccessible and no fallback is validated;
- SIFT setup instructions change enough to break judge reproducibility;
- public docs still imply real validation when only synthetic validation exists.
