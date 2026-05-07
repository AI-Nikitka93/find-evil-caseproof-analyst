# Codebase Intelligence Safe Workflow

Date: 2026-05-06

Purpose: define the safe setup/status workflow if SocratiCode or an equivalent local codebase intelligence tool is later activated.

## Activation Gate

Do not activate until:

- current README/security model is rechecked;
- package metadata is rechecked;
- Node.js version is compatible;
- Docker daemon is running if the selected tool requires it;
- license implications are accepted;
- indexing location and cleanup rules are understood;
- no secrets or evidence folders are indexed unintentionally.

## Candidate Setup Path

Current README describes MCP config patterns such as:

```text
command: npx
args: ["-y", "socraticode"]
```

For this project, setup must remain local and reversible.

## Status Workflow

If activated later:

1. Confirm Docker is running.
2. Confirm the selected tool version and license.
3. Configure the MCP host without embedding secrets.
4. Exclude local-only folders from indexing:
   - `.env*`
   - `evidence/`
   - `cases/`
   - `fixtures/`
   - `docs/*.local.md`
5. Index the project.
6. Check index status.
7. Verify search returns relevant project files.
8. Record limitations in project notes.

## Limitations

Known limits to record before activation:

- indexing time depends on repo size and local resources;
- Docker images and embedding models may be downloaded;
- Docker on Windows may not expose GPU acceleration;
- external embeddings require safe credential handling and are not enabled by default;
- license and data-handling implications must be reviewed before public/team use.

## Current Decision

Current decision remains:

```text
SKIP activation now because Docker daemon is not reachable and manual search is sufficient for current repo size.
```
