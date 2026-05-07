# Demo Video Script

Date: 2026-05-07  
Limit: under 5 minutes  
Format required by FIND EVIL: live terminal screencast with audio narration,
not slides.

## Recording Rule

Record only a terminal and the public-safe docs. Do not show:

- `.env.local`;
- API provider dashboards;
- raw key values;
- private account pages;
- unreviewed local case files containing sensitive paths;
- copyrighted music or third-party media.

## Setup Before Recording

Terminal working directory:

```powershell
cd "M:\Projects\Konkurs\Find Evil!"
```

Recommended environment:

```powershell
$env:MCP_SERVER_COMMAND="py"
$env:FIND_EVIL_AGENT_PROVIDER="auto"
```

Do not type or display API keys during recording. Configure `.env.local`
beforehand.

## Shot List

### 0:00-0:25 Opening

Narration:

> This is CaseProof Analyst, a read-only Custom MCP Server and bounded AI
> triage agent for FIND EVIL. The goal is fast first triage without accepting
> unsupported AI findings.

Show:

```powershell
Get-Content README.md -TotalCount 45
```

### 0:25-0:55 Readiness Checks

Narration:

> Before running, the project checks both the model runtime and the
> SIFT-compatible forensic command surface. The checks report readiness without
> printing secrets.

Commands:

```powershell
py -m src.agent --check-api
py scripts\check_env.py --strict
```

Expected:

- OpenRouter selected as current ready runtime.
- `mmls`, `fls`, `log2timeline.py`, `psort.py`, and `rip.pl` found through WSL.

### 0:55-1:45 Real Evidence Backend Run

Narration:

> This run opens the real RD01 E01 evidence read-only, verifies the hash,
> identifies the volume boundary, inventories high-signal Windows artifacts,
> and writes an evidence package under the case workspace.

Command:

```powershell
py scripts\run_real_case.py --case-id CASE-RD01-DEMO --evidence-path evidence\base-rd-01-cdrive.E01 --case-workspace cases\CASE-RD01-DEMO --json
```

Show:

- `confirmed_findings`;
- `artifact_counts`;
- `evidence_unchanged: true`.

### 1:45-2:30 Self-Correction Moment

Narration:

> The important part is not that the agent says something confident. It
> challenges a tempting compromise claim and drops it because this bounded run
> has parsed bounded SOFTWARE Run-key and SYSTEM service registry content, but
> has not parsed event or timeline content into compromise evidence.

Commands:

```powershell
Get-Content cases\CASE-RD01-DEMO\reports\correction_ledger.md
Get-Content cases\CASE-RD01-DEMO\reports\real_run_accuracy_report.md
```

Point out:

- rejected unsupported claim;
- zero confirmed compromise findings;
- unknown event/timeline content and deeper registry correlation remain visible.

### 2:30-3:20 Evidence Chain

Narration:

> A judge can trace a confirmed finding from the report to an evidence-book
> reference and then to the execution log.

Commands:

```powershell
Get-Content cases\CASE-RD01-DEMO\reports\evidence_book.md
Get-Content cases\CASE-RD01-DEMO\logs\agent_execution.jsonl
```

Show:

- `case_open_readonly`;
- `list_partitions`;
- `filesystem_inventory`;
- `verify_claim`;
- timestamps and parser statuses.

### 3:20-4:10 Architecture Boundary

Narration:

> Evidence safety is enforced by architecture. The model does not get a generic
> shell tool. The MCP server exposes fixed forensic actions, writes outputs
> under the case workspace, and keeps the original evidence input-only.

Command:

```powershell
Get-Content docs\architecture.md -TotalCount 90
```

### 4:10-4:45 Close

Narration:

> The current release is a defensible first triage slice: real evidence access,
> evidence-linked findings, visible self-correction, and structured logs. It
> does not claim full incident reconstruction. The next step is content-level
> event, timeline, and deeper registry analysis.

Show:

```powershell
Get-Content docs\final_quality_gate_matrix.md -TotalCount 60
```

## Public Video Checklist

- Audio narration is clear.
- Video is under 5 minutes.
- No key, token, credential file, account page, or private evidence download
  page is visible.
- Video shows live terminal execution.
- Video shows real evidence run or replayed real output from a just-created
  workspace.
- Video shows a self-correction or rejected unsupported claim.
- Video URL is public or unlisted-but-accessible according to Devpost form
  requirements.
