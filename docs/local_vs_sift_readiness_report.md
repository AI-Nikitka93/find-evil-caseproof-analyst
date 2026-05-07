# Local Vs SIFT Readiness Report

Date: 2026-05-06  
Purpose: distinguish local Windows development readiness from real SIFT evidence-run readiness.

## Local Windows Development Readiness

Status: usable for code and documentation work.

Verified:

- Python launcher works through `py`;
- test suite passes;
- source files compile;
- API readiness reports configured Anthropic runtime without printing secret values;
- Groq and OpenRouter keys are detected as candidate adapters only;
- MCP server and agent code can be imported and tested locally;
- synthetic fixture workflows remain available for initial validation.

Not sufficient for:

- real SIFT evidence validation;
- real `.E01` inventory;
- real timeline generation;
- real registry parsing;
- final accuracy report;
- final demo video.

## Real SIFT Evidence-Run Readiness

Status: blocked.

Blocking facts:

- no real `.E01` evidence file exists in `evidence/`;
- only `fixtures/smoke.raw` exists locally and it is 256 bytes;
- `mmls` is missing;
- `fls` is missing;
- `log2timeline.py` is missing;
- `psort.py` is missing;
- `rip.pl` is missing.

## Current Readiness Command Result

Command:

```text
py scripts\check_env.py --json
```

Current real-run readiness:

```text
ready_for_real_sift_run: false
```

## Correct Interpretation

The project is locally usable for planning, code checks, synthetic validation, and public documentation preparation.

The project is not ready for final contest validation until a real evidence image and SIFT-compatible forensic runtime are available.

## Next Required Input

Place this file locally:

```text
M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01
```

Then run the project in a SIFT-compatible environment with:

```text
mmls
fls
log2timeline.py
psort.py
rip.pl
```
