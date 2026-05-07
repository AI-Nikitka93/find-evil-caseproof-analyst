# Ground Truth Method

Date: 2026-05-06

Purpose: define how CaseProof Analyst will evaluate findings without pretending that unofficial notes are an official answer key.

## Source Priority

Use this priority order when building expected answers:

1. Official case answer key or official scenario notes, if available.
2. Official starter case description or contest-provided context.
3. Reproducible tool output from the selected evidence image.
4. Reviewer-derived manifest created from documented analyst review.
5. Analyst inference marked as inference, never as confirmed fact.

## Finding Labels

Every important statement must use one of these labels:

| Label | Meaning | Allowed in final confirmed findings |
|---|---|---|
| Confirmed fact | Supported by one or more linked evidence records. | Yes |
| Analyst inference | Reasonable interpretation from evidence, but not directly proven by one record. | Yes, only if clearly marked as inference. |
| Unknown | The available evidence or tooling cannot answer this yet. | Yes, as a limitation. |
| Unsupported | Proposed claim with no sufficient evidence link. | No, except in a dropped/corrected-claim section. |
| Contradicted | Claim conflicts with stronger evidence. | No, except in a correction section. |

## Expected Answer Sources

Expected answers can come from:

- official challenge materials;
- evidence-derived records generated in the case workspace;
- repeated independent tool paths that agree;
- reviewer-derived notes with explicit limitations;
- public writeups only if licensing and provenance allow them to be used as reference, not copied as authoritative truth.

## Rules For Confirmed Facts

A finding can be confirmed only when it has:

- a linked evidence record or source output;
- a specific artifact family;
- a timestamp, path, record ID, offset, or equivalent locator when available;
- no stronger contradictory evidence;
- a final verification result that does not mark it unsupported.

## Rules For Inference

An inference is allowed when:

- it is useful for the analyst story;
- it is derived from confirmed facts;
- it is clearly labeled as inference;
- the report explains what would be needed to upgrade it to confirmed.

An inference is not allowed to become a confirmed compromise claim by wording alone.

## Rules For Unknowns

Unknown must be used when:

- the artifact is absent;
- the tool failed;
- the dataset does not expose the required evidence;
- there is no official ground truth;
- evidence supports multiple interpretations.

Unknown is a valid accuracy outcome. It is better than hallucinating a conclusion.

## Reviewer-Derived Manifest Gate

If no official answer key exists, the project uses a reviewer-derived manifest. That manifest must:

- state that it is not official ground truth;
- list the reviewer, date, source evidence, and review scope;
- separate direct evidence from interpretation;
- include confidence per expected item;
- include limitations and unresolved questions;
- be replaceable if official answers appear later.

## Accuracy Report Mapping

The accuracy report must count:

- confirmed findings;
- inferred findings;
- unsupported claims dropped;
- contradicted claims corrected;
- expected artifact families not found;
- tool failures affecting coverage;
- unknowns that remain after review.

## No-Go Conditions

The project must not publish real accuracy claims if:

- it only used the synthetic fixture;
- the selected `.E01` file was not analyzed;
- expected answers are copied from an unverified source;
- reviewer-derived notes are presented as official answers;
- unsupported claims appear in the final confirmed section.
