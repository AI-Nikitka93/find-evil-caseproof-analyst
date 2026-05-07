from src.claim_policy import (
    AutonomyBudget,
    EvidenceSignal,
    build_controlled_unsupported_claim,
    detect_evidence_conflict,
    draft_claim,
    public_step_rationale,
    retry_decision,
    visible_parser_uncertainty,
    resolve_claim_verification,
    visible_stop_reason,
)


def test_controlled_unsupported_claim_becomes_visible_dropped_ledger_entry() -> None:
    claim = build_controlled_unsupported_claim(
        evidence_id="ev-1",
        artifact_family="registry persistence",
        observed_fact="suspected run key persistence",
    )

    decision = resolve_claim_verification(claim=claim, verifier_status="unsupported", supporting_evidence=[])

    assert decision.final_status == "dropped"
    assert decision.report_section == "Unsupported Dropped"
    assert decision.ledger_entry.original_candidate == claim.claim_text
    assert decision.ledger_entry.reason_challenged == "unsupported_claim"
    assert decision.ledger_entry.final_status == "dropped"


def test_confirmed_claim_requires_supporting_evidence() -> None:
    claim = draft_claim(
        claim_id="c-1",
        artifact_family="timeline",
        observed_fact="powershell execution observed",
        evidence_reference_expectation="timeline record with powershell execution",
        confidence_target="confirmed",
    )

    decision = resolve_claim_verification(claim=claim, verifier_status="confirmed", supporting_evidence=[])

    assert decision.final_status == "needs_human_review"
    assert decision.report_section == "Needs Human Review"
    assert decision.ledger_entry.reason_challenged == "missing_support_for_confirmed"


def test_evidence_conflict_is_first_class_human_review_outcome() -> None:
    conflict = detect_evidence_conflict(
        [
            EvidenceSignal(source="timeline", fact_key="service_install_time", fact_value="2026-05-06T10:00:00Z"),
            EvidenceSignal(source="event_log", fact_key="service_install_time", fact_value="2026-05-06T10:07:00Z"),
        ]
    )

    assert conflict is not None
    assert conflict.reason == "evidence_conflict"
    assert conflict.final_status == "needs_human_review"
    assert "timeline" in conflict.sources
    assert "event_log" in conflict.sources


def test_visible_stop_reason_for_bounded_autonomy() -> None:
    reason = visible_stop_reason(AutonomyBudget(iteration=20, max_iterations=20, tool_calls=12, tool_call_budget=60))

    assert reason is not None
    assert reason.kind == "iteration_budget_exhausted"
    assert "max iteration" in reason.analyst_message.lower()


def test_retry_decision_blocks_unbounded_same_tool_loop() -> None:
    decision = retry_decision(tool_name="build_timeline", same_tool_failures=2)

    assert decision.allow_retry is False
    assert decision.final_status == "needs_human_review"
    assert "build_timeline" in decision.analyst_message


def test_parser_failure_becomes_analyst_visible_uncertainty() -> None:
    uncertainty = visible_parser_uncertainty(
        artifact_family="event records",
        parser_status="failed",
        tool_name="extract_event_records",
    )

    assert uncertainty.final_status == "needs_human_review"
    assert uncertainty.report_section == "Needs Human Review"
    assert "event records" in uncertainty.analyst_message
    assert "extract_event_records" in uncertainty.analyst_message


def test_public_step_rationale_has_no_private_reasoning_markers() -> None:
    rationale = public_step_rationale(
        next_step="verify_claim",
        reason="candidate persistence claim cannot enter the report without linked evidence",
    )

    assert "verify_claim" in rationale
    assert "linked evidence" in rationale
    assert "chain-of-thought" not in rationale.lower()
    assert "private reasoning" not in rationale.lower()
