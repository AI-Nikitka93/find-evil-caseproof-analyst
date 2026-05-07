from pathlib import Path

import scripts.audit_release_controls as audit_release_controls


def test_release_controls_report_passes_current_contracts() -> None:
    report = audit_release_controls.build_release_controls_report()

    assert report["status"] == "ok"
    assert report["failed_checks"] == []
    assert report["secrets_redacted"] is True
    assert report["expected_tools"] == list(audit_release_controls.EXPECTED_TOOLS)
    boundary_check = next(check for check in report["checks"] if check["name"] == "boundary_docs_exist")
    assert boundary_check["detail"] == "all release-control docs exist"
    for path in (
        "docs/reviewer_traceability_walkthrough.md",
        "docs/final_quality_gate_matrix.md",
        "docs/final_submission_package.md",
        "docs/demo_video_script.md",
        "docs/judge_try_it_out.md",
        "docs/public_release_manifest.md",
        "docs/public_real_execution_log_sample.jsonl",
        "docs/public_real_traceability_packet.md",
        "docs/final_release_go_no_go_2026-05-07.md",
        "docs/autonomous_smoke_hardening_2026-05-07.md",
    ):
        assert path in audit_release_controls.REQUIRED_DOCS

    public_log_check = next(check for check in report["checks"] if check["name"] == "public_real_execution_log_sample")
    assert public_log_check["ok"] is True
    assert "public-safe real log records" in public_log_check["detail"]
    final_audit_check = next(check for check in report["checks"] if check["name"] == "final_submission_audit_exists")
    assert final_audit_check["ok"] is True


def test_release_controls_detects_missing_ignore_pattern(tmp_path: Path) -> None:
    root = tmp_path
    (root / ".gitignore").write_text(".env\n", encoding="utf-8")
    (root / "src").mkdir()
    (root / "src" / "server.py").write_text("", encoding="utf-8")

    report = audit_release_controls.build_release_controls_report(root)

    assert report["status"] == "blocked"
    assert "local_only_ignore_patterns" in report["failed_checks"]
