# Parser Failure Policy

Date: 2026-05-06

Purpose: make parser failure, partial output, and empty output visible product states instead of hidden success.

## Policy

Parser failure is evidence about the run, not an implementation detail to hide.

If a parser fails or returns partial output, the product must:

- preserve the failure status;
- keep the affected artifact family out of confirmed findings;
- trigger a bounded correction or follow-up where safe;
- mark remaining gaps as unknown or needs human review;
- include the limitation in the report or accuracy package when it affects coverage.

## Parser States

| State | Meaning | Product behavior |
|---|---|---|
| `not_started` | Tool path was not attempted. | Do not imply coverage. |
| `ok` | Tool produced readable output within bounds. | Findings may be verified against it. |
| `partial` | Tool produced incomplete, truncated, or limited output. | Findings can be used carefully; limitations must remain visible. |
| `failed` | Tool failed or output could not be parsed. | No confirmed finding from that parser path. |

## Correction Rules

The agent may retry only when:

- the next action is bounded;
- arguments can be corrected without guessing evidence;
- no destructive or broad shell action is required;
- retry count remains within the bounded workflow.

The agent must stop or downgrade when:

- the same parser path fails repeatedly;
- a retry would require arbitrary shell access;
- evidence path or workspace safety is unclear;
- output is absent and no alternative safe artifact path exists.

## Reporting Rules

Final report must distinguish:

- confirmed evidence;
- inference from partial evidence;
- unknown due to missing parser coverage;
- unsupported claim;
- dropped claim;
- needs human review.

## Current Implementation Mapping

Current schema includes parser states through:

- `ParserStatus`;
- tool outputs with `parser_status`;
- execution log records with `parser_status`;
- verifier outcomes for unsupported or human-review claims.

## Acceptance

This policy is ready when:

- parser states are defined;
- correction and stop rules are explicit;
- failed parser output cannot become a confirmed finding by wording alone;
- existing tests and audits preserve visible failure behavior.
