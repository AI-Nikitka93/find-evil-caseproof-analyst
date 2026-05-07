# Fallback Dataset Plan

Date: 2026-05-06

Purpose: prevent the project from getting stuck if the selected evidence file is unavailable, corrupted, too slow, or unsuitable for the demo.

## Primary Dataset

Primary target:

```text
SRL-2018-Compromised Enterprise Network / base-rd-01-cdrive.E01
```

Reason:

- aligns with the Windows disk triage lane;
- uses `.E01` evidence compatible with the selected SIFT workflow;
- likely supports a compromise narrative suitable for the FIND EVIL demo.

## Fallback Order

| Priority | Candidate | Use if |
|---:|---|---|
| 1 | `base-wkstn-01-c-drive.E01` | Primary image is unavailable or does not produce a clear demo story. |
| 2 | `base-file-cdrive.E01` | Workstation image is weak, and file-server artifacts produce a stronger traceable story. |
| 3 | `base-dc-cdrive.E01` | Other hosts fail, and domain-controller artifacts are needed for a meaningful narrative. |
| 4 | `base-rd-02-cdrive.E01` | First remote-desktop image fails but the same role remains promising. |
| 5 | `dmz-ftp-cdrive.E01` | External-facing host provides better artifacts for compromise explanation. |

## Fallback Trigger Conditions

Switch away from the primary target if:

- file cannot be downloaded or obtained;
- download is incomplete or corrupted;
- SIFT tools cannot read the image;
- partition/filesystem inventory fails;
- timeline generation is empty or unusable;
- registry/event paths produce no meaningful story;
- runtime is too slow for credible demo preparation;
- no natural correction sequence can be demonstrated.

## Fallback Evaluation Procedure

For each fallback candidate:

- record source and filename;
- place it under local ignored evidence storage;
- run the same preflight checklist;
- inventory size, type, and readability;
- test partition and filesystem access first;
- sample timeline or high-value artifact output;
- decide whether it improves demo clarity.

## Documentation Requirements

If a fallback is used, update:

- dataset decision memo;
- dataset documentation;
- evidence inventory;
- chain-of-custody-style note;
- accuracy report;
- README Try-It-Out instructions if the command changes;
- submission readiness audit.

## No-Go Rule

Do not substitute the synthetic fixture as a fallback for final validation.

If no real starter evidence can be validated, the project remains blocked for final hackathon submission.
