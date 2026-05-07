# Project State

```state
current_goal: Build a read-only Custom MCP Server for Windows disk triage.
current_task: Final local submission package prepared with public-safe real execution trace, bounded registry/event content proof, and verified public GitHub repository; remaining blockers are demo video and Devpost gates.
status: PUBLIC_REPO_READY_EXTERNAL_SUBMISSION_BLOCKED
active_step: Record/upload demo video, paste Devpost text, and verify final public links.
next_step: Create verified public demo video URL, then run final public link audit before Devpost submission.
blockers: ["demo video is not recorded or uploaded", "public video visibility is not verified", "Devpost form is not submitted", "full timeline and deeper registry/event correlation remain open as accepted limitations"]
artifacts: ["README.md", "LICENSE", "docs/architecture.md", "docs/dataset_documentation.md", "docs/submission_readiness_audit.md", "docs/mcp_architecture.md", "docs/accuracy_report.md", "docs/reviewer_traceability_walkthrough.md", "docs/public_real_execution_log_sample.jsonl", "docs/public_real_traceability_packet.md", "docs/final_quality_gate_matrix.md", "docs/final_submission_package.md", "docs/demo_video_script.md", "docs/judge_try_it_out.md", "docs/public_release_manifest.md", "docs/final_release_go_no_go_2026-05-07.md", "agent_execution_log.jsonl", "src/server.py", "src/agent.py", "src/prompts.py", "src/claim_policy.py", "src/reporting.py", "src/phase_gate.py", "src/output_package.py", "src/design_quality.py", "src/visual_system.py", "src/real_validation.py", "scripts/check_env.py", "scripts/preflight_case.py", "scripts/run_real_case.py", "scripts/generate_public_trace_packet.py", "scripts/generate_output_package.py", "scripts/audit_release_controls.py", "scripts/audit_design_quality.py", "scripts/audit_visual_package.py", "scripts/audit_real_validation.py", "tests/test_server_contracts.py", "tests/test_agent_contracts.py", "tests/test_env_check.py", "tests/test_claim_policy.py", "tests/test_reporting_behavior.py", "tests/test_phase_gate.py", "tests/test_output_package.py", "tests/test_design_quality.py", "tests/test_visual_system.py", "tests/test_real_validation_gate.py", "tests/test_public_trace_packet.py", "tests/test_release_controls.py", "tests/mock_eval_fixture.py", "cases/CASE-RD01/reports/final_analyst_report.md", "cases/CASE-RD01/reports/evidence_book.md", "cases/CASE-RD01/reports/correction_ledger.md", "cases/CASE-RD01/reports/real_run_accuracy_report.md", "cases/CASE-RD01/exports/event_content_summary.json", "cases/CASE-RD01/logs/agent_execution.jsonl"]
updated_at: 2026-05-07
```

## Notes

The selected real starter evidence is now present locally at
`M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01`.
It is stored under the ignored local-only `evidence/` folder, marked read-only,
and verified by size, EWF header, and SHA256 hash.
The current server contains backend behavior for the eight public MCP tools.
The current agent is a single-agent + tools runtime with hard iteration, timeout,
tool-call, and token budgets. The required SIFT-compatible binaries, including
`icat`, are available through WSL in this Windows dev environment; official
SANS SIFT OVA clean-machine validation remains open.
The current accuracy report is explicitly a Synthetic Benchmark Fixture for MVP
Validation and must not be described as real APT dataset accuracy.
The root README now routes judges to the required hackathon artifacts and
documents the synthetic nature of current eval metrics.
Local verification passed for tests, syntax, MCP tool listing, JSONL, README
links, evidence file presence, evidence size, EWF header, WSL forensic tool
availability, real bounded CASE-RD01 output audit, release controls, design
audit, visual audit, and markdown link audit. Final local submission package is
prepared. The public GitHub repository is verified at
`https://github.com/AI-Nikitka93/find-evil-caseproof-analyst`. Final Devpost
submission is still blocked by public demo video upload/visibility and the
Devpost form itself.
`scripts/generate_public_trace_packet.py` now produces
`docs/public_real_execution_log_sample.jsonl` and
`docs/public_real_traceability_packet.md` from the latest complete
`cases/CASE-RD01` real run, preserving the step trace, bounded registry
Run-key/service extraction, bounded event extraction, and self-correction
reason without publishing raw local case outputs.
API readiness can now be checked with `py -m src.agent --check-api`.
SIFT runtime readiness can now be checked with `py scripts/check_env.py --strict`.
The latest API readiness check selects OpenRouter as the working implemented
runtime without printing secret values. Groq is also implemented and currently
passes `--check-api`, but OpenRouter remains the selected demo path unless a
fresh Groq smoke run is recorded.
`src/claim_policy.py` now provides tested executable behavior for controlled
unsupported-claim fallback, retry-stop decisions, parser uncertainty, public
step rationale, claim disposition, and evidence conflict handling.
`src/reporting.py` and `src/phase_gate.py` now provide tested executable
behavior for correction-ledger rendering, no-confirmed-finding output,
degraded artifact notices, real-run acceptance, reviewer checks, and Phase 4
ordinary/anchor status gates.
`src/output_package.py` and `scripts/generate_output_package.py` now provide
tested executable output-package generation from structured input, including
real-run accuracy output that does not mix synthetic fixture claims. The output
package now also includes public-safe redaction, reviewer quality gates, judge
summary, reviewer glossary, stable artifact index, and honest unknown/baseline
sections.
`DESIGN.md`, `docs/design_research_note_2026-05-06.md`, `src/design_quality.py`,
and `scripts/audit_design_quality.py` now provide a checked Phase 6 design
contract for evidence-first public docs and Stitch-compatible visual generation.
`src/visual_system.py`, `scripts/audit_visual_package.py`,
`docs/visual_asset_policy.md`, and `docs/demo_narration_notes.md` now provide a
checked visual state catalog, AI-asset production discipline, no-AI fallback,
Mermaid trust/evidence/correction diagrams, README hierarchy, and degraded-state
language.
`docs/visual_qa_checklist.md` and the visual package audit now enforce no
clipped-text intent, diagram readability, no decorative clutter, no misleading
green status, and the rule that visuals cannot mask real validation gaps.
`src/real_validation.py` and `scripts/audit_real_validation.py` now block fake
real-run completion until required real outputs exist. The CASE-RD01 bounded
real pass now satisfies the required local real-output gate and includes
content-level registry parsing for SOFTWARE Run keys/SYSTEM services plus
bounded EVTX event parsing through `python-evtx` when local Plaso is degraded.
`docs/MASTER_TODO_WORLD_CLASS.md` is now a focused submission-critical path,
not the old 220-item planning backlog. Post-release/community/design expansion
work is deferred until after submission. Local actionable tasks are closed; the
remaining open items are external submission gates that require an uploaded
demo video and Devpost submission.
`src/real_validation.py` now also verifies original-evidence snapshots, output
workspace containment, parser-failure visibility, no-confirmed-finding reports,
degraded environment reports, and redaction surfaces. `scripts/run_real_case.py`
uses those boundaries to produce a real bounded CASE-RD01 package without
claiming full incident reconstruction.
`scripts/final_submission_audit.py` is now the final 100-point submission gate:
required files, public repo links, MIT license, public-safe trace,
git/public-repo synchronization, supported video URL, and submitted Devpost URL.
It is expected to remain blocked until video and Devpost URLs exist.
`src/agent.py` was hardened after live OpenRouter smoke runs to repair common
model tool arguments, reject invalid tool names before MCP, compact large tool
outputs before returning them to the model, and report exact stop-limit counts.
The deterministic CASE-RD01 real evidence pass remains the primary demo proof
path; short OpenRouter smoke is useful but not full autonomous incident
reconstruction.
