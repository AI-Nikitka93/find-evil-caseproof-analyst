# Self-Correction Scenarios

Purpose: define the correction situations the product must handle visibly.

## Scenario Set

| Scenario | Trigger | Required response | Final state |
|---|---|---|---|
| Parser failure | Tool returns failed parser status or unreadable output. | Record failure, retry only with a bounded safer argument if available. | Corrected, partial, or needs human review. |
| Unsupported claim | `verify_claim` finds evidence but no matching support. | Drop or run one targeted follow-up check. | Dropped, corrected, or needs human review. |
| Evidence conflict | Two records disagree or timing/source does not align. | Record conflict and run at most one targeted check. | Corrected or needs human review. |
| Missing artifact family | Expected registry, event, timeline, or filesystem family is unavailable. | Report unavailable family and its impact. | Needs human review or limitation. |
| Ambiguous timestamp | Timestamp exists but source, timezone, or meaning is unclear. | Avoid overclaiming sequence; label uncertainty. | Inferred or needs human review. |
| Unsafe request | Next action would require destructive write or broad shell access. | Refuse visibly and record the blocked action. | Dropped or needs human review. |

## Correction Quality Bar

A correction is valid only when:

- the original candidate is visible;
- the reason for challenge is visible;
- the follow-up is bounded and safe;
- the final status is explicit;
- confirmed output is re-verified before reporting.
