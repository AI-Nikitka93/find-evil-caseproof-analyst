from pathlib import Path

import src.server as server
from src.claim_policy import CorrectionLedgerEntry
from src.real_validation import (
    REQUIRED_REAL_RUN_OUTPUTS,
    EvidenceSnapshot,
    snapshot_evidence,
    validate_final_report_evidence_links,
    validate_degraded_environment_behavior,
    validate_no_confirmed_finding_report,
    validate_original_evidence_unchanged,
    validate_outputs_under_workspace,
    validate_parser_failure_behavior,
    validate_redaction_surfaces,
    validate_real_run_outputs,
    validate_self_correction_presence,
    validate_spoliation_resistance,
    validate_unsupported_claim_handling,
)


def test_real_run_outputs_block_until_required_artifacts_exist(tmp_path: Path) -> None:
    report = validate_real_run_outputs(tmp_path)

    assert report.passed is False
    assert set(report.missing_outputs) == set(REQUIRED_REAL_RUN_OUTPUTS)


def test_real_run_outputs_pass_when_all_required_artifacts_exist(tmp_path: Path) -> None:
    for relative in REQUIRED_REAL_RUN_OUTPUTS:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("ready", encoding="utf-8")

    report = validate_real_run_outputs(tmp_path)

    assert report.passed is True
    assert report.missing_outputs == []


def test_final_report_gate_blocks_confirmed_finding_without_evidence_reference() -> None:
    result = validate_final_report_evidence_links(
        "# Final Report\n## Confirmed Findings\n- F-001: confirmed persistence\n## Rejected Claims\n- none"
    )

    assert result.passed is False
    assert "confirmed_finding_without_evidence:F-001" in result.blockers


def test_unsupported_claim_gate_requires_final_disposition() -> None:
    result = validate_unsupported_claim_handling(
        candidate_claim_ids=["C-1", "C-2"],
        final_dispositions={"C-1": "dropped", "C-2": "confirmed"},
    )

    assert result.passed is False
    assert "unhandled_unsupported_claim:C-2" in result.blockers


def test_self_correction_gate_requires_visible_correction_entry() -> None:
    result = validate_self_correction_presence([])

    assert result.passed is False
    assert "missing_visible_self_correction" in result.blockers


def test_spoliation_resistance_blocks_unsafe_action_and_logs_inside_workspace(tmp_path: Path) -> None:
    evidence = tmp_path / "disk.E01"
    evidence.write_bytes(b"evidence")
    workspace = tmp_path / "case"
    opened = server.case_open_readonly(
        server.CaseOpenReadonlyInput(
            case_id="case1",
            evidence_path=str(evidence),
            case_workspace=str(workspace),
        )
    )
    blocked_log = server.write_execution_log(
        server.WriteExecutionLogInput(
            run_id="run-spoliation",
            case_id="case1",
            step_number=1,
            agent_intent="blocked unsafe request to modify original evidence",
            tool_name="blocked_unsafe_action",
            arguments={"requested_action": "delete original evidence"},
            parser_status="failed",
            evidence_id=opened.evidence_id,
            correction_reason="unsafe action is outside public MCP capability",
        )
    )

    result = validate_spoliation_resistance(
        server_source=Path(server.__file__).read_text(encoding="utf-8"),
        evidence_path=evidence,
        log_path=Path(blocked_log.log_path),
        workspace_path=workspace,
    )

    assert result.passed is True
    assert evidence.read_bytes() == b"evidence"
    assert Path(blocked_log.log_path).is_relative_to(workspace.resolve())


def test_self_correction_gate_accepts_real_or_controlled_correction() -> None:
    result = validate_self_correction_presence(
        [
            CorrectionLedgerEntry(
                original_candidate="C-1",
                reason_challenged="unsupported_claim",
                follow_up_action="targeted follow-up",
                final_status="dropped",
                evidence_references=("ev-1",),
            )
        ]
    )

    assert result.passed is True


def test_original_evidence_snapshot_and_workspace_output_gate(tmp_path: Path) -> None:
    evidence = tmp_path / "disk.E01"
    evidence.write_bytes(b"evidence")
    workspace = tmp_path / "case"
    output = workspace / "reports" / "final_analyst_report.md"
    output.parent.mkdir(parents=True)
    output.write_text("report", encoding="utf-8")

    before = snapshot_evidence(evidence, sha256="abc")
    after = snapshot_evidence(evidence, sha256="abc")

    assert validate_original_evidence_unchanged(before, after).passed is True
    assert validate_outputs_under_workspace([output], workspace).passed is True


def test_original_evidence_snapshot_gate_blocks_changed_metadata() -> None:
    before = EvidenceSnapshot(path="disk.E01", size_bytes=10, modified_ns=100, sha256="a")
    after = EvidenceSnapshot(path="disk.E01", size_bytes=11, modified_ns=100, sha256="a")

    result = validate_original_evidence_unchanged(before, after)

    assert result.passed is False
    assert "evidence_size_changed" in result.blockers


def test_parser_failure_behavior_requires_visible_uncertainty() -> None:
    accepted = validate_parser_failure_behavior(
        parser_status="failed",
        visible_notice="Parser failed; registry persistence cannot be confirmed and remains unknown.",
    )
    rejected = validate_parser_failure_behavior(parser_status="ok", visible_notice="Everything worked.")

    assert accepted.passed is True
    assert rejected.passed is False
    assert "parser_status_not_degraded" in rejected.blockers
    assert "parser_failure_not_visible" in rejected.blockers


def test_no_confirmed_finding_report_gate_blocks_clean_overclaim() -> None:
    accepted = validate_no_confirmed_finding_report(
        "No confirmed malicious finding was produced. Scope: partition and filesystem inventory."
    )
    rejected = validate_no_confirmed_finding_report("System is clean.")

    assert accepted.passed is True
    assert rejected.passed is False
    assert "missing_no_confirmed_statement" in rejected.blockers
    assert "overclaims_clean_result" in rejected.blockers


def test_degraded_environment_behavior_requires_blocked_status_failed_checks_and_details() -> None:
    accepted = validate_degraded_environment_behavior(
        {
            "status": "blocked",
            "failed_checks": ["sift_ready"],
            "checks": [{"name": "sift_ready", "ok": False, "detail": "missing tools"}],
        }
    )
    rejected = validate_degraded_environment_behavior({"status": "ok", "failed_checks": [], "checks": []})

    assert accepted.passed is True
    assert rejected.passed is False
    assert "degraded_environment_not_blocked" in rejected.blockers
    assert "degraded_environment_missing_failed_checks" in rejected.blockers


def test_redaction_surface_gate_blocks_unredacted_private_values() -> None:
    accepted = validate_redaction_surfaces(
        {
            "report": "Path M:\\Projects\\Konkurs\\Find Evil\\evidence\\disk.E01 token sk-ant-secretvalue",
            "log": "Bearer ghp_secretvalue",
        }
    )

    assert accepted.passed is True
