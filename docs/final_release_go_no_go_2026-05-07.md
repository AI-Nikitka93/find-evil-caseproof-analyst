# Final Release Go/No-Go Board

Date: 2026-05-07  
Current decision: **NO-GO for Devpost submission until video and Devpost
steps are complete; GO for public repository package.**

## Current Go Items

| Item | Status | Evidence |
|---|---:|---|
| Code exists locally | GO | `src/`, `scripts/`, `tests/` |
| MIT license exists | GO | `LICENSE` |
| README setup exists | GO | `README.md` |
| Architecture diagram exists | GO | `docs/architecture.md` |
| Dataset documentation exists | GO | `docs/dataset_documentation.md` |
| Accuracy report exists | GO | `docs/accuracy_report.md` |
| Real bounded CASE-RD01 pass exists | GO | `cases/CASE-RD01/` local package |
| Bounded registry content proof exists | GO | `cases/CASE-RD01/exports/registry_content_summary.json` |
| Bounded event content proof exists | GO | `cases/CASE-RD01/exports/event_content_summary.json` |
| Bounded correlation proof exists | GO | `cases/CASE-RD01/exports/correlation_summary.json` |
| Execution log exists locally | GO | `cases/CASE-RD01/logs/agent_execution.jsonl` |
| Traceability walkthrough exists | GO | `docs/reviewer_traceability_walkthrough.md` |
| Devpost text draft exists | GO | `docs/final_submission_package.md` |
| Demo script exists | GO | `docs/demo_video_script.md` |
| Demo rehearsal gate exists | GO | `scripts/demo_rehearsal.py --strict` verifies required demo story assets before recording |
| Judge runbook exists | GO | `docs/judge_try_it_out.md` |
| Judging readiness map exists | GO | `docs/judging_17_readiness.md` |
| Judge max readiness report exists | GO | `docs/judge_max_readiness_report.md` shows all six criteria at local 17/17 proof level |
| Public GitHub URL | GO | https://github.com/AI-Nikitka93/find-evil-caseproof-analyst |
| Final submission audit exists | GO | `scripts/final_submission_audit.py --json` |

## Current No-Go Items

| Item | Status | Required action |
|---|---:|---|
| Demo video URL | NO-GO | Record under-5-minute terminal demo with audio and upload publicly. |
| Devpost form | NO-GO | Paste final English text, public repo URL, and video URL into Devpost. |
| Final video/Devpost link audit | NO-GO | Check public video and final Devpost links from a non-private session. |

Use this command before recording the video:

```powershell
py scripts\demo_rehearsal.py --strict
```

Use this command as the final mechanical gate after the video and Devpost page
exist:

```powershell
py scripts\audit_judge_readiness.py --write-doc --strict
py scripts\final_submission_audit.py --demo-video-url VIDEO_URL --devpost-url DEVPOST_URL --strict
```

The command must reach `ready (100/100)` before final submission is treated as
complete.

## Accepted Limitations

These limitations are acceptable if stated honestly:

- first release is a narrow Windows disk triage lane;
- current real run confirms evidence integrity, volume access, artifact-family
  availability, bounded SOFTWARE Run-key/SYSTEM service parsing, bounded
  registry/event correlation, and correction behavior;
- no confirmed malicious finding is claimed;
- bounded event content and bounded registry/event correlation are parsed,
  while full Plaso timeline and deeper process/account corroboration remain
  future work;
- WSL runtime is SIFT-compatible for tested tools but not the official SANS
  SIFT OVA;
- OpenRouter is the current selected free/low-cost demo runtime path;
- Groq is implemented and currently passes API readiness, but should only be
  named in the final video if the recorded run uses it successfully.

## Not Accepted

The submission must not claim:

- full incident reconstruction;
- full SIFT coverage;
- real APT accuracy beyond the bounded CASE-RD01 pass;
- a specific provider is used in the demo unless the recorded run proves it;
- demo video completion before the video is uploaded and visible;

## Legal And License Review

| Surface | Status | Notes |
|---|---:|---|
| Project license | OK | MIT license at root. |
| Third-party code | OK with dependency licenses | Uses Python packages from `requirements.txt`; no vendored third-party assets. |
| Evidence file | LOCAL ONLY | Do not publish `evidence/`. |
| Case outputs | LOCAL BY DEFAULT | Do not publish raw `cases/` without separate public-safe review. |
| Demo media | PENDING | Use terminal screencast only; no copyrighted music or third-party marks beyond necessary tool names. |
| Submission language | OK | Prepared public submission text is English. |

## Freshness Review

Live facts refreshed on 2026-05-07:

- Devpost deadline: Jun 15, 2026 at 11:45 PM EDT.
- Required video: less than 5 minutes, live terminal screencast, audio
  narration, real evidence, self-correction sequence, public video host.
- Required repository: public GitHub, open-source MIT or Apache 2.0 license,
  README setup instructions.
- Required artifacts: architecture diagram, dataset docs, accuracy report,
  execution logs, testing instructions.

Refresh again immediately before final submission because Devpost rules can
change.

## Final Submission Decision

Do not press Submit until all three conditions are true:

1. Demo video URL verified.
2. Devpost text copied from `docs/final_submission_package.md` and checked.
3. `py scripts\final_submission_audit.py --demo-video-url VIDEO_URL --devpost-url DEVPOST_URL --strict`
   returns ready.
4. Final local verification commands pass.
