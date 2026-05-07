# Final GO Decision

Date: 2026-05-07

Decision: **LOCAL PACKAGE GO / FINAL DEVPOST SUBMISSION NO-GO UNTIL VIDEO AND DEVPOST URL EXIST**

This file is the explicit release decision for the FIND EVIL submission package.
It separates the local engineering package from the external submission gates so
the project can be advanced without overstating readiness.

## Current Decision

| Surface | Decision | Evidence |
|---|---:|---|
| Local code package | GO | `py -m pytest` passes 102 tests; `src/`, `scripts/`, `tests/`, README, MIT license, and required docs exist. |
| Local SIFT-compatible runtime | GO | `py scripts\check_env.py --strict` finds `mmls`, `fls`, `icat`, `log2timeline.py`, `psort.py`, and `rip.pl` through WSL. |
| Implemented model runtime | GO | `py -m src.agent --check-api` selects OpenRouter and also validates Groq as implemented. |
| Real bounded evidence package | GO | `cases/CASE-RD01/` contains final report, evidence book, correction ledger, real-run accuracy report, registry/event/correlation exports, and execution log. |
| Public-safe trace package | GO | `docs/public_real_execution_log_sample.jsonl` and `docs/public_real_traceability_packet.md` preserve evidence opening, artifact depth, verification, and self-correction. |
| Demo rehearsal assets | GO | `py scripts\demo_rehearsal.py --json --strict` reports `ready`. |
| Public GitHub repository | GO | `https://github.com/AI-Nikitka93/find-evil-caseproof-analyst` is the configured public repository and `origin/main` is synced locally. |
| Demo video URL | NO-GO | No public YouTube, Vimeo, or Youku URL has been supplied yet. |
| Submitted Devpost URL | NO-GO | No submitted Devpost project URL has been supplied yet. |
| Final contest submission | NO-GO | The final submission gate intentionally blocks until both external URLs exist. |

## What GO Means Here

`LOCAL PACKAGE GO` means the repository is ready to record the public demo and
paste the Devpost story. It does not mean the contest entry has already been
submitted.

`FINAL SUBMISSION GO` requires all of the following:

1. Public demo video URL on YouTube, Vimeo, or Youku.
2. Submitted Devpost project URL.
3. `py scripts\final_submission_audit.py --demo-video-url VIDEO_URL --devpost-url DEVPOST_URL --strict` returns `ready (100/100)`.

## Required Video Proof

The video must be under five minutes and show live terminal execution with audio
narration. It must show:

1. API/runtime readiness check.
2. SIFT-compatible tool readiness check.
3. Real CASE-RD01 bounded run or pre-recording rehearsal command sequence.
4. Public trace packet with evidence opening, registry/event depth, and claim
   verification.
5. The self-correction moment: unsupported compromise claim is dropped from
   confirmed findings.
6. Final statement that no malicious finding is claimed from this bounded pass.

Do not make a marketing-only video. Do not use slides as the primary proof.

## Final Mechanical Gate

Run this after the public video and Devpost page exist:

```powershell
py scripts\audit_judge_readiness.py --write-doc --strict
py scripts\demo_rehearsal.py --strict
py scripts\final_submission_audit.py --demo-video-url VIDEO_URL --devpost-url DEVPOST_URL --strict
```

Expected final result:

```text
Final submission status: ready (100/100)
local_package: GO
external_submission: GO
final_submission: GO
```

## Non-Negotiable Wording Boundary

Allowed:

- real bounded CASE-RD01 evidence pass;
- read-only Custom MCP Server;
- SIFT-compatible Windows disk triage;
- bounded registry Run-key/service parsing;
- bounded EVTX parsing and registry/event correlation;
- unsupported compromise claim dropped;
- no confirmed malicious finding in this bounded pass.

Not allowed:

- full incident reconstruction;
- full SIFT coverage;
- confirmed APT compromise;
- real SIFT accuracy beyond the bounded CASE-RD01 pass;
- final Devpost submission readiness before video and Devpost URLs exist.

