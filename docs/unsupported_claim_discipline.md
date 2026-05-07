# Unsupported Claim Discipline

Purpose: make unsupported claims visible evidence discipline rather than hidden
model failure.

## Required Handling

Every unsupported candidate claim must end in one of these states:

- `Dropped`: no support found and no safe follow-up is justified.
- `Corrected`: bounded follow-up changed the claim and the new claim is
  verified.
- `Needs human review`: evidence is missing, conflicted, ambiguous, or parser
  status prevents a safe decision.

## Required Record

For each unsupported claim, record:

- original candidate;
- artifact family;
- verification result;
- reason challenged;
- follow-up action, if any;
- final status;
- evidence references or missing evidence note.

## Output Surfaces

Unsupported claims must appear in at least one of:

- `Unsupported Dropped` section of the final analyst report;
- `Correction Ledger`;
- accuracy report unsupported/hallucination-control section;
- execution log entry with correction reason.

## No Silent Drop Rule

The product must never delete an unsupported claim from the analyst-facing trail
without a visible final disposition.
