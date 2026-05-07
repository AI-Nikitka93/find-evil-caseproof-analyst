# AI Skill Stack Discovery Evaluation

Date: 2026-05-06

Tool evaluated: autoskills / `midudev/autoskills`

## Current Source Check

Checked sources:

- `https://github.com/midudev/autoskills`
- package metadata via `npm view autoskills version license engines --json`
- local dry-run via `npx autoskills --dry-run`

Current observed package metadata:

```json
{
  "version": "0.3.6",
  "license": "CC-BY-NC-4.0",
  "engines": {
    "node": ">=22.6.0"
  }
}
```

Current local prerequisites:

```text
node: v24.14.1
npm: 11.11.0
```

## README Security Model Summary

The current README says autoskills:

- scans project files to detect technologies;
- selects curated skills from an audited registry;
- verifies downloaded skill files against a manifest with hashes;
- supports `--dry-run`;
- writes a `skills-lock.json` entry when skills are installed;
- requires Node.js >= 22.

## Local Dry-Run Result

Command:

```text
npx autoskills --dry-run
```

Observed technologies:

```text
Python
Pydantic
```

Observed suggested skills:

```text
inferen-sh/python-executor
wshobson/python-testing-patterns
bobmatnyc/pydantic
```

Observed install behavior:

```text
--dry-run: nothing was installed.
```

## Current Decision

Decision: do not install automatically in this batch.

Reason:

- dry-run worked and detected the stack;
- suggested skills may be useful, but one suggestion showed a security-check warning;
- the project already has local instructions and task-specific docs;
- installing skills changes the agent workflow surface and should be deliberate;
- no real SIFT/evidence blocker is solved by installing skills.

## Safe Next Step

If skill installation is approved later:

- install only selected skills;
- review generated/installed files before use;
- keep any lock/manifest file if created;
- do not print or store secrets in skill config;
- rerun release-control audit after installation.

## Acceptance

This evaluation is complete because it checked the current README/security model, local package metadata, local runtime compatibility, and an actual safe dry-run without installing anything.
