# Public Release Manifest

Date: 2026-05-07  
Purpose: define what belongs in the public GitHub repository and what must stay
local-only.

## Include In Public Repository

| Path | Reason |
|---|---|
| `README.md` | Main judge-facing landing page and setup instructions. |
| `LICENSE` | MIT license, visible at repository root. |
| `.env.example` | Safe environment template without secret values. |
| `requirements.txt` | Python dependency list. |
| `src/` | MCP server, agent, claim/reporting/output logic. |
| `scripts/` | Readiness, real-run, output, and audit CLIs. |
| `tests/` | Contract and behavior tests. |
| `docs/architecture.md` | Architecture diagram and trust boundary. |
| `docs/dataset_documentation.md` | Dataset source, real bounded run scope, limits. |
| `docs/accuracy_report.md` | Real bounded accuracy report plus synthetic fixture separation. |
| `docs/submission_readiness_audit.md` | Current readiness truth. |
| `docs/reviewer_traceability_walkthrough.md` | Judge traceability path. |
| `docs/final_quality_gate_matrix.md` | Criteria-level gate matrix. |
| `docs/final_submission_package.md` | Devpost-ready text and required component mapping. |
| `docs/demo_video_script.md` | Demo recording script. |
| `docs/judge_try_it_out.md` | Setup, run, troubleshooting, recovery. |
| `docs/final_release_go_no_go_2026-05-07.md` | Final release decision board. |
| `docs/public_real_execution_log_sample.jsonl` | Public-safe real CASE-RD01 execution-log excerpt. |
| `docs/public_real_traceability_packet.md` | Public-safe walkthrough for the real log excerpt and self-correction signal. |
| `agent_execution_log.jsonl` | Historical synthetic fixture only, clearly labeled in docs. |

## Exclude From Public Repository

| Path | Reason |
|---|---|
| `.env` / `.env.local` / `.env.*` except `.env.example` | Contains local credentials or runtime config. |
| `evidence/` | Contains large local evidence files. |
| `cases/` | Contains local generated evidence-derived outputs. |
| `docs/*.local.md` | Local-only notes and secret index. |
| `docs/superpowers/` | Local implementation plans and agent working notes. |
| `__pycache__/`, `.pytest_cache/`, `scripts/__pycache__/` | Generated caches. |
| `.playwright-mcp/` | Local browser automation state. |
| `УСЛОВИЯ.txt` | Local copied contest notes; public package cites cleaned project docs instead. |
| raw demo recordings before review | May show private paths or terminal state. |

## Public Artifact Substitution

Because `cases/` is intentionally ignored, the public repository should point
judges to:

- `docs/dataset_documentation.md` for evidence identity, run scope, and counts;
- `docs/accuracy_report.md` for real bounded findings and unknowns;
- `docs/reviewer_traceability_walkthrough.md` for the local trace path;
- `docs/public_real_execution_log_sample.jsonl` for a real public-safe tool
  execution excerpt;
- `docs/public_real_traceability_packet.md` for the corresponding step table
  and self-correction pointer;
- `docs/final_submission_package.md` for the exact submission story.

If raw `cases/CASE-RD01` outputs are later published, they must be reviewed
separately for:

- no API keys or tokens;
- no private account data;
- no unnecessary local machine paths;
- no original evidence bytes;
- no large binary exports;
- no claims beyond the bounded run.

## Local Readiness Checks

Run before publishing:

```powershell
py -m pytest
py scripts\check_env.py --strict
py scripts\audit_release_controls.py
py scripts\audit_design_quality.py
py scripts\audit_visual_package.py
py scripts\audit_real_validation.py --case-workspace cases\CASE-RD01 --strict
py scripts\generate_public_trace_packet.py --strict
```

Run a public-noise scan:

```powershell
rg -n "TODO|PLACEHOLDER|INSERT|your-key|sk-|gsk_|OPENROUTER_API_KEY=|GROQ_API_KEY=|ANTHROPIC_API_KEY=" README.md docs src scripts tests .env.example requirements.txt LICENSE
```

`your-key` is allowed only in setup examples if it is clearly a placeholder.

## Current Publication Status

Public repository verified on 2026-05-07:

- `https://github.com/AI-Nikitka93/find-evil-caseproof-analyst`
- Visibility: public
- License: MIT
- Default branch: `main`

Before final Devpost submission, verify from a clean browser session that:

- the repository is public;
- the license is visible;
- README renders correctly;
- Mermaid diagrams render;
- all links resolve;
- ignored local files are absent.
