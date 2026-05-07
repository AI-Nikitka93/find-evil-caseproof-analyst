import json
import subprocess
import sys
from pathlib import Path

from scripts.generate_output_package import build_package_from_json
from src.claim_policy import CorrectionLedgerEntry
from src.output_package import (
    AccuracySummary,
    EvidenceBookEntry,
    Finding,
    OutputPackageInput,
    public_safe_redact,
    generate_output_package,
    validate_correction_ledger_quality,
    validate_evidence_book_quality,
    validate_report_quality,
    render_traceability_chain,
)


def _package_input(tmp_path: Path) -> OutputPackageInput:
    return OutputPackageInput(
        case_id="CASE-RD01",
        output_dir=tmp_path,
        executive_summary="One confirmed persistence finding was verified.",
        scope=["Windows disk triage", "registry persistence", "timeline review"],
        confirmed_findings=[
            Finding(
                finding_id="F-001",
                title="Run key persistence",
                status="confirmed",
                evidence_refs=["ev-1:reg-run"],
                tool_trace=["extract_registry_persistence", "verify_claim"],
                confidence="high",
            )
        ],
        inferred_findings=[
            Finding(
                finding_id="F-002",
                title="Possible interactive logon sequence",
                status="inferred",
                evidence_refs=["ev-1:event-4624"],
                tool_trace=["extract_event_records"],
                confidence="medium",
            )
        ],
        rejected_claims=["Service installation was confirmed without supporting evidence"],
        limitations=["Event record parsing was partial"],
        next_actions=["Review service control manager records manually"],
        evidence_book=[
            EvidenceBookEntry(
                finding_id="F-001",
                evidence_ref="ev-1:reg-run",
                source_reference="SYSTEM hive",
                artifact_family="registry persistence",
                extraction_action="extract_registry_persistence",
                parser_status="ok",
                review_notes="Supports run key persistence claim.",
            )
        ],
        correction_entries=[
            CorrectionLedgerEntry(
                original_candidate="Service installation was confirmed",
                reason_challenged="unsupported_claim",
                follow_up_action="downgrade and keep in rejected claims",
                final_status="dropped",
                evidence_references=(),
            )
        ],
        accuracy=AccuracySummary(
            dataset="SRL-2018 base-rd-01-cdrive.E01",
            methodology="Compare verified findings against reviewer-derived manifest.",
            findings_accuracy="Pending real reviewer scoring",
            false_positives=["Service installation was rejected"],
            missed_artifacts=["Unknown until real validation"],
            hallucination_controls=["Unsupported claims are dropped before final confirmed findings"],
            evidence_integrity="Original evidence remains read-only.",
            limits=["No real SIFT run until evidence exists locally"],
            untested_families=["memory artifacts were not part of the disk-only lane"],
            rejected_unsupported_claims=["Service installation was confirmed without supporting evidence"],
            baseline_comparison=None,
        ),
        execution_steps=[
            {"step_number": 1, "tool_name": "extract_registry_persistence", "claim_id": "F-001", "evidence_ref": "ev-1:reg-run"},
            {"step_number": 2, "tool_name": "verify_claim", "claim_id": "F-001", "evidence_ref": "ev-1:reg-run"},
        ],
        synthetic_historical_path="docs/accuracy_report.md",
    )


def test_generate_output_package_writes_required_judge_surfaces(tmp_path: Path) -> None:
    result = generate_output_package(_package_input(tmp_path))

    assert result.created_files.keys() == {
        "final_analyst_report",
        "evidence_book",
        "correction_ledger",
        "real_run_accuracy_report",
        "execution_log_review",
        "judge_summary",
        "reviewer_glossary",
        "quality_gate_summary",
        "artifact_index",
    }
    for path in result.created_files.values():
        assert path.is_file()
        assert path.stat().st_size > 0


def test_final_report_contains_required_sections_without_raw_log_dump(tmp_path: Path) -> None:
    result = generate_output_package(_package_input(tmp_path))
    report = result.created_files["final_analyst_report"].read_text(encoding="utf-8")

    for section in (
        "Executive Summary",
        "Scope",
        "Confirmed Findings",
        "Inferred Findings",
        "Rejected Claims",
        "Limitations",
        "Next Analyst Actions",
    ):
        assert section in report
    assert "Run key persistence" in report
    assert "raw log" not in report.lower()


def test_evidence_book_and_traceability_chain_are_reviewable(tmp_path: Path) -> None:
    result = generate_output_package(_package_input(tmp_path))
    evidence_book = result.created_files["evidence_book"].read_text(encoding="utf-8")
    chain = render_traceability_chain(finding_id="F-001", claim_id="F-001", evidence_ref="ev-1:reg-run", execution_action="verify_claim", source_reference="SYSTEM hive")

    assert "F-001" in evidence_book
    assert "ev-1:reg-run" in evidence_book
    assert "extract_registry_persistence" in evidence_book
    assert chain == "F-001 -> F-001 -> ev-1:reg-run -> verify_claim -> SYSTEM hive"


def test_real_accuracy_report_does_not_mix_synthetic_fixture_claims(tmp_path: Path) -> None:
    result = generate_output_package(_package_input(tmp_path))
    accuracy = result.created_files["real_run_accuracy_report"].read_text(encoding="utf-8")
    artifact_index = json.loads(result.created_files["artifact_index"].read_text(encoding="utf-8"))

    assert accuracy.startswith("# Real Run Accuracy Report")
    assert "Synthetic Benchmark Fixture" not in accuracy
    assert artifact_index["synthetic_historical_fixture"] == "docs/accuracy_report.md"
    assert artifact_index["real_run_accuracy_report"].endswith("real_run_accuracy_report.md")


def test_output_package_uses_analyst_readable_names(tmp_path: Path) -> None:
    result = generate_output_package(_package_input(tmp_path))
    names = {path.name for path in result.created_files.values()}

    assert names == {
        "final_analyst_report.md",
        "evidence_book.md",
        "correction_ledger.md",
        "real_run_accuracy_report.md",
        "execution_log_review.md",
        "judge_summary.md",
        "reviewer_glossary.md",
        "quality_gate_summary.md",
        "artifact_index.json",
    }
    assert not any(name.startswith("dump") or name.startswith("output_") for name in names)


def test_json_cli_payload_builds_same_output_package(tmp_path: Path) -> None:
    payload = {
        "case_id": "CASE-RD01",
        "output_dir": str(tmp_path),
        "executive_summary": "One confirmed finding.",
        "scope": ["registry"],
        "confirmed_findings": [
            {
                "finding_id": "F-001",
                "title": "Run key persistence",
                "status": "confirmed",
                "evidence_refs": ["ev-1:reg-run"],
                "tool_trace": ["verify_claim"],
                "confidence": "high",
            }
        ],
        "inferred_findings": [],
        "rejected_claims": [],
        "limitations": [],
        "next_actions": [],
        "evidence_book": [
            {
                "finding_id": "F-001",
                "evidence_ref": "ev-1:reg-run",
                "source_reference": "SYSTEM hive",
                "artifact_family": "registry persistence",
                "extraction_action": "extract_registry_persistence",
                "parser_status": "ok",
                "review_notes": "Reviewable.",
            }
        ],
        "correction_entries": [
            {
                "original_candidate": "Unsupported service install",
                "reason_challenged": "unsupported_claim",
                "follow_up_action": "drop",
                "final_status": "dropped",
                "evidence_references": [],
            }
        ],
        "accuracy": {
            "dataset": "real dataset",
            "methodology": "reviewer manifest",
            "findings_accuracy": "pending",
            "false_positives": [],
            "missed_artifacts": [],
            "hallucination_controls": [],
            "evidence_integrity": "read-only",
            "limits": [],
        },
        "execution_steps": [],
        "synthetic_historical_path": "docs/accuracy_report.md",
    }

    result = generate_output_package(build_package_from_json(payload))

    assert result.created_files["final_analyst_report"].is_file()
    assert result.created_files["artifact_index"].is_file()


def test_generate_output_package_cli_writes_all_files(tmp_path: Path) -> None:
    payload = {
        "case_id": "CASE-RD01",
        "output_dir": str(tmp_path / "package"),
        "executive_summary": "One confirmed finding.",
        "scope": ["registry"],
        "confirmed_findings": [
            {
                "finding_id": "F-001",
                "title": "Run key persistence",
                "status": "confirmed",
                "evidence_refs": ["ev-1:reg-run"],
                "tool_trace": ["verify_claim"],
                "confidence": "high",
            }
        ],
        "inferred_findings": [],
        "rejected_claims": [],
        "limitations": [],
        "next_actions": [],
        "evidence_book": [
            {
                "finding_id": "F-001",
                "evidence_ref": "ev-1:reg-run",
                "source_reference": "SYSTEM hive",
                "artifact_family": "registry persistence",
                "extraction_action": "extract_registry_persistence",
                "parser_status": "ok",
                "review_notes": "Reviewable.",
            }
        ],
        "correction_entries": [
            {
                "original_candidate": "Unsupported service install",
                "reason_challenged": "unsupported_claim",
                "follow_up_action": "drop",
                "final_status": "dropped",
                "evidence_references": [],
            }
        ],
        "accuracy": {
            "dataset": "real dataset",
            "methodology": "reviewer manifest",
            "findings_accuracy": "pending",
            "false_positives": [],
            "missed_artifacts": [],
            "hallucination_controls": [],
            "evidence_integrity": "read-only",
            "limits": [],
        },
        "execution_steps": [
            {"step_number": 1, "tool_name": "verify_claim", "claim_id": "F-001", "evidence_ref": "ev-1:reg-run"}
        ],
        "synthetic_historical_path": "docs/accuracy_report.md",
    }
    input_json = tmp_path / "input.json"
    input_json.write_text(json.dumps(payload), encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, "scripts/generate_output_package.py", "--input-json", str(input_json), "--json"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    created = json.loads(completed.stdout)["created_files"]
    assert set(created) == {
        "final_analyst_report",
        "evidence_book",
        "correction_ledger",
        "real_run_accuracy_report",
        "execution_log_review",
        "judge_summary",
        "reviewer_glossary",
        "quality_gate_summary",
        "artifact_index",
    }
    for path in created.values():
        assert Path(path).is_file()


def test_public_safe_redaction_removes_local_paths_usernames_and_tokens() -> None:
    text = (
        "Read M:\\Projects\\Konkurs\\Find Evil!\\evidence\\base-rd-01-cdrive.E01 "
        "from C:\\Users\\admin\\.codex with token sk-ant-api03-secret and bearer ghp_secretvalue."
    )

    redacted = public_safe_redact(text)

    assert "M:\\Projects" not in redacted
    assert "C:\\Users\\admin" not in redacted
    assert "sk-ant" not in redacted
    assert "ghp_" not in redacted
    assert "[LOCAL_PATH]" in redacted
    assert "[TOKEN]" in redacted


def test_report_quality_rubric_blocks_raw_logs_and_unsupported_confidence() -> None:
    report = "\n".join(
        [
            "# Final Analyst Report",
            "## Confirmed Findings",
            "- F-001: confirmed evil without evidence",
            "raw log: execute_shell_cmd output",
        ]
    )

    result = validate_report_quality(report)

    assert not result.passed
    assert "raw_log_dump" in result.blockers
    assert "unsupported_confident_language" in result.blockers


def test_evidence_book_quality_requires_reviewable_confirmed_links() -> None:
    confirmed = [
        Finding(
            finding_id="F-001",
            title="Persistence",
            status="confirmed",
            evidence_refs=["ev-1"],
            tool_trace=["verify_claim"],
            confidence="high",
        )
    ]
    entries = [
        EvidenceBookEntry(
            finding_id="F-002",
            evidence_ref="",
            source_reference="source says",
            artifact_family="registry",
            extraction_action="extract_registry_persistence",
            parser_status="ok",
            review_notes="source says this is bad",
        )
    ]

    result = validate_evidence_book_quality(entries, confirmed)

    assert not result.passed
    assert "missing_confirmed_finding_link:F-001" in result.blockers
    assert "ambiguous_source_language" in result.blockers
    assert "missing_evidence_reference" in result.blockers


def test_correction_ledger_quality_blocks_staged_or_incomplete_corrections() -> None:
    entries = [
        CorrectionLedgerEntry(
            original_candidate="fake demo correction",
            reason_challenged="",
            follow_up_action="",
            final_status="dropped",
            evidence_references=(),
        )
    ]

    result = validate_correction_ledger_quality(entries)

    assert not result.passed
    assert "missing_challenge_reason" in result.blockers
    assert "missing_follow_up_action" in result.blockers
    assert "staged_correction_language" in result.blockers


def test_generated_package_contains_judge_summary_glossary_crosslinks_and_honest_accuracy_sections(tmp_path: Path) -> None:
    result = generate_output_package(_package_input(tmp_path))

    judge_summary = result.created_files["judge_summary"].read_text(encoding="utf-8")
    glossary = result.created_files["reviewer_glossary"].read_text(encoding="utf-8")
    accuracy = result.created_files["real_run_accuracy_report"].read_text(encoding="utf-8")
    index = json.loads(result.created_files["artifact_index"].read_text(encoding="utf-8"))

    assert "Inspect first" in judge_summary
    assert "Self-correction" in judge_summary
    assert "Evidence chain" in judge_summary
    assert "## Claim" in glossary
    assert "## Parser failure" in glossary
    assert "## Untested Families And Unknowns" in accuracy
    assert "memory artifacts were not part of the disk-only lane" in accuracy
    assert "## Rejected Unsupported Claims" in accuracy
    assert "## Baseline Comparison" in accuracy
    assert "future scope" in accuracy.lower()
    assert index["stable_entrypoints"]["dataset_documentation"] == "docs/dataset_documentation.md"
    assert index["stable_entrypoints"]["accuracy_report"] == "real_run_accuracy_report.md"
