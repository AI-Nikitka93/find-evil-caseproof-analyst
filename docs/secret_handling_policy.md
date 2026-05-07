# Secret Handling Policy

Purpose: prevent API keys, local credentials, private machine paths, and
forensic evidence locations from leaking into reports, logs, screenshots, or
public documentation.

## Protected Data

Protected data includes:

- real API keys and provider tokens;
- local credential files;
- private operator notes;
- local-only evidence files;
- generated case workspaces;
- private execution logs from real evidence;
- screenshots that show keys, private paths, account pages, or local secrets.

## Storage Rules

- Local credentials may live in `.env.local`.
- Shareable examples must use `.env.example`.
- Secret notes must use `.local.md` naming.
- Real evidence belongs under `evidence/`.
- Generated case outputs belong under `cases/`.
- Public docs may name environment variable names, but must not include values.

## Logging Rules

- Readiness checks report `configured: true` or `configured: false`, never the
  secret value.
- Agent reports must not echo provider keys or raw local credential content.
- Execution logs may include provider name and runtime status, but not key
  material.
- Error messages must not include copied environment values.

## Screenshot And Demo Rules

- Hide terminal output that could show environment values.
- Do not record `.env.local`, local credential stores, provider account pages,
  or local-only secret notes.
- If a terminal command prints a secret unexpectedly, discard that capture and
  rotate the affected key before publishing any material.

## Release Gate

Before public release, run the release-control audit and inspect any newly added
docs or media for obvious secret patterns. A release is blocked if a real key,
private evidence path, local credential value, or private case output appears in
public material.
