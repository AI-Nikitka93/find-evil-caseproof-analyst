# Project Map

## Goal

Build a narrow, high-confidence DFIR agent for FIND EVIL! that triages Windows
disk images through a read-only Custom MCP Server.

## Main Artifacts

- `docs/hackathon_strategy.md`: product and judging strategy.
- `docs/research_sift_mcp.md`: technical evidence handoff for MCP and SIFT.
- `docs/mcp_architecture.md`: MCP server contract and integration design.
- `src/server.py`: FastMCP server with read-only backend wrappers.
- `src/agent.py`: autonomous MCP stdio client with Anthropic and OpenAI-compatible OpenRouter/Groq provider paths.
- `src/prompts.py`: DFIR analyst system prompt and initial task prompt builder.
- `src/claim_policy.py`: executable claim/correction policy for controlled unsupported claims, final dispositions, parser uncertainty, retry limits, public step rationale, and evidence conflict detection.
- `src/reporting.py`: executable reporting behavior for correction ledger rendering, no-confirmed-finding reports, degraded artifact notices, real-run acceptance, and reviewer quality checks.
- `src/phase_gate.py`: executable master-TODO phase status parser for ordinary/anchor completion gates.
- `src/output_package.py`: executable judge-facing output package generator for final report, evidence book, correction ledger, real-run accuracy report, execution-log review, public-safe redaction, quality gates, judge summary, reviewer glossary, stable artifact index, and traceability chains.
- `src/design_quality.py`: executable Phase 6 design-package audit for Stitch readiness, forensic visual identity, research-source coverage, and secret-free design docs.
- `src/visual_system.py`: executable visual-system catalog, Mermaid diagram renderers, and public visual-package audit for T119-T128.
- `src/real_validation.py`: executable real-run validation gates for required outputs, evidence-linked confirmed findings, unsupported-claim disposition, visible self-correction, spoliation resistance, original-evidence snapshots, workspace containment, parser failure visibility, no-confirmed-finding behavior, degraded environment reporting, and redaction surfaces.
- `scripts/check_env.py`: local prerequisite checker for SIFT binaries and API environment.
- `scripts/preflight_case.py`: case-specific preflight for evidence path, workspace, API readiness, and SIFT readiness.
- `scripts/run_real_case.py`: deterministic real CASE-RD01 MCP-backend run path for evidence access, bounded filesystem inventory, output-package generation, correction ledger, replay consistency, and real-run summary when autonomous model runtime is unavailable.
- `scripts/generate_public_trace_packet.py`: public-safe real execution-log excerpt generator for publishing CASE-RD01 step trace without raw `cases/` or local absolute paths.
- `scripts/audit_release_controls.py`: release-control audit for local-only rules, public tool stability, schema markers, and obvious secret leaks.
- `scripts/generate_output_package.py`: CLI for generating the judge-facing output package from JSON input.
- `scripts/audit_design_quality.py`: CLI for validating the Phase 6 design package.
- `scripts/audit_visual_package.py`: CLI for validating iconography, diagrams, README hierarchy, degraded states, and cross-surface visual language.
- `scripts/audit_real_validation.py`: CLI for blocking fake real-run completion until required real SIFT artifacts exist.
- `docs/spoliation_threat_model.md`: product-level evidence spoliation threat model and controls.
- `docs/unsafe_action_refusal_story.md`: visible refusal/correction story for unsafe or destructive requests.
- `docs/parser_failure_policy.md`: parser failure, partial output, unknown, and correction policy.
- `docs/output_size_discipline.md`: raw output vs bounded analyst-facing output discipline.
- `docs/codebase_intelligence_evaluation_2026-05-06.md`: current SocratiCode/codebase-intelligence evaluation.
- `docs/codebase_intelligence_safe_workflow.md`: safe activation workflow if codebase intelligence is approved later.
- `docs/manual_code_navigation_rules.md`: manual search-before-reading fallback rules while indexing is skipped.
- `docs/ai_skill_stack_evaluation_2026-05-06.md`: autoskills/security model evaluation and dry-run result.
- `docs/ai_skill_stack_dry_run_2026-05-06.md`: captured safe `autoskills --dry-run` result with no installation.
- `docs/ai_skill_stack_decision_2026-05-06.md`: explicit skip/manual-skill decision for the first release.
- `docs/secret_handling_policy.md`: secret storage, logging, screenshot, and release-gate policy.
- `docs/provider_readiness_check.md`: safe local provider-readiness behavior and current runtime truth.
- `docs/runtime_adapter_language_audit.md`: canonical implemented-runtime vs candidate-adapter wording.
- `docs/future_agent_project_instructions.md`: future-agent read order, operating boundary, and completion rule.
- `docs/no_revert_workspace_discipline.md`: no-revert and no unsafe cleanup rules for shared workspace work.
- `docs/phase3_anchor_review.md`: anchor review for Phase 3 trust and execution-enablement work.
- `docs/phase3_end_review.md`: Phase 3 end review and transition signal.
- `docs/canonical_investigation_flow.md`: canonical open-context-gather-claim-verify-correct-report flow.
- `docs/agent_decision_language.md`: standard claim disposition language for reports and logs.
- `docs/final_finding_evidence_gate.md`: final confirmed-finding evidence gate.
- `docs/unsupported_claim_discipline.md`: no silent drop rule for unsupported claims.
- `docs/self_correction_scenarios.md`: parser, claim, conflict, missing-artifact, timestamp, and unsafe-request correction cases.
- `docs/demo_grade_correction_scenario.md`: natural real-evidence correction scenario for demo use.
- `DESIGN.md`: Stitch-ready design contract for evidence-first documentation visuals and lightweight review surfaces.
- `docs/design_research_note_2026-05-06.md`: design research note covering visual references, Lazyweb decision, design-to-code repository findings, and anti-patterns.
- `docs/visual_asset_policy.md`: iconography direction, AI-assisted asset production cycle, manual metaphor selection, and no-AI fallback visual plan.
- `docs/demo_narration_notes.md`: slides-free demo narration notes aligned with the same forensic visual language and degraded-state language.
- `docs/visual_qa_checklist.md`: visual QA checklist and no-mask rule for real validation blockers.
- `docs/phase5_anchor_review.md`: anchor review for Phase 5 output package hardening.
- `docs/phase5_end_review.md`: Phase 5 end review and transition signal.
- `docs/phase6_anchor_review.md`: anchor review for Phase 6 visual and documentation surface work.
- `docs/phase6_end_review.md`: Phase 6 end review and transition signal.
- `tests/test_server_contracts.py`: backend contract, parser, and safety tests.
- `tests/test_agent_contracts.py`: agent runtime contract tests.
- `tests/test_env_check.py`: environment-check contract tests.
- `tests/test_claim_policy.py`: executable behavior tests for fallback correction, bounded retries, parser uncertainty, claim drafting/verification, public rationale, and evidence conflict handling.
- `tests/test_reporting_behavior.py`: executable tests for correction ledger, no-confirmed-finding, degraded artifact, real-run acceptance, and reviewer checklist behavior.
- `tests/test_phase_gate.py`: executable tests for phase ordinary/anchor status parsing.
- `tests/test_output_package.py`: executable tests for output package generation, real-vs-synthetic separation, traceability, analyst-readable output names, public-safe redaction, quality rubrics, judge summary, reviewer glossary, and honest accuracy sections.
- `tests/test_design_quality.py`: executable tests for the Phase 6 design package, source coverage, and Stitch-ready sections.
- `tests/test_visual_system.py`: executable tests for visual state catalog, Mermaid diagrams, public README hierarchy, degraded states, and visual package audit.
- `tests/test_real_validation_gate.py`: executable tests for real-run artifact gates, final-report evidence links, unsupported claim disposition, self-correction visibility, and spoliation resistance.
- `tests/test_public_trace_packet.py`: executable tests for real execution-log sanitization, trace completeness, correction visibility, and generated public packet files.
- `docs/accuracy_report.md`: real bounded CASE-RD01 accuracy report plus historical synthetic fixture separation.
- `docs/architecture.md`: GitHub-facing architecture diagram and security boundary summary.
- `docs/dataset_documentation.md`: real bounded CASE-RD01 dataset documentation, generated artifacts, observed counts, limitations, and synthetic fixture status.
- `docs/submission_readiness_audit.md`: local verification and FIND EVIL requirement matrix.
- `docs/reviewer_traceability_walkthrough.md`: judge-facing trace path from confirmed findings to evidence references and execution logs.
- `docs/public_real_execution_log_sample.jsonl`: public-safe real CASE-RD01 execution-log excerpt with tool order, parser status, output references, token-usage field, and self-correction reason.
- `docs/public_real_traceability_packet.md`: reviewer walkthrough for the public real execution-log excerpt and self-correction signal.
- `docs/final_quality_gate_matrix.md`: final judging-criteria gate matrix for autonomy, accuracy, depth, constraints, audit trail, usability, media, and release hygiene.
- `docs/final_submission_package.md`: Devpost-ready English project description, story, and required component mapping.
- `docs/demo_video_script.md`: under-5-minute live terminal demo script with self-correction moment and recording safety rules.
- `docs/judge_try_it_out.md`: judge setup, run commands, troubleshooting, and manual recovery guide.
- `docs/public_release_manifest.md`: public include/exclude manifest for GitHub publication and local-only artifact policy.
- `docs/final_release_go_no_go_2026-05-07.md`: current go/no-go decision board and external submission gates.
- `docs/PRODUCT_ANCHOR.md`: product anchor, scope stop rule, and anti-drift boundary.
- `docs/contest_freshness_2026-05-06.md`: live contest facts and local-vs-live comparison.
- `docs/requirement_gap_matrix.md`: contest requirement to artifact/gap/result matrix.
- `docs/positioning_caseproof.md`: public positioning, winning thesis, and scope boundary.
- `docs/audience_positioning.md`: practitioner positioning and audience separation.
- `docs/submission_release_contract.md`: required artifact release gate and no-go conditions.
- `docs/freshness_dependency_register_2026-05-06.md`: freshness-sensitive dependency register.
- `docs/scope_stop_rule.md`: first-release scope acceptance/defer/reject rule.
- `docs/phase1_anchor_review.md`: completed anchor review for T001-T020.
- `docs/phase1_end_review.md`: completed Phase 1 transition review.
- `docs/real_evidence_request.md`: exact evidence file and SIFT environment request for Phase 2 blockers.
- `docs/starter_evidence_availability_2026-05-06.md`: current starter evidence resource status and last known candidate listing.
- `docs/dataset_decision_memo.md`: selected evidence candidate and alternatives.
- `docs/evidence_workspace_policy.md`: original evidence vs generated workspace separation policy.
- `docs/sift_readiness_gate.md`: current SIFT real-run readiness gate.
- `docs/local_vs_sift_readiness_report.md`: local development readiness vs real SIFT readiness.
- `docs/evidence_prerun_checklist.md`: repeatable pre-run gate for API, SIFT, evidence path, workspace, and original-evidence safety.
- `docs/expected_artifact_families.md`: expected partition, filesystem, timeline, registry, event, negative-control, verification, and execution-trail families.
- `docs/ground_truth_method.md`: accuracy labeling method for confirmed facts, inferences, unknowns, unsupported claims, and reviewer-derived expectations.
- `docs/reviewer_derived_manifest_template.md`: ready manifest template for cases without official answer keys.
- `docs/reviewer_derived_manifest_case_rd01.md`: current reviewer-derived manifest state for the selected RD01 evidence candidate.
- `docs/dataset_documentation_outline.md`: final dataset documentation structure before real analysis.
- `docs/demo_host_selection_criteria.md`: criteria for choosing the evidence host/image used in the demo.
- `docs/fallback_dataset_plan.md`: fallback order and switch conditions if the selected evidence file fails.
- `docs/pre_release_freshness_checklist.md`: volatile contest, dataset, SIFT, and release facts to recheck before submission.
- `docs/volatile_notes_update_cycle.md`: recurring update cycle for freshness-sensitive contest, evidence, runtime, and submission facts.
- `docs/real_validation_go_no_go_2026-05-06.md`: current no-go decision for real SIFT validation and exact unblock conditions.
- `docs/local_only_notes_audit.md`: local-only audit for secrets, credentials, evidence, and generated workspaces.
- `docs/phase2_anchor_review.md`: anchor review for Phase 2 readiness work.
- `docs/phase2_end_review.md`: Phase 2 end review with explicit stop signal while real evidence remains missing.
- `docs/trust_boundary_contract.md`: consolidated evidence-safety boundary contract.
- `docs/public_tool_name_stability_check.md`: public MCP tool name stability check.
- `docs/schema_product_entity_mapping.md`: schema-to-product-entity mapping.
- `docs/public_tool_safety_acceptance.md`: per-tool read/create/never-change safety acceptance.
- `docs/MASTER_TODO_WORLD_CLASS.md`: focused submission-critical TODO for real SIFT validation, public submission package, and release gate; old post-release/design expansion is deferred.
- `agent_execution_log.jsonl`: synthetic judge-facing execution log sample.
- `README.md`: GitHub landing page and hackathon artifact checklist.
- `LICENSE`: MIT license.
- `tests/mock_eval_fixture.py`: deterministic generator for the synthetic execution log.

## Scope Boundary

Completed backend scope:

- Eight MCP tool contracts.
- Pydantic input and output schemas.
- Read-only architecture boundary.
- Claude Code / Protocol SIFT integration notes.
- Read-only path validation.
- Bounded parsers for `mmls`, `fls`, Plaso JSON Lines, RegRipper text, and event JSON Lines.
- Append-only execution log in the case workspace.
- Bounded single-agent execution loop with MCP tool routing.
- Final report generation to `report.md`.
- Synthetic accuracy report and execution log fixture.
- GitHub-facing README, MIT license, and architecture diagram.
- Local readiness audit against contest conditions.
- API readiness and SIFT binary preflight checks.
- Secret redaction and provider-readiness language controls.
- Future-agent instructions and no-revert workspace discipline.
- Canonical investigation flow, claim decision language, final finding gate,
  unsupported-claim discipline, and self-correction scenario definitions.
- Executable claim-policy behavior covering fallback unsupported-claim checks,
  bounded retry/stop decisions, analyst-visible parser uncertainty, public
  step rationale, and first-class evidence conflicts.
- Executable reporting behavior for T081-T086 and phase-gate auditing for
  T087-T088.
- Executable output package generation for T089-T108, including CLI JSON input
  integration, real-run accuracy separation from the synthetic fixture,
  public-safe redaction, reviewer quality gates, judge summary, glossary,
  stable artifact index, and honest unknown/baseline sections.
- Executable design-quality audit for T111-T118, including Stitch-ready
  `DESIGN.md`, visual research source coverage, Lazyweb stop condition,
  forensic identity tokens, and no-secret design package checks.
- Executable visual-system audit for T119-T128, including state iconography,
  AI-asset production discipline, no-AI fallback, trust/evidence/correction
  Mermaid diagrams, README hierarchy, and degraded-state documentation.
- Executable visual QA and real-validation gates for T129-T132/T138, including
  visual no-mask checks, Phase 6 anchor/end reviews, required real-run output
  checks, and controlled spoliation-resistance testing.
- Executable local validation gates for T139-T143, covering evidence immutability,
  output workspace containment, parser-failure visibility, no-confirmed-finding
  behavior, degraded environment behavior, and redaction surfaces.
- WSL-backed SIFT-compatible tool execution for local Windows development,
  including `rip.pl` to `regripper` aliasing and volume-image fallback when
  `mmls` does not provide a partition table.
- Real bounded CASE-RD01 output package for T133-T148, including final report,
  evidence book, correction ledger, real-run accuracy report, execution log,
  high-signal inventory export, replay consistency, and reviewer-derived
  manifest comparison.
- Focused active TODO path: real SIFT validation first, then public submission
  package, then release gate. Post-release/community/design expansion is no
  longer active pre-submission work.

Still open:

- Final video and Devpost link/render verification after upload/submission.
- Demo video recording, public upload, and visibility verification.
- Devpost form submission with public links.
- Full long-run autonomous investigation beyond the short OpenRouter smoke run.
- Event-log content, full timeline, and deeper registry correlation beyond the
  bounded pass. SOFTWARE Run-key and SYSTEM service parsing are now covered by
  the current CASE-RD01 run.

## Key Risks

- Parser output fields may differ on the final SIFT image.
- Dataset link availability may affect fixture realism.
- Tool accuracy must be proven with execution logs and claim verification.
