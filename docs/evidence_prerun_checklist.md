# Evidence Run Preflight Checklist

Date: 2026-05-06

Purpose: provide a repeatable go/no-go procedure before any real evidence run.

## Intended Use

Run the automated preflight before starting the agent:

```text
py scripts\preflight_case.py --case-id CASE-RD01 --evidence-path "M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01" --case-workspace "M:\Projects\Konkurs\Find Evil!\cases\CASE-RD01" --json --strict
```

If the preflight returns `blocked`, do not start the real run.

After the preflight passes, run:

```text
python -m src.agent --case-id CASE-RD01 --evidence-path "M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01" --case-workspace "M:\Projects\Konkurs\Find Evil!\cases\CASE-RD01"
```

On Windows local dev, use `py` if `python` is not available:

```text
py -m src.agent --case-id CASE-RD01 --evidence-path "M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01" --case-workspace "M:\Projects\Konkurs\Find Evil!\cases\CASE-RD01"
```

## Required Inputs

The run cannot start unless all required inputs are present:

- case ID is explicit and does not reuse an old case workspace accidentally;
- evidence path points to the selected real disk image;
- case workspace is outside the original evidence folder;
- API readiness check passes without printing secrets;
- SIFT readiness check passes in the target forensic environment;
- previous synthetic-only results are not used as proof of real evidence accuracy.

## Evidence Path Gate

Expected first real evidence path:

```text
M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01
```

The evidence path must pass these checks:

- file exists;
- file size is compatible with a real disk image, not a tiny fixture;
- path is under the local ignored `evidence/` folder or an equivalent read-only evidence location;
- file is not inside `cases/`;
- file is not inside a generated output folder;
- file is not tracked as part of the public repository package.

## Workspace Gate

Expected workspace pattern:

```text
M:\Projects\Konkurs\Find Evil!\cases\<CASE-ID>\
```

The case workspace must pass these checks:

- workspace path exists or can be created;
- workspace is not the same as the evidence folder;
- generated logs, reports, indexes, and exports write only inside the workspace;
- previous run outputs are either intentionally reused or archived before a new run;
- no generated output path points back to original evidence.

## API Gate

Run:

```text
py -m src.agent --check-api
```

Pass condition:

- implemented agent runtime is configured;
- secret values are not printed;
- model selection is visible enough for run reproducibility;
- missing future-provider keys do not block the current implemented runtime.

## SIFT Tool Gate

Run:

```text
py scripts\check_env.py --json
```

In the target SIFT environment, pass condition:

- `mmls` resolves;
- `fls` resolves;
- `log2timeline.py` resolves;
- `psort.py` resolves;
- `rip.pl` resolves;
- readiness result says a real SIFT run is allowed.

If running inside SIFT with `python`, use:

```text
python scripts/check_env.py --json
```

## Original Evidence Safety Gate

The run is blocked if any planned operation would:

- write into the evidence folder;
- modify the selected disk image;
- copy generated artifacts over original evidence;
- expose generic destructive command access to the agent;
- treat a prompt rule as the only protection for original evidence.

## Output Completeness Gate

A real run is incomplete unless it can produce or update:

- case report;
- case execution log;
- evidence index or equivalent evidence references;
- correction or unsupported-claim record where applicable;
- updated dataset documentation;
- updated accuracy report.

## Stop Conditions

Stop before the run if:

- the selected evidence file is absent;
- SIFT commands are missing;
- workspace and evidence paths overlap;
- API check prints or exposes secrets;
- the run would only regenerate synthetic fixture artifacts;
- there is no way to preserve the original evidence as input-only.

## Current Local Status

Current Windows local status on 2026-05-06:

- API readiness: configured for the implemented runtime;
- SIFT readiness: blocked because required forensic tools are missing;
- evidence readiness: blocked because `base-rd-01-cdrive.E01` is not present locally;
- real validation readiness: no-go until both evidence and SIFT tool gates pass.

Current command result:

```text
py scripts\preflight_case.py --case-id CASE-RD01 --evidence-path "M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01" --case-workspace "M:\Projects\Konkurs\Find Evil!\cases\CASE-RD01" --json
```

Expected current result before the evidence file and SIFT runtime exist:

```text
status: blocked
failed checks include: evidence_exists, evidence_size, sift_ready
```
