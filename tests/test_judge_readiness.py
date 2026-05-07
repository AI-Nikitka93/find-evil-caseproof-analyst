from pathlib import Path

from src.judge_readiness import build_judge_readiness_report, render_judge_readiness_markdown
from scripts.final_submission_audit import GitSyncStatus


def _write_package(root: Path) -> None:
    docs = root / "docs"
    docs.mkdir()
    (root / "scripts").mkdir()
    (root / "src").mkdir()
    (root / "tests").mkdir()
    (root / "README.md").write_text(
        "https://github.com/AI-Nikitka93/find-evil-caseproof-analyst\n",
        encoding="utf-8",
    )
    (root / "LICENSE").write_text("MIT License\n", encoding="utf-8")
    (root / "src" / "agent.py").write_text("MAX_ITERATIONS = 8\n", encoding="utf-8")
    (root / "src" / "prompts.py").write_text("verify_claim\nself-correction\n", encoding="utf-8")
    (root / "src" / "server.py").write_text(
        "def case_open_readonly(): pass\n"
        "def list_partitions(): pass\n"
        "def filesystem_inventory(): pass\n"
        "def build_timeline(): pass\n"
        "def extract_registry_persistence(): pass\n"
        "def extract_event_records(): pass\n"
        "def verify_claim(): pass\n"
        "def write_execution_log(): pass\n"
        "subprocess.run(['safe'], check=False)\n",
        encoding="utf-8",
    )
    for name in (
        "architecture.md",
        "mcp_architecture.md",
        "trust_boundary_contract.md",
        "dataset_documentation.md",
        "accuracy_report.md",
        "judge_try_it_out.md",
        "reviewer_traceability_walkthrough.md",
        "judging_17_readiness.md",
        "autonomous_smoke_hardening_2026-05-07.md",
    ):
        (docs / name).write_text("evidence trace self-correction\n", encoding="utf-8")
    (docs / "final_submission_package.md").write_text(
        "Repo https://github.com/AI-Nikitka93/find-evil-caseproof-analyst\n",
        encoding="utf-8",
    )
    (docs / "demo_video_script.md").write_text(
        "live terminal\nreal evidence\nself-correction\ntrace\n",
        encoding="utf-8",
    )
    (docs / "demo_narration_notes.md").write_text("narration\n", encoding="utf-8")
    (docs / "public_real_execution_log_sample.jsonl").write_text(
        '{"tool_name":"case_open_readonly","parser_status":"ok"}\n'
        '{"tool_name":"extract_registry_persistence","parser_status":"ok"}\n'
        '{"tool_name":"extract_event_records","parser_status":"partial"}\n'
        '{"tool_name":"verify_claim","parser_status":"ok","correction_reason":"Unsupported claim dropped."}\n',
        encoding="utf-8",
    )
    (docs / "public_real_traceability_packet.md").write_text(
        "case_open_readonly\nverify_claim\nself-correction\n",
        encoding="utf-8",
    )
    (root / "scripts" / "demo_rehearsal.py").write_text("print('ready')\n", encoding="utf-8")
    (root / "scripts" / "final_submission_audit.py").write_text("print('audit')\n", encoding="utf-8")
    reports = root / "cases" / "CASE-RD01" / "reports"
    reports.mkdir(parents=True)
    (reports / "final_analyst_report.md").write_text(
        "## Confirmed Findings\n- F001 evidence ev-1\n## Rejected Claims\nNo confirmed malicious finding.\n",
        encoding="utf-8",
    )
    for name in ("evidence_book.md", "correction_ledger.md", "real_run_accuracy_report.md", "replay_consistency.md"):
        (reports / name).write_text("evidence self-correction unsupported claim dropped\n", encoding="utf-8")
    logs = root / "cases" / "CASE-RD01" / "logs"
    logs.mkdir(parents=True)
    (logs / "agent_execution.jsonl").write_text('{"tool_name":"case_open_readonly"}\n', encoding="utf-8")
    exports = root / "cases" / "CASE-RD01" / "exports"
    exports.mkdir(parents=True)
    for name in ("root_inventory.json", "high_signal_inventory.json", "registry_content_summary.json", "event_content_summary.json"):
        (exports / name).write_text("[]", encoding="utf-8")
    (exports / "correlation_summary.json").write_text(
        '{"status":"review_required","confirmed_compromise":false,'
        '"timeline_anchors":[{"timestamp_utc":"2026-05-07T00:00:00Z"}],'
        '"correlation_findings":[{"finding_id":"C001","evidence_refs":["ev:event:1"]}],'
        '"rejected_claims":["Confirmed compromise on RD01"]}',
        encoding="utf-8",
    )


def test_judge_readiness_scores_all_criteria_17_but_keeps_external_submission_blocked(tmp_path: Path) -> None:
    _write_package(tmp_path)

    report = build_judge_readiness_report(
        root=tmp_path,
        git_status=GitSyncStatus(ok=True, detail="clean and synced"),
    )

    assert report["criterion_score_summary"]["all_criteria_at_17"] is True
    assert report["criterion_score_summary"]["scores"] == {
        "Autonomous Execution Quality": 17,
        "IR Accuracy": 17,
        "Breadth And Depth": 17,
        "Constraint Implementation": 17,
        "Audit Trail Quality": 17,
        "Usability And Documentation": 17,
    }
    assert report["submission_gate"]["status"] == "blocked"
    assert report["submission_gate"]["blockers"] == ["demo_video_url", "devpost_url"]


def test_judge_readiness_marks_specific_criterion_below_17_when_trace_is_missing(tmp_path: Path) -> None:
    _write_package(tmp_path)
    (tmp_path / "docs" / "public_real_execution_log_sample.jsonl").write_text(
        '{"tool_name":"case_open_readonly","parser_status":"ok"}\n',
        encoding="utf-8",
    )

    report = build_judge_readiness_report(
        root=tmp_path,
        git_status=GitSyncStatus(ok=True, detail="clean and synced"),
    )

    assert report["criterion_score_summary"]["all_criteria_at_17"] is False
    assert report["criterion_score_summary"]["scores"]["Autonomous Execution Quality"] < 17
    assert report["criterion_score_summary"]["scores"]["Audit Trail Quality"] < 17


def test_render_judge_readiness_markdown_includes_external_boundary(tmp_path: Path) -> None:
    _write_package(tmp_path)
    report = build_judge_readiness_report(
        root=tmp_path,
        git_status=GitSyncStatus(ok=True, detail="clean and synced"),
    )

    markdown = render_judge_readiness_markdown(report)

    assert "# Judge Max Readiness Report" in markdown
    assert "17/17" in markdown
    assert "External submission gate" in markdown
    assert "demo_video_url" in markdown
