# No-Revert Workspace Discipline

Purpose: protect user work, local evidence, and generated case artifacts from
accidental loss while multiple agents may operate in the same project.

## Core Rule

Do not revert, delete, overwrite, or clean up files that are unrelated to the
current task unless the user explicitly asks for that exact action.

## Protected Areas

Protected areas include:

- `evidence/`
- `cases/`
- `.env.local`
- `docs/*.local.md`
- real run outputs;
- user-edited docs;
- submission artifacts;
- generated reports that may be evidence for readiness.

## Safe Edit Behavior

- Read the current file before editing it.
- Prefer narrow patches over broad rewrites.
- If a file has unrelated changes, work around them and preserve them.
- If a cleanup is needed, first identify the exact files, why they are unused,
  and which verification proves removal is safe.
- Do not run destructive repository reset commands.

## Conflict Behavior

If a task cannot be completed because a file is missing, an evidence image is
absent, a runtime is unavailable, or a user decision is needed, record the
blocker truthfully. Do not create fake evidence, fake run outputs, or fake
completion notes.
