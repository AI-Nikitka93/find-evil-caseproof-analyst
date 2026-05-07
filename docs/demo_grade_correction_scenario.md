# Demo-Grade Correction Scenario

Purpose: prepare a correction sequence that can appear in a real evidence run
without staging fake output.

## Primary Scenario

Scenario: unsupported persistence claim challenged by verifier.

Candidate flow:

1. Filesystem or timeline evidence suggests suspicious execution or persistence.
2. Agent drafts a candidate claim naming the artifact family and expected
   supporting reference.
3. `verify_claim` does not find enough support for `Confirmed`.
4. Agent records the challenge in the correction ledger.
5. Agent performs one bounded follow-up using registry persistence or event
   records, if available.
6. If support appears, the claim becomes `Corrected` and may become
   `Confirmed` only after re-verification.
7. If support does not appear, the claim becomes `Dropped` or `Needs human
   review`.

## Why This Is Demo-Grade

- It uses natural DFIR ambiguity: execution hints do not always prove
  persistence.
- It does not require fake evidence.
- It demonstrates the product promise: speed without unsupported findings.
- It shows judge-visible correction through report sections, correction ledger,
  and execution logs.

## Required Evidence Surfaces

The final demo can use this scenario only when the real run contains:

- a candidate claim;
- a verifier challenge;
- a bounded follow-up action;
- final disposition;
- evidence references or explicit missing-support explanation.

## No-Go Condition

If real evidence does not naturally produce this scenario, do not fabricate it.
Use the separate controlled fallback scenario from the next task instead.
