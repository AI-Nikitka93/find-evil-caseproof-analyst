from pathlib import Path

from scripts import run_real_case
from src import server


def test_extract_artifact_from_image_uses_icat_and_writes_binary_output(monkeypatch, tmp_path: Path) -> None:
    evidence = tmp_path / "disk.E01"
    evidence.write_bytes(b"evidence")
    exports = tmp_path / "case" / "exports"
    record = server.FileMetadataRecord(
        record_id="ev-test:fls:1:164257-128-3",
        path="Windows/System32/config/SYSTEM",
        inode="164257-128-3",
        entry_type="file",
        allocated=True,
    )
    calls: list[list[str]] = []

    class Completed:
        returncode = 0
        stdout = b"registry-bytes"
        stderr = b""

    def fake_execution_args(tool_name: str, args: list[str]) -> list[str]:
        calls.append(args)
        assert tool_name == "icat"
        return args

    def fake_run(args: list[str], **kwargs: object) -> Completed:
        assert kwargs["capture_output"] is True
        assert kwargs["check"] is False
        return Completed()

    monkeypatch.setattr(run_real_case.server, "_execution_args", fake_execution_args)
    monkeypatch.setattr(run_real_case.subprocess, "run", fake_run)

    output_path = run_real_case._extract_artifact_from_image(
        record=record,
        evidence_path=evidence,
        partition_start_sector=0,
        exports_dir=exports,
    )

    assert calls == [["icat", "-o", "0", str(evidence), "164257-128-3"]]
    assert output_path == exports / "SYSTEM"
    assert output_path.read_bytes() == b"registry-bytes"


def test_extract_named_artifacts_from_image_extracts_matching_records(monkeypatch, tmp_path: Path) -> None:
    evidence = tmp_path / "disk.E01"
    evidence.write_bytes(b"evidence")
    exports = tmp_path / "case" / "exports"
    records = [
        server.FileMetadataRecord(
            record_id="ev-test:fls:1:21867-128-4",
            path="Windows/System32/winevt/Logs/Security.evtx",
            inode="21867-128-4",
            entry_type="file",
            allocated=True,
        ),
        server.FileMetadataRecord(
            record_id="ev-test:fls:2:21865-128-4",
            path="Windows/System32/winevt/Logs/Application.evtx",
            inode="21865-128-4",
            entry_type="file",
            allocated=True,
        ),
    ]

    def fake_extract_artifact_from_image(**kwargs: object) -> Path:
        record = kwargs["record"]
        assert isinstance(record, server.FileMetadataRecord)
        output = exports / Path(record.path).name
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(record.path.encode("utf-8"))
        return output

    monkeypatch.setattr(run_real_case, "_extract_artifact_from_image", fake_extract_artifact_from_image)

    extracted = run_real_case._extract_named_artifacts_from_image(
        records=records,
        wanted_paths=("Windows/System32/winevt/Logs/Security.evtx", "Windows/System32/winevt/Logs/System.evtx"),
        evidence_path=evidence,
        partition_start_sector=0,
        exports_dir=exports,
    )

    assert list(extracted) == ["Windows/System32/winevt/Logs/Security.evtx"]
    assert extracted["Windows/System32/winevt/Logs/Security.evtx"].name == "Security.evtx"
