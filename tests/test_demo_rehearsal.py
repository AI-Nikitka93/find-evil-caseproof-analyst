from pathlib import Path

from scripts import demo_rehearsal


def _write_demo_package(root: Path) -> None:
    docs = root / "docs"
    docs.mkdir()
    (docs / "demo_video_script.md").write_text(
        "live terminal execution\nreal evidence\nself-correction sequence\ntraceability chain\n",
        encoding="utf-8",
    )
    (docs / "demo_narration_notes.md").write_text("audio narration\n", encoding="utf-8")
    (docs / "public_real_traceability_packet.md").write_text(
        "## Self-Correction Signal\nUnsupported compromise claim dropped from confirmed findings.\n",
        encoding="utf-8",
    )
    (docs / "public_real_execution_log_sample.jsonl").write_text(
        '{"step_number":1,"tool_name":"case_open_readonly","parser_status":"ok","correction_reason":null}\n'
        '{"step_number":2,"tool_name":"filesystem_inventory","parser_status":"ok","correction_reason":null}\n'
        '{"step_number":3,"tool_name":"extract_registry_persistence","parser_status":"ok","correction_reason":null}\n'
        '{"step_number":4,"tool_name":"extract_event_records","parser_status":"partial","correction_reason":null}\n'
        '{"step_number":5,"tool_name":"verify_claim","parser_status":"ok","correction_reason":"Unsupported compromise claim dropped from confirmed findings."}\n',
        encoding="utf-8",
    )
    reports = root / "cases" / "CASE-RD01" / "reports"
    reports.mkdir(parents=True)
    for name in (
        "final_analyst_report.md",
        "evidence_book.md",
        "correction_ledger.md",
        "real_run_accuracy_report.md",
    ):
        (reports / name).write_text("case output\n", encoding="utf-8")


def test_demo_rehearsal_report_confirms_required_video_story(tmp_path: Path) -> None:
    _write_demo_package(tmp_path)

    report = demo_rehearsal.build_demo_rehearsal_report(root=tmp_path, case_id="CASE-RD01")

    assert report["status"] == "ready"
    assert report["blockers"] == []
    assert report["demo_story"]["has_real_evidence_open"] is True
    assert report["demo_story"]["has_self_correction"] is True
    assert report["demo_story"]["has_registry_or_event_depth"] is True
    assert report["commands"]["deterministic_real_run"].startswith("py scripts\\run_real_case.py")


def test_demo_rehearsal_blocks_when_public_trace_has_no_correction(tmp_path: Path) -> None:
    _write_demo_package(tmp_path)
    (tmp_path / "docs" / "public_real_execution_log_sample.jsonl").write_text(
        '{"step_number":1,"tool_name":"case_open_readonly","parser_status":"ok","correction_reason":null}\n',
        encoding="utf-8",
    )

    report = demo_rehearsal.build_demo_rehearsal_report(root=tmp_path, case_id="CASE-RD01")

    assert report["status"] == "blocked"
    assert "self_correction_trace" in report["blockers"]
