# Evidence And Workspace Policy

Date: 2026-05-06  
Purpose: close the original evidence vs generated workspace separation for Phase 2.

## Local Evidence Folder

Real evidence must be placed under:

```text
M:\Projects\Konkurs\Find Evil!\evidence\
```

This folder is local-only and ignored by git.

## Recommended Evidence File

```text
M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01
```

## Case Workspace Folder

Generated outputs must be written under:

```text
M:\Projects\Konkurs\Find Evil!\cases\<CASE-ID>\
```

Example:

```text
M:\Projects\Konkurs\Find Evil!\cases\SRL-2018-RD01\
```

## Separation Rule

Original evidence:

- input-only;
- never an output target;
- never overwritten;
- never cleaned by project hygiene tasks;
- never committed to public repository.

Case workspace:

- stores generated reports;
- stores evidence book outputs;
- stores correction ledger outputs;
- stores execution logs;
- stores accuracy artifacts for the run;
- can be archived or excluded from public release depending on sensitivity and size.

## Public Packaging Rule

Public repository may include:

- source code;
- documentation;
- synthetic fixture artifacts clearly labelled as synthetic;
- redacted or small example outputs if safe.

Public repository must not include:

- real downloaded evidence images;
- private case workspaces;
- local credentials;
- unredacted sensitive paths;
- large raw forensic exports.

## Readiness Check

Before any real run, verify:

- `evidence/` contains the intended real evidence file;
- `cases/<CASE-ID>/` is separate from the original evidence file;
- output path does not point into `evidence/`;
- `.gitignore` excludes `evidence/` and `cases/`.
