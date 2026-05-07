# Evidence-Locked Self-Correcting Disk Triage MCP

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An autonomous DFIR triage agent for the FIND EVIL! hackathon. It analyzes a
Windows disk image through a local Custom MCP Server that exposes typed,
read-only SIFT wrappers instead of broad shell access.

## Promise

Public promise: **fast first triage without accepting unsupported AI
findings.** This is forensic clarity, evidence-first reading, and no decorative
dashboard framing.

The core goal is not broad DFIR coverage. The goal is a narrow, auditable path:
open evidence read-only, extract disk artifacts, verify each finding against
evidence records, drop unsupported claims, and preserve an execution trail.

> [!IMPORTANT]
> `docs/accuracy_report.md` now includes a real bounded CASE-RD01 evidence pass.
> It proves read-only access, SIFT-compatible tool execution, filesystem
> inventory, correction-ledger behavior, and replay consistency. It does not
> claim full incident reconstruction or autonomous AI completion.

## Quick Status

| Area | Status | What to inspect |
|---|---:|---|
| Code and tests | Ready locally | `src/`, `tests/`, `scripts/` |
| Real evidence file | Present locally | `evidence/base-rd-01-cdrive.E01` is local-only and ignored |
| Implemented model runtime | Ready locally | `python -m src.agent --check-api` selects OpenRouter/Groq/Anthropic without printing secrets |
| SIFT-compatible runtime | Available through WSL | `py scripts\check_env.py --strict` |
| Public GitHub repository | Published | https://github.com/AI-Nikitka93/find-evil-caseproof-analyst |
| Final local package | Prepared with external gates | Devpost text, demo script, judge runbook, quality matrix, and go/no-go board are in `docs/` |
| Final Devpost submission | External gates remain | public demo video URL and Devpost form submission still remain |

## Real Validation Status

The selected real evidence image is present locally and has a bounded real run
under `cases/CASE-RD01/`. The current successful path includes deterministic MCP
backend execution through WSL forensic tools, `icat` extraction of registry
hives, RegRipper parsing of SOFTWARE Run keys and SYSTEM services, and a short
OpenRouter autonomous agent smoke run against the real evidence. Full incident
reconstruction is still not claimed.

Empty and degraded states are explicit:

- No evidence file: stop before claiming validation.
- Missing SIFT runtime: show missing commands and do not imply real run success.
- Missing AI runtime key: stop autonomous mode and configure one implemented
  provider key (`OPENROUTER_API_KEY`, `GROQ_API_KEY`, or `ANTHROPIC_API_KEY`).
- No confirmed finding: report the inspected scope and keep findings empty.
- Partial parser output: mark the artifact as degraded.
- Unsupported claim: drop, downgrade, or route to Human Review.
- Blocked unsafe action: name the unavailable capability and preserve evidence
  as input-only.

## What It Does

- Starts a local MCP server with read-only wrappers for `mmls`, `fls`,
  `icat`, `log2timeline.py`, `psort.py`, and `rip.pl`.
- Runs a bounded AI execution loop over MCP stdio with implemented Anthropic,
  OpenRouter, and Groq provider paths.
- Requires `verify_claim` before final findings are reported as confirmed.
- Writes append-only execution logs for tool calls, parser failures, verifier
  results, and self-correction.
- Blocks spoliation by architecture: destructive tools are not exposed.

## Product Direction

The first full release is not a broad SIFT wrapper suite. It is a focused
CaseProof Analyst release: real SIFT-compatible evidence, visible
self-correction, traceable findings, an analyst report, an evidence book, a
correction ledger, an accuracy report, and replayable execution logs.

## Hackathon Requirements Checklist

| Required component | Status | Location |
|---|---:|---|
| Code Repo | Published | https://github.com/AI-Nikitka93/find-evil-caseproof-analyst plus [`src/server.py`](src/server.py), [`src/agent.py`](src/agent.py), [`tests/`](tests/), [`docs/public_release_manifest.md`](docs/public_release_manifest.md) |
| Demo Video | Script ready; recording/upload external | [`docs/demo_video_script.md`](docs/demo_video_script.md) |
| Architecture Diagram | Present | [`docs/architecture.md`](docs/architecture.md) |
| Project Description | Ready to paste | [`docs/final_submission_package.md`](docs/final_submission_package.md) |
| Dataset Documentation | Present with limits | [`docs/dataset_documentation.md`](docs/dataset_documentation.md) documents the real bounded CASE-RD01 pass and synthetic fixture status. |
| Accuracy Report | Present | [`docs/accuracy_report.md`](docs/accuracy_report.md) |
| Try-It-Out Instructions | Present | [Try-It-Out Instructions](#try-it-out-instructions), [`docs/judge_try_it_out.md`](docs/judge_try_it_out.md) |
| Agent Execution Logs | Present locally and as public-safe real excerpt | [`docs/public_real_execution_log_sample.jsonl`](docs/public_real_execution_log_sample.jsonl), [`docs/public_real_traceability_packet.md`](docs/public_real_traceability_packet.md), [`docs/reviewer_traceability_walkthrough.md`](docs/reviewer_traceability_walkthrough.md) |

Final submission control docs:

- [`docs/final_submission_package.md`](docs/final_submission_package.md):
  Devpost-ready English description and component mapping.
- [`docs/demo_video_script.md`](docs/demo_video_script.md): under-5-minute
  live terminal demo script with self-correction moment.
- [`docs/judge_try_it_out.md`](docs/judge_try_it_out.md): setup, run,
  troubleshooting, and recovery instructions.
- [`docs/final_quality_gate_matrix.md`](docs/final_quality_gate_matrix.md):
  judging-criteria gate matrix.
- [`docs/final_release_go_no_go_2026-05-07.md`](docs/final_release_go_no_go_2026-05-07.md):
  final go/no-go board.

## Architecture & Security Boundaries

The selected architecture is a Custom MCP Server with a single-agent client.
This is intentional: evidence protection lives at the tool boundary, not only in
the prompt.

Constraint Implementation:

- The model cannot call arbitrary shell commands.
- The MCP server exposes only fixed forensic tool contracts.
- Original evidence is registered as read-only input.
- Outputs and logs are constrained to a case workspace.
- Unsupported claims are blocked or downgraded by `verify_claim`.
- Destructive requests such as `rm` or overwrite are not valid MCP tools.

See [`docs/architecture.md`](docs/architecture.md) for the Mermaid diagram and
runtime flow.

## Try-It-Out Instructions

### 1. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Configure the implemented model runtime

For a free/low-cost local setup, prefer OpenRouter first. Groq is also supported
as an implemented OpenAI-compatible runtime, but the local Groq key may be
account-blocked or rate-limited even when its syntax is valid. Anthropic remains
supported if you have a valid key.

```bash
export FIND_EVIL_AGENT_PROVIDER="auto"
export OPENROUTER_API_KEY="your-key"
```

PowerShell:

```powershell
$env:FIND_EVIL_AGENT_PROVIDER="auto"
$env:OPENROUTER_API_KEY="your-key"
```

Check model/API readiness without printing secrets:

```bash
python -m src.agent --check-api
```

This command prints provider readiness and runtime status without printing key
values.

### 3. Check SIFT tools

Use this before a real evidence run. The real DFIR path requires `mmls`,
`fls`, `icat`, `log2timeline.py`, `psort.py`, and `rip.pl` in `PATH`.

```bash
python scripts/check_env.py --strict
```

PowerShell fallback:

```powershell
py scripts\check_env.py --strict
```

### 4. Run the autonomous agent

Use this on a SIFT-compatible machine with the required DFIR tools in `PATH`.

```bash
python -m src.agent --provider openrouter --case-id CASE-001 --evidence-path /path/to/disk.E01 --case-workspace cases/CASE-001 --report-path report.md
```

Windows PowerShell fallback when `python` is not on `PATH`:

```powershell
$env:MCP_SERVER_COMMAND="py"
py -m src.agent --provider openrouter --case-id CASE-001 --evidence-path "C:\path\to\disk.E01" --case-workspace "cases\CASE-001" --report-path report.md
```

The agent starts the local MCP server with:

```bash
python -m src.server
```

It then follows the bounded loop in `src/agent.py`:

1. open case;
2. list partitions;
3. inventory filesystem and build timeline;
4. extract registry and event evidence;
5. verify claims;
6. write `report.md`.

### 5. Generate the synthetic eval log

If you do not have a SIFT image locally, generate the synthetic execution log
used by the current Accuracy Report:

```bash
python tests/mock_eval_fixture.py
```

This writes:

```text
agent_execution_log.jsonl
```

### 6. Run local checks

```bash
python -m pytest tests
python -m py_compile src/agent.py src/prompts.py src/server.py
```

## Repository Structure

```text
.
├── README.md
├── LICENSE
├── agent_execution_log.jsonl
├── requirements.txt
├── src/
│   ├── agent.py
│   ├── prompts.py
│   └── server.py
├── tests/
│   ├── mock_eval_fixture.py
│   ├── test_agent_contracts.py
│   └── test_server_contracts.py
└── docs/
    ├── accuracy_report.md
    ├── architecture.md
    ├── hackathon_strategy.md
    ├── mcp_architecture.md
    └── research_sift_mcp.md
```

## Key Artifacts

- [`DESIGN.md`](DESIGN.md): evidence-first visual contract for docs and
  generated review surfaces.
- [`docs/hackathon_strategy.md`](docs/hackathon_strategy.md): strategy and
  judging-criteria mapping.
- [`docs/mcp_architecture.md`](docs/mcp_architecture.md): MCP contract design.
- [`docs/architecture.md`](docs/architecture.md): public architecture diagram.
- [`docs/accuracy_report.md`](docs/accuracy_report.md): real bounded CASE-RD01
  accuracy report and remaining limitations.
- [`docs/dataset_documentation.md`](docs/dataset_documentation.md): dataset
  status, real bounded run scope, synthetic fixture status, and next dataset work.
- [`docs/submission_readiness_audit.md`](docs/submission_readiness_audit.md):
  local readiness audit against the FIND EVIL! requirements.
- [`docs/reviewer_traceability_walkthrough.md`](docs/reviewer_traceability_walkthrough.md):
  judge path from finding to evidence reference to execution log.
- [`docs/final_submission_package.md`](docs/final_submission_package.md):
  Devpost-ready project description and required component map.
- [`docs/public_release_manifest.md`](docs/public_release_manifest.md):
  include/exclude policy for the public GitHub repository.
- [`docs/public_real_traceability_packet.md`](docs/public_real_traceability_packet.md):
  public-safe real CASE-RD01 step trace and self-correction pointer.
- [`docs/public_real_execution_log_sample.jsonl`](docs/public_real_execution_log_sample.jsonl):
  redacted real execution-log excerpt generated from `cases/CASE-RD01`.
- [`agent_execution_log.jsonl`](agent_execution_log.jsonl): synthetic
  judge-facing execution log sample.

## Current Limitations

- Full incident reconstruction remains open.
- The local Groq key is syntactically present but returned HTTP 403 during live
  smoke testing; OpenRouter is the current working free/low-cost runtime path.
- Event-log content, full timeline, and deeper registry correlation remain
  open; bounded SOFTWARE Run-key and SYSTEM service parsing is present.
- Demo video upload and Devpost submission remain external gates. Draft text
  and recording script are now included in `docs/`.

## Contribution Path

Contributions should strengthen evidence validation, traceability,
self-correction, safe execution, reproducibility, or public submission
readiness. Visual work must follow `DESIGN.md` and must not hide real validation
gaps.

## License

MIT. See [`LICENSE`](LICENSE).
