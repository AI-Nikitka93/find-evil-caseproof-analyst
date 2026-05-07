# Reviewer-Derived Manifest: CASE-RD01

Date: 2026-05-06

Status: real bounded evidence pass completed with bounded registry content; full incident reconstruction still open.

## Manifest Identity

| Field | Value |
|---|---|
| Case ID | `CASE-RD01` |
| Evidence filename | `base-rd-01-cdrive.E01` |
| Evidence source | FIND EVIL starter case data / SRL-2018-Compromised Enterprise Network |
| Official answer key status | Not available in the local project materials. |
| Manifest type | Reviewer-derived manifest, not official ground truth. |
| Current blocker | Event-log content, full timeline, and deeper registry correlation remain open; full long-run autonomous investigation is not yet claimed. |

## Required Limitation Statement

This manifest is reviewer-derived and is not an official answer key. It exists to support transparent accuracy evaluation when official ground truth is unavailable. Findings must still be verified against case evidence before being reported as confirmed.

## Current Evidence Facts

| Fact | Current value |
|---|---|
| Local evidence path | `M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01` |
| Local file presence | Present as of 2026-05-06. |
| Evidence size | `17,820,145,297` bytes. |
| Evidence hash/check value | SHA256 `12A622AA073DBBDA3A4983014328A6085C8247CE93FE47FD6BA7483ED9D19AAB`. |
| File type check | First bytes show EWF `EVF` signature. |
| Storage rule | Stored in ignored local-only `evidence/` folder and marked read-only. |
| Review environment | WSL Ubuntu forensic toolchain; SIFT-compatible commands available locally. |
| Real accuracy status | Partial real validation exists for evidence access, artifact-family availability, and bounded SOFTWARE Run-key/SYSTEM service registry content. |

## Expected Items To Fill From Real Review

| Expected item ID | Artifact family | Question | Current answer | Confidence | Limitation |
|---|---|---|---|---|---|
| RD01-PARTITION-001 | Partition layout | Which partition should be analyzed? | The image behaves as an NTFS volume image at sector `0`; `mmls` did not provide a partition table and `fsstat` supplied the volume boundary. | Medium | WSL toolchain, not official SIFT OVA. |
| RD01-FS-001 | Filesystem inventory | Which paths are high-signal for the case story? | Root inventory and high-signal inventory completed; registry hives, event logs, user hives, and McAfee Agent event paths were located. | Medium | This is artifact-family availability, not content-level compromise proof. |
| RD01-TIME-001 | Timeline | Which events anchor the attack story? | Unknown. | Low | Full Plaso timeline content was not parsed in the bounded pass. |
| RD01-REG-001 | Registry persistence | Which persistence artifacts are present or absent? | SOFTWARE Run keys and SYSTEM services were extracted and parsed into bounded registry content records. No malicious persistence finding is confirmed from those records alone. | Medium | Deeper registry correlation remains open. |
| RD01-EVT-001 | Event records | Which event records support or contradict the story? | Unknown. Security, System, and Application event-log paths were located but not parsed into events. | Low | Content extraction remains open. |
| RD01-CORR-001 | Correction candidate | Which claim can be visibly corrected by follow-up evidence? | `Confirmed compromise or persistence on RD01` was challenged and dropped. | Medium | Controlled correction from bounded real run, not a full incident conclusion. |
| RD01-NEG-001 | Negative control | Which expected artifact family is absent or inconclusive? | Event content, full timeline, and deeper registry correlation remain unknown rather than overclaimed. | Medium | Unknowns must not be treated as clean results. |

## Promotion Rules

An item can move from `Unknown` to `Confirmed fact` only when:

- the real evidence file exists locally;
- the relevant tool path produced readable output;
- the evidence locator is recorded;
- the claim passes verification;
- no stronger contradictory evidence exists.

## Rejection Rules

An item must stay out of confirmed findings when:

- it is based only on the selected filename;
- it is based only on scenario expectation;
- it is copied from an unofficial writeup without evidence verification;
- it is unsupported by the project execution log.
