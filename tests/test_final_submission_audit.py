from pathlib import Path

import scripts.final_submission_audit as final_submission_audit


def _write_minimum_package(root: Path) -> None:
    (root / "docs").mkdir()
    (root / "src").mkdir()
    (root / "tests").mkdir()
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
    (root / "docs" / "public_real_execution_log_sample.jsonl").write_text(
        '{"tool_name":"case_open_readonly","correction_reason":null}\n'
        '{"tool_name":"verify_claim","correction_reason":"Unsupported claim dropped."}\n',
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


def test_supported_video_hosts_are_limited_to_devpost_hosts() -> None:
    assert final_submission_audit.is_supported_video_url("https://vimeo.com/123") is True
    assert final_submission_audit.is_supported_video_url("https://www.youtube.com/watch?v=abc") is True
    assert final_submission_audit.is_supported_video_url("https://youtu.be/abc") is True
    assert final_submission_audit.is_supported_video_url("https://youku.com/video/id_abc") is True
    assert final_submission_audit.is_supported_video_url("https://example.com/video") is False
