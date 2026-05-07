# Judge Try-It-Out And Recovery Guide

Date: 2026-05-07  
Audience: FIND EVIL judges and practitioners testing the repository locally.

## Prerequisites

- Python 3.10 or newer.
- SIFT-compatible Linux terminal or WSL environment exposing:
  - `mmls`;
  - `fls`;
  - `log2timeline.py`;
  - `psort.py`;
  - `rip.pl` or compatible RegRipper executable.
- One implemented model provider key for autonomous mode:
  - preferred current path: `OPENROUTER_API_KEY`;
  - optional: valid `ANTHROPIC_API_KEY`;
  - Groq is implemented and currently passes API readiness here, but use the
    provider that is freshly verified for your run.
- Real evidence file placed under `evidence/`.

## Setup

```bash
python -m pip install -r requirements.txt
```

PowerShell fallback when `python` is not on `PATH`:

```powershell
py -m pip install -r requirements.txt
```

## Configure Runtime

Use environment variables or `.env.local`. Never commit `.env.local`.

```bash
export FIND_EVIL_AGENT_PROVIDER=auto
export OPENROUTER_API_KEY=your-key
```

PowerShell:

```powershell
$env:FIND_EVIL_AGENT_PROVIDER="auto"
$env:OPENROUTER_API_KEY="your-key"
$env:MCP_SERVER_COMMAND="py"
```

Check API readiness without printing keys:

```bash
python -m src.agent --check-api
```

PowerShell:

```powershell
py -m src.agent --check-api
```

## Check SIFT Runtime

```bash
python scripts/check_env.py --strict
```

PowerShell:

```powershell
py scripts\check_env.py --strict
```

Expected result:

- status `ok`;
- required SIFT commands found;
- `Ready for real SIFT run: True` when an implemented provider key is configured.

## Deterministic Real Evidence Pass

Use this when you want a reproducible MCP/backend evidence package without
depending on model behavior:

```powershell
py scripts\run_real_case.py --case-id CASE-RD01-JUDGE --evidence-path evidence\base-rd-01-cdrive.E01 --case-workspace cases\CASE-RD01-JUDGE --json
```

Expected outputs:

- `cases/CASE-RD01-JUDGE/reports/final_analyst_report.md`;
- `cases/CASE-RD01-JUDGE/reports/evidence_book.md`;
- `cases/CASE-RD01-JUDGE/reports/correction_ledger.md`;
- `cases/CASE-RD01-JUDGE/reports/real_run_accuracy_report.md`;
- `cases/CASE-RD01-JUDGE/reports/artifact_index.json`;
- `cases/CASE-RD01-JUDGE/logs/agent_execution.jsonl`.

Verify:

```powershell
py scripts\audit_real_validation.py --case-workspace cases\CASE-RD01-JUDGE --strict
```

For a final submission package check after the public video and Devpost page
exist:

```powershell
py scripts\final_submission_audit.py --demo-video-url VIDEO_URL --devpost-url DEVPOST_URL --strict
```

## Autonomous Agent Smoke

Use this to test the model + MCP stdio loop:

```powershell
py -m src.agent --provider openrouter --case-id CASE-RD01-AUTO-JUDGE --evidence-path evidence\base-rd-01-cdrive.E01 --case-workspace cases\CASE-RD01-AUTO-JUDGE --report-path cases\CASE-RD01-AUTO-JUDGE\reports\final_agent_report.md --max-iterations 5
```

Interpretation:

- a short smoke proves API connectivity and MCP tool routing;
- a short smoke is not a full incident reconstruction;
- if the model stops early or returns a fallback report, use the deterministic
  real evidence pass for the judge-facing evidence package.

## Troubleshooting

| Problem | Meaning | Action |
|---|---|---|
| `python` is not recognized | Windows launcher exists but `python` is not on `PATH` | Use `py` commands. |
| Missing SIFT binaries | Runtime is not SIFT-compatible enough for real run | Install SIFT tools or run in SANS SIFT/WSL with the required commands. |
| Missing API key | Autonomous model runtime cannot start | Configure `OPENROUTER_API_KEY` or another implemented provider key. |
| Provider HTTP 403 | Key/account/model access rejected by provider | Use OpenRouter or replace/retest the provider key. |
| Evidence path missing | Real evidence is not in local ignored `evidence/` | Place the `.E01` under `evidence/` and do not commit it. |
| Workspace rejected | Output path is inside evidence or outside allowed case workspace | Use `cases/<CASE-ID>`. |
| No confirmed compromise finding | Bounded run did not parse enough content-level evidence | Treat compromise status as unknown; do not upgrade to confirmed. |
| Parser failure | Tool output was missing, invalid, partial, or too large | Keep the artifact degraded and route to human review or follow-up parsing. |

## Manual Recovery

If a judge run fails:

1. Stop the run; do not retry blindly.
2. Run `py -m src.agent --check-api`.
3. Run `py scripts\check_env.py --strict`.
4. Run `py scripts\preflight_case.py --case-id CASE --evidence-path PATH --case-workspace cases\CASE --strict`.
5. Inspect the generated case workspace if any files were created.
6. Report the blocker as one of: missing provider, missing SIFT tool, missing
   evidence, invalid workspace, parser failure, provider limit, or unknown.
7. Do not edit or delete the original evidence path.

## Expected Honest Outcome

The current project should produce a defensible first triage package. It should
not be expected to produce a full incident reconstruction until registry,
event, and timeline content parsing are completed.

The final submission audit should only reach 100/100 after the public video URL,
submitted Devpost URL, and public repository synchronization are all real.
