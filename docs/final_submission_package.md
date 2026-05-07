# Final Submission Package

Date: 2026-05-07  
Use: paste-ready Devpost text plus required component mapping.

## Live Rule Snapshot

Live Devpost facts checked on 2026-05-07:

- Deadline: June 15, 2026 at 11:45 PM EDT.
- Required public repository: GitHub, public, MIT or Apache 2.0 license.
- Required local run support: setup instructions or live deployment.
- Required video: less than 5 minutes, live terminal screencast, audio
  narration, real evidence, at least one self-correction sequence, publicly
  visible on YouTube, Vimeo, or Youku.
- Required written materials: English or English translation.
- Required artifacts: architecture diagram, dataset documentation, accuracy
  report, and agent execution logs.

Sources:

- `https://findevil.devpost.com/`
- `https://findevil.devpost.com/rules`

## Project Name

CaseProof Analyst

## Tagline

Fast first triage for SIFT evidence without accepting unsupported AI findings.

## Short Description

CaseProof Analyst is a read-only Custom MCP Server and bounded AI agent for
FIND EVIL. It triages a Windows disk image through typed SIFT-compatible tools,
checks candidate findings against evidence, drops unsupported claims, and emits
an analyst report, evidence book, correction ledger, accuracy report, and
execution log.

## What It Does

CaseProof Analyst gives an incident responder a defensible first pass over disk
evidence. The agent cannot run arbitrary shell commands through the MCP server.
Instead, it can call a small set of typed forensic tools:

- open evidence read-only;
- inspect volume or partition boundaries;
- inventory filesystem paths;
- build timeline outputs when the runtime supports it;
- extract registry and event evidence through bounded wrappers;
- verify claims;
- write execution logs.

The current real CASE-RD01 pass proves evidence integrity, NTFS volume access,
high-signal Windows artifact discovery, bounded registry Run-key/service
content parsing, bounded EVTX event-content parsing, bounded registry/event
correlation, replay consistency, and self-correction for an unsupported
compromise claim. It does not claim full incident reconstruction.

## How It Was Built

The project is built in Python with the official `mcp` package and FastMCP. The
server exposes eight public MCP tools with Pydantic schemas. The agent starts
the server over stdio, uses hard iteration and timeout budgets, and routes model
tool calls through the MCP boundary.

The important design choice is that evidence safety is architectural. The model
does not receive generic shell access. Generated reports, logs, and exports are
written under a separate case workspace, while the original evidence path stays
input-only.

## What Makes It Different

Most AI triage demos look good when the final report sounds confident. This
project is optimized for the harder question: can a reviewer trace the claim
back to evidence?

Every confirmed finding must have an evidence reference. Unsupported claims are
dropped, downgraded, corrected, or routed to human review. Parser failures and
unknowns remain visible. The demo story is not "AI found everything"; it is "AI
moved quickly, then stopped itself from making a claim it could not prove."

## Real Validation

The project was tested against the FIND EVIL starter evidence file
`base-rd-01-cdrive.E01` from the SRL-2018 compromised enterprise dataset. The
real bounded pass produced:

- final analyst report;
- evidence book;
- correction ledger;
- real-run accuracy report;
- execution log review;
- public-safe real execution-log excerpt;
- bounded registry/event correlation summary;
- judge summary;
- artifact index;
- JSONL execution log.

Confirmed findings are limited to evidence integrity, volume accessibility,
artifact-family availability, bounded registry Run-key/service content, and
bounded EVTX event records, plus a bounded correlation finding that explicitly
keeps compromise unconfirmed. No malicious finding is claimed.

## Challenges

The main challenge was keeping the project honest. The evidence is large, local
runtime behavior varies, and some tools produce text rather than clean JSON. The
project therefore treats parser failures, missing tools, missing model keys, and
unsupported claims as first-class states instead of hiding them.

Another challenge was model runtime availability. OpenRouter is currently the
selected free/low-cost demo path in `auto` mode. Groq is implemented and now
passes API readiness in this workspace, while Anthropic remains supported when a
valid key is available.

## What I Learned

For DFIR, the trust boundary matters as much as the final prose. A useful AI
responder has to preserve evidence, show its work, and know when to say
"unknown." A narrow evidence-backed triage slice is more useful than a broad
demo that silently upgrades assumptions into findings.

## What Is Next

Next work is deeper content-level analysis:

- expand registry parsing beyond SOFTWARE Run keys and SYSTEM services;
- generate and summarize a bounded Plaso timeline;
- correlate full timeline, process, account, and persistence evidence;
- run a longer autonomous model loop when provider limits allow it;
- compare against official ground truth if it becomes available.

## Required Component Mapping

| Required component | Final submission value |
|---|---|
| Public code repository | https://github.com/AI-Nikitka93/find-evil-caseproof-analyst |
| License | MIT, `LICENSE` |
| README setup | `README.md` |
| Local run instructions | README plus `docs/judge_try_it_out.md` |
| Demo video | YouTube/Vimeo/Youku URL after recording; pre-recording rehearsal via `py scripts\demo_rehearsal.py --strict` |
| Architecture diagram | `docs/architecture.md` |
| Dataset documentation | `docs/dataset_documentation.md` |
| Accuracy report | `docs/accuracy_report.md` |
| Judge criteria proof | `docs/judge_max_readiness_report.md` shows all six judging criteria at local 17/17 proof level, while still separating the public video and Devpost URL gates. |
| Final GO decision | `docs/final_go_decision_2026-05-07.md` states LOCAL GO and the remaining external gates. |
| Agent execution logs | `docs/public_real_execution_log_sample.jsonl`, `docs/public_real_traceability_packet.md`, plus local full run log under `cases/CASE-RD01/` |
| Text description | This document |

## Final Paste Checklist

- Use the verified GitHub repository URL: `https://github.com/AI-Nikitka93/find-evil-caseproof-analyst`.
- Replace `DEMO_VIDEO_URL` with the public video URL.
- Confirm the repository does not include `evidence/`, `cases/`, `.env.local`,
  or local-only notes.
- Confirm all submitted text is English.
- Regenerate the local judge scorecard with `py scripts\audit_judge_readiness.py --write-doc --strict`; it must show all six criteria at `17/17`.
- Run `py scripts\demo_rehearsal.py --strict` before recording and use its
  command sequence for the live terminal screencast.
- Confirm `py scripts\final_submission_audit.py --json` reports
  `local_package: GO` before recording; if it reports local `NO-GO`, fix that
  local gate before touching Devpost.
- Confirm the video shows the same behavior described here.
- Run the final 100-point gate after the video and Devpost page exist:

```powershell
py scripts\final_submission_audit.py --demo-video-url VIDEO_URL --devpost-url DEVPOST_URL --strict
```

Expected final state: `ready (100/100)`.
