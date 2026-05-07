import scripts.check_env as check_env
import scripts.preflight_case as preflight_case


def test_environment_report_lists_required_sift_binaries(monkeypatch) -> None:
    monkeypatch.setattr(check_env.shutil, "which", lambda name: f"/usr/bin/{name}" if name in {"mmls", "fls"} else None)

    report = check_env.build_environment_report()

    names = {item["name"] for item in report["required_sift_binaries"]}
    assert names == {"mmls", "fls", "icat", "log2timeline.py", "psort.py", "rip.pl"}
    assert report["status"] == "blocked"
    assert report["missing_required_sift_binaries"] == ["icat", "log2timeline.py", "psort.py", "rip.pl"]
    assert report["secrets_redacted"] is True


def test_environment_report_never_exposes_api_secret_values(monkeypatch) -> None:
    monkeypatch.setattr(check_env.shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "secret-value")

    report = check_env.build_environment_report()
    serialized = str(report)

    assert report["ready_for_real_sift_run"] is True
    assert "secret-value" not in serialized
    assert any(item["name"] == "ANTHROPIC_API_KEY" and item["configured"] for item in report["api_environment"])


def test_wsl_binary_timeout_is_reported_as_missing(monkeypatch) -> None:
    def timeout_run(*args, **kwargs):
        raise check_env.subprocess.TimeoutExpired(cmd=["wsl"], timeout=30)

    monkeypatch.setattr(check_env.shutil, "which", lambda name: "C:/Windows/System32/wsl.exe" if name == "wsl" else None)
    monkeypatch.setattr(check_env.subprocess, "run", timeout_run)

    result = check_env.check_binary("mmls")

    assert result.found is False
    assert result.path is None


def test_case_preflight_blocks_missing_evidence_and_overlapping_paths(monkeypatch, tmp_path) -> None:
    project_root = tmp_path
    monkeypatch.chdir(project_root)
    monkeypatch.setattr(check_env.shutil, "which", lambda name: None)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    report = preflight_case.build_preflight_report(
        case_id="CASE-RD01",
        evidence_path=str(project_root / "evidence" / "base-rd-01-cdrive.E01"),
        case_workspace=str(project_root / "evidence" / "CASE-RD01"),
    )

    assert report["status"] == "blocked"
    assert "evidence_exists" in report["failed_checks"]
    assert "workspace_not_evidence" in report["failed_checks"]
    assert report["secrets_redacted"] is True


def test_case_preflight_passes_with_realistic_paths_and_runtime(monkeypatch, tmp_path) -> None:
    project_root = tmp_path
    evidence_dir = project_root / "evidence"
    evidence_dir.mkdir()
    evidence_file = evidence_dir / "base-rd-01-cdrive.E01"
    evidence_file.write_bytes(b"0" * 2048)
    workspace = project_root / "cases" / "CASE-RD01"
    monkeypatch.chdir(project_root)
    monkeypatch.setattr(check_env.shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "secret-value")

    report = preflight_case.build_preflight_report(
        case_id="CASE-RD01",
        evidence_path=str(evidence_file),
        case_workspace=str(workspace),
        min_evidence_bytes=1024,
    )
    serialized = str(report)

    assert report["status"] == "ok"
    assert not report["failed_checks"]
    assert "secret-value" not in serialized
