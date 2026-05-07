# Focused Master TODO

Updated: 2026-05-07

Purpose: keep the remaining work aligned with FIND EVIL! judging requirements
and stop the project from producing secondary documents instead of a real SIFT
run.

## Contest Critical Path

The submission is competitive only if it proves:

- working software on, or integrated with, SANS SIFT Workstation;
- live terminal execution against real evidence;
- visible self-correction;
- confirmed findings traceable to artifacts, files, offsets, or logs;
- structured investigative narrative, not raw logs;
- architecture guardrails enforced outside the prompt;
- public repository with license, setup instructions, and no secrets/private
  evidence;
- demo video, architecture diagram, dataset documentation, accuracy report,
  try-it-out instructions, and execution logs.

## Completed Foundation

The completed foundation remains recorded in `docs/PROJECT_HISTORY.md` and
`docs/PROJECT_MAP.md`. It includes:

- product anchor and scope boundary;
- selected RD01 `.E01` evidence file, local-only and read-only;
- read-only MCP server contracts;
- autonomous agent loop;
- claim verification and correction policy;
- report/evidence/correction/accuracy output package;
- public-safe redaction and release-control checks;
- public-safe real execution-log excerpt and trace packet;
- visual documentation contract and diagrams;
- real-validation gates that block fake completion.

## Active Blocker

The current Windows shell is not a native SIFT runtime, but WSL Ubuntu now
provides the required SIFT-compatible forensic command surface used by the real
bounded CASE-RD01 pass:

- `mmls`
- `fls`
- `log2timeline.py`
- `psort.py`
- `rip.pl`

## PHASE 7 — Real SIFT Validation And Trust Proof

[x] T133 [P0] Run CASE-RD01 in a SIFT-compatible environment against `evidence/base-rd-01-cdrive.E01` without writing to the original evidence.

[x] T134 [P0] Produce the required real-run outputs inside the case workspace: final analyst report, evidence book, correction ledger, real-run accuracy draft, and execution log.

[x] T135 [P0] Verify that every confirmed finding in the real final report has an evidence reference.

[x] T136 [P0] Verify that every unsupported candidate claim in the real run is dropped, downgraded, corrected, or routed to human review.

[x] T137 [P0] Capture at least one visible self-correction sequence from the real run or a controlled verification challenge.

[x] T138 [P0] Verify spoliation resistance: unsafe/destructive action is blocked by unavailable capability or explicit safety boundary and recorded safely.

[x] T139 [P0] Verify original evidence bytes and metadata did not change, and every output lives under the case workspace.

[x] T140 [P0] Verify parser failure behavior with a controlled missing, invalid, or partial artifact scenario.

[x] T141 [P1] Verify no-confirmed-finding behavior on a limited or benign scope if practical.

[x] T142 [P0] Verify degraded environment behavior for missing forensic tools, missing provider key, missing evidence path, and invalid workspace.

[x] T143 [P0] Verify token, secret, local path, and private evidence redaction across generated reports, logs, screenshots, and public docs.

[x] T144 [P1] Verify timestamp and source-reference clarity so a reviewer can understand when and where evidence came from.

[x] T145 [P0] Compare real findings against ground truth or reviewer-derived manifest and record matches, misses, false positives, unknowns, and confidence limits.

[x] T146 [P0] Update the accuracy report from actual real-run results only.

[x] T147 [P0] Update dataset documentation with actual tested evidence, run scope, observed findings, and known limitations.

[x] T148 [P1] Repeat or replay enough of the flow to prove outputs are not one-off accidental artifacts.

[x] T149 [P1] Confirm a reviewer can trace at least one key finding from final report to source evidence without private help.

[x] T150 [P0] Perform a usability dry-run from README instructions in a clean or near-clean SIFT-compatible environment and fix confusing steps.

[x] T151 [P1] Build the final quality gate matrix: autonomy, accuracy, depth, constraints, audit trail, usability, and documentation.

[x] T152 [P0] Update submission readiness audit with real validation evidence and remaining no-go blockers.

## PHASE 8 — Public Submission Package

[x] T153 [P0] Verify public repository readiness: license visible, README accurate, required docs linked, no secrets, no private evidence, no case workspaces. Public GitHub repository verified at `https://github.com/AI-Nikitka93/find-evil-caseproof-analyst`.

[ ] T154 [P0] Refresh Devpost rules before submission and confirm video visibility, required materials, deadline, and language requirements. Rules refreshed on 2026-05-07; video visibility remains external until upload.

[x] T155 [P0] Finalize README first screen around promise, current validation status, quick start, trust boundary, required artifacts, limitations, and contribution path.

[x] T156 [P0] Write final Devpost project description: what it does, how it was built, challenges, learnings, and what is next.

[x] T157 [P0] Shape Devpost story around speed without unsupported findings, real self-correction, evidence chain, and architectural guardrails.

[x] T158 [P0] Prepare demo video script under contest limit: live terminal execution, real evidence, self-correction moment, evidence chain, and final report.

[x] T159 [P0] Rehearse demo and verify no secrets, private paths, copyrighted material, or staged fake output appear.

[ ] T160 [P0] Record live terminal demo that matches actual product behavior and does not rely on slides. External gate: actual video recording and upload are still required.

[ ] T161 [P0] Verify demo clearly shows at least one self-correction sequence and explains why the correction matters. External gate: verify against the uploaded video.

[x] T162 [P1] Prepare short English narration notes explaining trust boundary, evidence book, accuracy report, and current limitations.

[ ] T163 [P0] Verify architecture, trust-boundary, evidence-chain, and correction-loop diagrams render in the public repository view. External gate: public GitHub rendering cannot be checked until publication.

[x] T164 [P0] Update README, Devpost story, and artifact index links to dataset docs, accuracy report, public-safe real execution-log excerpt, and real output package.

[x] T165 [P0] Finalize judge try-it-out instructions: prerequisites, setup, readiness checks, run command, expected outputs, and troubleshooting.

[x] T166 [P1] Finalize troubleshooting for missing SIFT runtime, missing evidence, provider not configured, partial parser results, and blocked unsafe action.

[x] T167 [P0] Verify all public claims against actual artifacts and remove any `ready`, `complete`, or `real accuracy` wording not backed by evidence.

[x] T168 [P0] Build final submission checklist with every required component mapped to a public link or repository path.

## PHASE 9 — Release Gate And Safe Cleanup

[x] T169 [P0] Run safe project hygiene audit for generated noise, temporary scripts, unused drafts, local-only artifacts, and generated caches.

[x] T170 [P0] Isolate drafts and intermediate research outside the public release bundle without deleting review-critical evidence.

[x] T171 [P0] Review dependencies and remove only proven-unused dependencies after tests and audits still pass.

[x] T172 [P0] Verify ignored-file policy protects secrets, local environment notes, evidence downloads, case workspaces, and draft media.

[x] T173 [P0] Run final local verification: tests, syntax, readiness checks, release controls, real-validation audit, visual audit, artifact links, and documentation consistency.

[x] T174 [P0] Verify README, architecture, dataset docs, accuracy report, execution logs, and Devpost story say the same truth.

[x] T175 [P0] Prepare manual recovery instructions for failed judge run: identify blocker, inspect safe outputs, stop condition, and partial-state reporting.

[x] T176 [P0] Verify legal/license surface: MIT license visible, third-party assets allowed, no copyrighted music/material in demo.

[x] T177 [P0] Refresh quickly changing external assumptions before final publication: contest deadline, required artifacts, dataset availability, SIFT setup, platform rules, AI runtime availability.

[x] T178 [P0] Build final release go/no-go board: blockers, accepted limitations, remaining risks, and submission decision.

[ ] T179 [P0] Run final artifact path audit: every README and submission link resolves to existing public material. Local markdown links pass; final public GitHub/video links remain external.

[x] T180 [P0] Record final release state in `docs/STATE.md`, `docs/state.json`, and `docs/PROJECT_HISTORY.md`.

## Deferred Until After Submission

- Full visual investigation cockpit.
- Post-release monitoring and community cycles.
- Long-term benchmark program.
- Additional evidence families beyond the selected disk-triage lane.
- Runtime-provider expansion beyond the currently implemented agent runtime.
- Broad SIFT tool wrapping.
- Marketing/community promotion outside required submission materials.

## Current Release Blockers

- Full long-run autonomous AI investigation remains open; OpenRouter is the current working free/low-cost smoke-tested runtime path, while the local Groq key returned HTTP 403.
- Event-log content, full timeline, and deeper registry correlation remain open; bounded SOFTWARE Run-key and SYSTEM service parsing now exists.
- Public GitHub repository is verified at `https://github.com/AI-Nikitka93/find-evil-caseproof-analyst`.
- Demo video is not recorded or uploaded.
- Public video visibility and public GitHub diagram/link rendering are not verified.
- Devpost form is not submitted with public links.

## Active Count

- Local actionable tasks remaining: 0
- External submission gates remaining: T153, T154, T160, T161, T163, T179
- Closed active tasks retained: T133-T152, T155-T159, T162, T164-T178, T180
- Deferred non-submission tasks removed from active path: 40+
