# Demo Narration Notes

Date: 2026-05-06

Purpose: keep demo narration aligned with the same visual and evidence language
used in README, architecture, accuracy report, and generated evidence surfaces.

## Narration Language

Use forensic clarity and evidence-first language:

- promise: fast first triage without accepting unsupported AI findings;
- status: real validation is blocked until SIFT runtime commands are available;
- output: final report, evidence book, correction ledger, accuracy report, and
  execution logs;
- correction: show the unsupported claim, verifier challenge, targeted
  follow-up, and final disposition.
- visual framing: no decorative dashboard language.

## No Decorative Dashboard Framing

Do not describe the product as a visual cockpit, command center, or generic AI
chat. The demo is terminal-first and dossier-first.

## Empty And Degraded States

No evidence file:

- the run must stop before claiming validation;
- the missing path must be visible.

Missing SIFT runtime:

- the readiness check must show required missing commands;
- the demo must not pretend the real run succeeded.

No confirmed finding:

- the report must say no confirmed finding and list inspected scope.

Partial parser output:

- degraded parser status must be visible in report/evidence surfaces.

Unsupported claim:

- the claim must be dropped, downgraded, or routed to Human Review.

Blocked unsafe action:

- the product boundary must be named and the original evidence must remain
  input-only.
