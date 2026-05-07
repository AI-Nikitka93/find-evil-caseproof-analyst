# Reviewer-Derived Manifest Template

Date: 2026-05-06

Purpose: provide a ready-to-use manifest format for cases where no official answer key is available.

## Status

This is a template and quality gate. It is not a completed real evidence manifest because the selected evidence image is not present locally yet.

## Manifest Header Fields

| Field | Required content |
|---|---|
| `case_id` | Stable case identifier used in the run command and workspace. |
| `manifest_date` | Date when the reviewer-derived manifest was created or updated. |
| `reviewer` | Person or process that performed the evidence review. |
| `evidence_filename` | Exact evidence filename used for the review. |
| `evidence_source` | Source category and source location where appropriate. |
| `evidence_size` | Exact local byte size from the evidence inventory. |
| `evidence_hash_or_check_value` | Hash or check value generated or provided for the local file. |
| `review_environment` | SIFT-compatible environment used for the review. |
| `official_answer_key_available` | Whether an official answer key was available at review time. |
| `limitations` | Specific limitations that affect confidence or coverage. |

## Expected Item Format

Each expected item must use this structure:

```text
expected_item_id:
artifact_family:
question:
expected_answer:
answer_type: confirmed_fact | analyst_inference | unknown
supporting_evidence:
  - tool_or_review_source:
    evidence_locator:
    short_support:
confidence: high | medium | low
limitations:
contradictions_or_alternatives:
reviewer_notes:
```

## Required Manifest Sections

The reviewer-derived manifest must include:

- partition and filesystem context;
- high-value filesystem artifacts;
- timeline anchors;
- registry persistence or explicit absence;
- event records or explicit absence;
- correction-friendly candidate claims;
- negative controls;
- unresolved unknowns.

## Confidence Rules

| Confidence | Use when |
|---|---|
| High | Multiple evidence records or one strong direct record supports the answer. |
| Medium | Evidence supports the answer, but context or coverage is incomplete. |
| Low | The item is plausible but depends on weak, partial, or indirect evidence. |

Low-confidence items must not become confirmed final findings.

## Limitations Wording

Every reviewer-derived manifest must include this limitation statement:

```text
This manifest is reviewer-derived and is not an official answer key. It exists to support transparent accuracy evaluation when official ground truth is unavailable. Findings must still be verified against case evidence before being reported as confirmed.
```

## Replacement Rule

If an official answer key or authoritative case notes become available later:

- keep this manifest as historical review material;
- mark it superseded;
- update the accuracy report to distinguish official ground truth from reviewer-derived expectations;
- do not silently overwrite prior limitations.

## Current Case Intake Form

```text
case_id: CASE-RD01
manifest_date: 2026-05-06
reviewer: waiting for actual evidence review
evidence_filename: base-rd-01-cdrive.E01
evidence_source: FIND EVIL starter case data / SRL-2018-Compromised Enterprise Network
evidence_size: unavailable until local file inventory exists
evidence_hash_or_check_value: unavailable until local file inventory exists
review_environment: unavailable until SIFT-compatible runtime check passes
official_answer_key_available: no
limitations:
  - The real evidence file has not been inventoried in this local workspace.
  - This intake form is ready for real review but is not a completed evidence manifest.
```
