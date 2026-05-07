# Dataset Decision Memo

Date: 2026-05-06  
Decision status: Selected candidate; local file still required before real validation.

## Selected Candidate

Recommended real evidence candidate:

```text
SRL-2018-Compromised Enterprise Network / base-rd-01-cdrive.E01
```

Expected local placement:

```text
M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01
```

## Why This Candidate Fits

`base-rd-01-cdrive.E01` is the strongest current candidate because:

- it is a Windows disk-image style evidence file;
- it matches the project’s chosen Windows disk triage lane;
- `.E01` evidence aligns with the SIFT / disk-triage workflow already researched;
- it can support partition, filesystem, timeline, registry, event, claim verification, and evidence-book outputs;
- prior project research identified it inside the SRL-2018 compromised enterprise scenario;
- the `rd` host naming suggests a role that may be useful for a meaningful compromise narrative, subject to real validation.

## Alternatives

| Candidate | Decision | Reason |
|---|---|---|
| `base-wkstn-01-c-drive.E01` | fallback | Also likely fits Windows workstation triage, but not currently the recommended first target. |
| `base-file-cdrive.E01` | fallback | Potentially useful if file-server artifacts produce a stronger story. |
| `base-dc-cdrive.E01` | defer | Domain controller evidence may be valuable but can expand scope and review complexity. |
| `Rocba-Memory.zip` | reject for first lane | Memory-oriented evidence does not match the current disk-triage first release. |

## Decision Boundary

The selected candidate does not complete real validation by itself.

The decision becomes final only after:

- the file exists locally;
- the file can be read in a SIFT-compatible environment;
- initial inventory confirms useful artifacts;
- the demo story can be supported by evidence rather than expectation.

## Current Blocker

The file is not present locally yet.

Current local scan found only:

```text
fixtures/smoke.raw
```

That file is not suitable for real validation.
