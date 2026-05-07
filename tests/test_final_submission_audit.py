from pathlib import Path

import scripts.final_submission_audit as final_submission_audit


def _write_minimum_package(root: Path) -> None:
    (root / "docs").mkdir()
    (root / "src").mkdir()
    (root / "tests").mkdir()
    (root / "scripts").mkdir()
    (root / "README.md").write_text(
        "Public repo: https://github.com/AI-Nikitka93/find-evil-caseproof-analyst\n",
        encoding="utf-8",
    )
    (root / "LICENSE").write_text("MIT License\n", encoding="utf-8")
    (root / "docs" / "architecture.md").write_text("architecture\n", encoding="utf-8")
    (root / "docs" / "dataset_documentation.md").write_text("dataset\n", encoding="utf-8")
    (root / "docs" / "accuracy_report.md").write_text("accuracy\n", encoding="utf-8")
    (root / "docs" / "judge_try_it_out.md").write_text("try it\n", encoding="utf-8")
    (root / "docs" / "final_submission_package.md").write_text(
        "Repo https://github.com/AI-Nikitka93/find-evil-caseproof-analyst\n"
        "Video DEMO_VIDEO_URL\n",
        encoding="utf-8",
    )
    (root / "docs" / "public_real_traceability_packet.md").write_text("trace\n", encoding="utf-8")
    (root / "docs" / "reviewer_traceability_walkthrough.md").write_text("walkthrough\n", encoding="utf-8")
    (root / "docs" / "judging_17_readiness.md").write_text("judging readiness\n", encoding="utf-8")
    (root / "docs" / "freshness_dependency_register_2026-05-06.md").write_text(
        "Checked: 2026-05-07\n"
        "base-rd-01-cdrive.E01\n"
        "SIFT-compatible commands are available through WSL\n"
        "mcp 1.27.0\n",
        encoding="utf-8",
    )
    (root / "docs" / "pre_release_freshness_checklist.md").write_text(
        "Checked: 2026-05-07\n"
        "base-rd-01-cdrive.E01\n"
        "SIFT-compatible commands are available through WSL\n"
        "mcp 1.27.0\n",
        encoding="utf-8",
    )
    (root / "docs" / "volatile_notes_update_cycle.md").write_text(
        "Checked: 2026-05-07\n"
        "base-rd-01-cdrive.E01\n"
        "SIFT-compatible commands are available through WSL\n"
        "mcp 1.27.0\n",
        encoding="utf-8",
    )
    (root / "docs" / "judge_max_readiness_report.md").write_text(
        "# Judge Max Readiness Report\n"
        "Autonomous Execution Quality\n"
        "IR Accuracy\n"
        "Breadth And Depth\n"
        "Constraint Implementation\n"
        "Audit Trail Quality\n"
        "Usability And Documentation\n"
        "All criteria at 17/17: **true**\n"
        "External submission gate\n",
        encoding="utf-8",
    )
    (root / "docs" / "demo_video_script.md").write_text(
        "live terminal execution\nreal evidence\nself-correction sequence\ntraceability chain\n",
        encoding="utf-8",
    )
    (root / "docs" / "demo_narration_notes.md").write_text("audio narration\n", encoding="utf-8")
    (root / "docs" / "public_real_execution_log_sample.jsonl").write_text(
        '{"tool_name":"case_open_readonly","correction_reason":null}\n'
        '{"tool_name":"extract_registry_persistence","correction_reason":null}\n'
        '{"tool_name":"verify_claim","correction_reason":"Unsupported claim dropped."}\n',
        encoding="utf-8",
    )
    (root / "scripts" / "demo_rehearsal.py").write_text("print('demo rehearsal')\n", encoding="utf-8")
    reports = root / "cases" / "CASE-RD01" / "reports"
    reports.mkdir(parents=True)
    for name in (
        "final_analyst_report.md",
        "evidence_book.md",
        "correction_ledger.md",
        "real_run_accuracy_report.md",
    ):
        (reports / name).write_text("case output\n", encoding="utf-8")
    exports = root / "cases" / "CASE-RD01" / "exports"
    exports.mkdir(parents=True)
    (exports / "correlation_summary.json").write_text(
        '{"status":"review_required","confirmed_compromise":false,'
        '"correlation_findings":[{"finding_id":"C001","evidence_refs":["ev:event:1"]}],'
        '"rejected_claims":["Confirmed compromise on RD01"]}',
        encoding="utf-8",
    )


def test_final_submission_audit_passes_when_external_urls_and_git_sync_are_ready(tmp_path: Path) -> None:
    _write_minimum_package(tmp_path)

    report = final_submission_audit.build_final_submission_audit(
        root=tmp_path,
        demo_video_url="https://youtu.be/example12345",
        devpost_url="https://devpost.com/software/caseproof-analyst",
        git_status=final_submission_audit.GitSyncStatus(ok=True, detail="clean and synced"),
    )

    assert report["status"] == "ready"
    assert report["score"] == 100
    assert report["blockers"] == []
    assert report["external_gates"]["demo_video_url"]["ok"] is True
    assert report["external_gates"]["devpost_url"]["ok"] is True


def test_final_submission_audit_blocks_missing_demo_and_dirty_git(tmp_path: Path) -> None:
    _write_minimum_package(tmp_path)

    report = final_submission_audit.build_final_submission_audit(
        root=tmp_path,
        demo_video_url="DEMO_VIDEO_URL",
        devpost_url="",
        git_status=final_submission_audit.GitSyncStatus(ok=False, detail="dirty working tree"),
    )

    assert report["status"] == "blocked"
    assert report["score"] < 100
    assert "demo_video_url" in report["blockers"]
    assert "devpost_url" in report["blockers"]
    assert "public_repo_sync" in report["blockers"]


def test_final_submission_audit_blocks_when_demo_assets_do_not_prove_correction(tmp_path: Path) -> None:
    _write_minimum_package(tmp_path)
    (tmp_path / "docs" / "demo_video_script.md").write_text("live terminal only\n", encoding="utf-8")

    report = final_submission_audit.build_final_submission_audit(
        root=tmp_path,
        demo_video_url="https://youtu.be/example12345",
        devpost_url="https://devpost.com/software/caseproof-analyst",
        git_status=final_submission_audit.GitSyncStatus(ok=True, detail="clean and synced"),
    )

    assert report["status"] == "blocked"
    assert "demo_rehearsal_assets" in report["blockers"]


def test_final_submission_audit_blocks_broken_required_markdown_link(tmp_path: Path) -> None:
    _write_minimum_package(tmp_path)
    (tmp_path / "README.md").write_text(
        "Public repo: https://github.com/AI-Nikitka93/find-evil-caseproof-analyst\n"
        "[missing](docs/missing.md)\n",
        encoding="utf-8",
    )

    report = final_submission_audit.build_final_submission_audit(
        root=tmp_path,
        demo_video_url="https://youtu.be/example12345",
        devpost_url="https://devpost.com/software/caseproof-analyst",
        git_status=final_submission_audit.GitSyncStatus(ok=True, detail="clean and synced"),
    )

    assert report["status"] == "blocked"
    assert "required_markdown_links" in report["blockers"]


def test_final_submission_audit_blocks_missing_correlation_summary(tmp_path: Path) -> None:
    _write_minimum_package(tmp_path)
    (tmp_path / "cases" / "CASE-RD01" / "exports" / "correlation_summary.json").unlink()

    report = final_submission_audit.build_final_submission_audit(
        root=tmp_path,
        demo_video_url="https://youtu.be/example12345",
        devpost_url="https://devpost.com/software/caseproof-analyst",
        git_status=final_submission_audit.GitSyncStatus(ok=True, detail="clean and synced"),
    )

    assert report["status"] == "blocked"
    assert "correlation_summary" in report["blockers"]


def test_final_submission_audit_blocks_stale_freshness_docs(tmp_path: Path) -> None:
    _write_minimum_package(tmp_path)
    (tmp_path / "docs" / "volatile_notes_update_cycle.md").write_text(
        "Checked: 2026-05-07\n"
        "base-rd-01-cdrive.E01\n"
        "SIFT-compatible commands are available through WSL\n"
        "mcp 1.27.0\n"
        "selected `.E01` file is not present locally\n",
        encoding="utf-8",
    )

    report = final_submission_audit.build_final_submission_audit(
        root=tmp_path,
        demo_video_url="https://youtu.be/example12345",
        devpost_url="https://devpost.com/software/caseproof-analyst",
        git_status=final_submission_audit.GitSyncStatus(ok=True, detail="clean and synced"),
    )

    assert report["status"] == "blocked"
    assert "freshness_surfaces" in report["blockers"]


def test_supported_video_hosts_are_limited_to_devpost_hosts() -> None:
    assert final_submission_audit.is_supported_video_url("https://vimeo.com/123") is True
    assert final_submission_audit.is_supported_video_url("https://www.youtube.com/watch?v=abc") is True
    assert final_submission_audit.is_supported_video_url("https://youtu.be/abc") is True
    assert final_submission_audit.is_supported_video_url("https://youku.com/video/id_abc") is True
    assert final_submission_audit.is_supported_video_url("https://example.com/video") is False
