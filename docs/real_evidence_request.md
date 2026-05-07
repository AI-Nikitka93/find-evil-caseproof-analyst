# Real Evidence Request

Date: 2026-05-06  
Purpose: unblock the remaining Phase 2 real-evidence tasks and the later real SIFT validation lane.

## Current Local Evidence State

Local scan found only:

```text
fixtures/smoke.raw
```

Size:

```text
256 bytes
```

This is not a real SIFT disk image and cannot close the real evidence inventory or real validation tasks.

## Current Local SIFT Tool State

`py scripts/check_env.py --json` reports the real SIFT run as blocked because these required tools are missing from the current Windows environment:

- `mmls`
- `fls`
- `log2timeline.py`
- `psort.py`
- `rip.pl`

API readiness is configured, but SIFT forensic runtime readiness is not.

## Exact File Needed

Place one real SIFT-compatible Windows disk image in this folder:

```text
M:\Projects\Konkurs\Find Evil!\evidence\
```

Recommended filename:

```text
base-rd-01-cdrive.E01
```

Recommended source:

```text
FIND EVIL starter case data -> SRL-2018-Compromised Enterprise Network -> base-rd-01-cdrive.E01
```

If that file is unavailable, place one of these alternatives in the same folder:

```text
base-wkstn-01-c-drive.E01
base-file-cdrive.E01
base-dc-cdrive.E01
```

## Exact Environment Needed

Run the project in a SIFT-compatible environment where the following commands work:

```text
mmls
fls
log2timeline.py
psort.py
rip.pl
```

The SIFT Workstation path is preferred. A compatible environment is acceptable only if it exposes the same required forensic tools and can read the selected evidence image.

## What Will Be Closed After The File And Environment Exist

After the evidence image and SIFT environment are available, these remaining items can be honestly completed:

- T026: local evidence inventory;
- T027: chain-of-custody-style note;
- downstream real SIFT validation tasks that require the selected image and forensic tools.

T023, T024, T025, T028, T029, and T030 already have usable decision/readiness artifacts. They do not claim that real evidence validation has happened.

## Required Safety Rule

Do not place real evidence in the public repository package.

The `evidence/` folder must remain local-only and ignored by git.
