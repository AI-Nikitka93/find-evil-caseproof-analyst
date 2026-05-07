# Final Finding Evidence Gate

Purpose: prevent unsupported or hallucinated claims from entering the final
analyst report as confirmed findings.

## Gate Rule

A final `Confirmed` finding is allowed only when all of the following exist:

- claim ID or clear finding text;
- artifact family;
- observed fact;
- `verify_claim` result with status `confirmed`;
- at least one supporting evidence reference;
- tool trace or execution-log reference;
- confidence label;
- no unresolved evidence conflict.

## Report Behavior

If the gate passes:

- place the item under `Confirmed Findings`;
- include evidence reference and tool trace;
- keep the wording factual and bounded.

If the gate fails:

- move the item to `Inferred Findings`, `Unsupported Dropped`, or `Needs Human
  Review`;
- record the reason in `Correction Ledger`;
- do not silently remove the candidate.

## Runtime Reinforcement

The system prompt now requires:

- candidate claims before final findings;
- `verify_claim` before final report inclusion;
- linked evidence for `Confirmed`;
- visible disposition for every candidate claim.

The test suite checks that this behavior remains present in the agent prompt.
