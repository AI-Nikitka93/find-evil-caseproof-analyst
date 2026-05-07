from src.claim_policy import (
    build_controlled_unsupported_claim,
    resolve_claim_verification,
    visible_parser_uncertainty,
)
from src.reporting import (
    ArtifactOutcome,
    RunAcceptanceInput,
    build_no_evil_found_report,
    build_reviewer_quality_check,
    evaluate_real_run_acceptance,
    render_correction_ledger,
    render_degraded_artifact_notice,
)


def test_correction_ledger_renderer_includes_required_fields() -> None:
    claim = build_controlled_unsupported_claim(
        evidence_id="ev-1",
        artifact_family="registry",
        observed_fact="suspicious persistence",
    )
    decision = resolve_claim_verification(claim=claim, verifier_status="unsupported", supporting_evidence=[])

    rendered = render_correction_ledger([decision.ledger_entry])

    assert "Original candidate: registry: suspicious persistence" in rendered
    assert "Reason challenged: unsupported_claim" in rendered
    assert "Follow-up action: record dropped claim in correction ledger" in rendered
    assert "Final status: dropped" in rendered


def test_no_evil_found_report_states_scope_and_uncertainty_without_overclaiming() -> None:
    report = build_no_evil_found_report(
        case_id="CASE-1",
        checked_scope=["partitions", "filesystem inventory"],
        remaining_uncertainty=["event records unavailable"],
    )

    assert "No confirmed malicious finding was produced." in report
    assert "partitions" in report
    assert "event records unavailable" in report
    assert "clean" not in report.lower()


def test_degraded_artifact_notice_explains_failure_impact_and_unknowns() -> None:
    uncertainty = visible_parser_uncertainty(
        artifact_family="event records",
        parser_status="failed",
        tool_name="extract_event_records",
    )

    notice = render_degraded_artifact_notice(
        artifact_family=uncertainty.artifact_family,
        failed_tool="extract_event_records",
        why_it_matters="logon and service activity cannot be confirmed",
        remaining_unknowns=["whether a service was installed"],
    )

    assert "event records" in notice
    assert "extract_event_records" in notice
    assert "logon and service activity cannot be confirmed" in notice
    assert "whether a service was installed" in notice


def test_real_run_acceptance_requires_all_claims_handled_correction_and_outputs() -> None:
    accepted = evaluate_real_run_acceptance(
        RunAcceptanceInput(
            completed=True,
            clear_stop_reason=None,
            unhandled_claim_ids=[],
            correction_events=1,
            output_paths=["report.md", "evidence_book.md", "correction_ledger.md", "agent_execution.jsonl"],
        )
    )
    rejected = evaluate_real_run_acceptance(
        RunAcceptanceInput(
            completed=True,
            clear_stop_reason=None,
            unhandled_claim_ids=["claim-1"],
            correction_events=0,
            output_paths=["report.md"],
        )
    )

    assert accepted.accepted is True
    assert accepted.blockers == []
    assert rejected.accepted is False
    assert "unhandled_claims" in rejected.blockers
    assert "missing_correction_event" in rejected.blockers
    assert "missing_required_outputs" in rejected.blockers


def test_reviewer_quality_check_flags_unsupported_confirmed_findings() -> None:
    checklist = build_reviewer_quality_check(
        sequence_complete=True,
        failures_visible=True,
        self_correction_visible=True,
        bounded_stop=True,
        final_findings=[
            ArtifactOutcome(name="finding-1", status="confirmed", evidence_refs=["ev-1:row-2"]),
            ArtifactOutcome(name="finding-2", status="confirmed", evidence_refs=[]),
        ],
    )

    assert checklist.ready is False
    assert checklist.items["sequence_quality"] is True
    assert checklist.items["no_unsupported_final_claims"] is False
    assert "finding-2" in checklist.blockers[0]
