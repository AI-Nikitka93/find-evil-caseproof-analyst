# SIFT Readiness Gate

Date: 2026-05-06  
Current status: BLOCKED in the current Windows environment.

## Required For Real SIFT Run

The real run gate requires all of these to be true:

- a real `.E01` or equivalent SIFT-compatible evidence file exists locally;
- original evidence is stored under the local ignored `evidence/` folder;
- case output workspace is separate from the evidence folder;
- required forensic commands are available;
- API readiness check passes without printing secrets;
- the agent can start the local MCP server;
- the environment can produce outputs under `cases/<CASE-ID>/`.

## Required Forensic Commands

The current first-release lane requires:

```text
mmls
fls
log2timeline.py
psort.py
rip.pl
```

## Current Verification Result

Current command:

```text
py scripts\check_env.py --json
```

Current result:

```text
status: blocked
missing_required_sift_binaries:
  - mmls
  - fls
  - log2timeline.py
  - psort.py
  - rip.pl
ready_for_real_sift_run: false
```

## WSL Probe

WSL Ubuntu is available, but the required SIFT forensic commands were not found there during the current check.

## Gate Decision

Real SIFT validation cannot start in the current environment.

This is a correct gate result, not a completed real validation result.

## What Unblocks The Gate

To pass this gate:

1. Put the selected evidence file at:

```text
M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01
```

2. Use a SIFT-compatible environment where these commands resolve:

```text
mmls
fls
log2timeline.py
psort.py
rip.pl
```

3. Re-run the readiness check in that environment.
