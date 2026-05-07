import json
from pathlib import Path

import pytest

import src.server as server


SERVER_PATH = Path(__file__).resolve().parents[1] / "src" / "server.py"

EXPECTED_TOOLS = {
    "case_open_readonly",
    "list_partitions",
    "filesystem_inventory",
    "build_timeline",
    "extract_registry_persistence",
    "extract_event_records",
    "verify_claim",
    "write_execution_log",
}


def test_server_declares_expected_fastmcp_tools() -> None:
    source = SERVER_PATH.read_text(encoding="utf-8")

    assert "from mcp.server.fastmcp import FastMCP" in source
    assert "MCPServer" not in source
    assert "mcp = FastMCP(" in source

    for tool_name in EXPECTED_TOOLS:
        assert f"def {tool_name}(" in source

    assert source.count("@mcp.tool()") == len(EXPECTED_TOOLS)


def test_backend_implementation_has_no_contract_stubs_or_shell_execution() -> None:
    source = SERVER_PATH.read_text(encoding="utf-8")

    assert "NotImplementedError" not in source
    assert "pass" not in source
    assert "shell=True" not in source
    assert "subprocess.run(" in source
    assert "timeout=" in source
    assert "capture_output=True" in source
    assert "text=True" in source
    assert "check=False" in source


def test_parse_mmls_output_returns_structured_partition_records() -> None:
    output = """
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Size    Description
000:  Meta      0000000000   0000000000   0000000001   0512B   Primary Table (#0)
001:  -------   0000000000   0000002047   0000002048   1.0M    Unallocated
002:  000:000   0000002048   0000204799   0000202752   99M     NTFS / exFAT (0x07)
"""

    partitions = server._parse_mmls_output(output)

    assert len(partitions) == 3
    assert partitions[2].slot == "000:000"
    assert partitions[2].start_sector == 2048
    assert partitions[2].length_sectors == 202752
    assert partitions[2].filesystem_type == "NTFS"
    assert partitions[2].is_allocated is True
    assert partitions[1].is_allocated is False


def test_parse_fls_output_returns_file_inventory_records() -> None:
    output = """
r/r 4-128-1: $AttrDef
d/d 36-144-1: Users
r/r * 38-128-1: deleted.txt
"""

    records = server._parse_fls_output(output, evidence_id="ev-test", max_entries=100)

    assert [record.path for record in records] == ["$AttrDef", "Users", "deleted.txt"]
    assert records[0].entry_type == "file"
    assert records[1].entry_type == "directory"
    assert records[2].entry_type == "deleted"
    assert records[2].allocated is False


def test_parse_regripper_run_output_returns_run_key_values(tmp_path: Path) -> None:
    output = """
run v.20200511
(Software, NTUSER.DAT) [Autostart] Get autostart key contents from Software hive

Microsoft\\Windows\\CurrentVersion\\Run
LastWrite Time 2018-05-11 19:34:10Z
  SecurityHealth - %ProgramFiles%\\Windows Defender\\MSASCuiL.exe
  VMware User Process - "C:\\Program Files\\VMware\\VMware Tools\\vmtoolsd.exe" -n vmusr
"""

    records = server._parse_regripper_output(
        output,
        evidence_id="ev-reg",
        hive_path=tmp_path / "SOFTWARE",
        max_records=10,
    )

    assert any(record.value_name == "SecurityHealth" for record in records)
    security = next(record for record in records if record.value_name == "SecurityHealth")
    assert security.persistence_type == "run_key"
    assert security.registry_path.endswith("CurrentVersion\\Run")
    assert "MSASCuiL.exe" in (security.value_data or "")
    assert not any(record.registry_path.startswith("run v.") for record in records)


def test_parse_regripper_services_output_returns_service_image_paths(tmp_path: Path) -> None:
    output = """
ControlSet001\\Services
Lists services/drivers in Services key by LastWrite times

Thu Sep  6 20:26:36 2018 Z
  Name      = mnemosyne
  Display   = Connected Devices Platform User Service
  ImagePath = \\??\\C:\\windows\\Mnemosyne.sys
  Type      = Kernel driver
  Start     = Manual
  Group     =
"""

    records = server._parse_regripper_output(
        output,
        evidence_id="ev-reg",
        hive_path=tmp_path / "SYSTEM",
        max_records=10,
    )

    service = next(record for record in records if record.value_name == "mnemosyne")
    assert service.persistence_type == "service"
    assert service.registry_path.endswith("Services\\mnemosyne")
    assert "Mnemosyne.sys" in (service.value_data or "")
    assert not any(record.value_name == "Display" for record in records)
    assert not any(record.registry_path.endswith("\\Services") and not record.value_name for record in records)


def test_case_open_rejects_path_traversal(tmp_path: Path) -> None:
    evidence = tmp_path / "disk.E01"
    evidence.write_bytes(b"evidence")

    with pytest.raises(Exception, match="Path traversal"):
        server.case_open_readonly(
            server.CaseOpenReadonlyInput(
                case_id="case1",
                evidence_path=str(evidence),
                case_workspace=str(tmp_path / ".." / "outside"),
            )
        )


def test_missing_sift_binary_raises_tool_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
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

    def raise_missing(*args: object, **kwargs: object) -> object:
        raise FileNotFoundError("mmls")

    monkeypatch.setattr(server.subprocess, "run", raise_missing)

    with pytest.raises(Exception, match="mmls is not available"):
        server.list_partitions(
            server.ListPartitionsInput(
                evidence_id=opened.evidence_id,
                image_path=str(evidence),
            )
        )


def test_plaso_timeline_command_uses_positional_storage_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
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
    calls: list[tuple[str, list[str]]] = []

    def fake_run_command(tool_name: str, args: list[str], **kwargs: object) -> object:
        calls.append((tool_name, args))
        if tool_name == "psort.py":
            jsonl_file = Path(args[args.index("-w") + 1])
            jsonl_file.parent.mkdir(parents=True, exist_ok=True)
            jsonl_file.write_text("", encoding="utf-8")
        return object()

    monkeypatch.setattr(server, "_run_command", fake_run_command)

    server.build_timeline(
        server.BuildTimelineInput(
            evidence_id=opened.evidence_id,
            source_path=str(evidence),
            max_records=1,
        )
    )

    log2timeline_args = calls[0][1]
    assert calls[0][0] == "log2timeline.py"
    assert "--storage-file" not in log2timeline_args
    assert log2timeline_args[-2].endswith(".plaso")
    assert log2timeline_args[-1] == str(evidence.resolve())


def test_event_record_command_uses_positional_storage_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    evidence = tmp_path / "disk.E01"
    evidence.write_bytes(b"evidence")
    workspace = tmp_path / "case"
    event_log = workspace / "exports" / "Security.evtx"
    event_log.parent.mkdir(parents=True)
    event_log.write_bytes(b"evtx")
    opened = server.case_open_readonly(
        server.CaseOpenReadonlyInput(
            case_id="case1",
            evidence_path=str(evidence),
            case_workspace=str(workspace),
        )
    )
    calls: list[tuple[str, list[str]]] = []

    def fake_run_command(tool_name: str, args: list[str], **kwargs: object) -> object:
        calls.append((tool_name, args))
        if tool_name == "psort.py":
            jsonl_file = Path(args[args.index("-w") + 1])
            jsonl_file.parent.mkdir(parents=True, exist_ok=True)
            jsonl_file.write_text("", encoding="utf-8")
        return object()

    monkeypatch.setattr(server, "_run_command", fake_run_command)

    server.extract_event_records(
        server.ExtractEventRecordsInput(
            evidence_id=opened.evidence_id,
            event_log_paths=[str(event_log)],
            max_records=1,
        )
    )

    log2timeline_args = calls[0][1]
    assert calls[0][0] == "log2timeline.py"
    assert "--storage-file" not in log2timeline_args
    assert log2timeline_args[-2].endswith(".plaso")
    assert log2timeline_args[-1] == str(event_log.resolve())


def test_event_records_fallback_to_python_evtx_when_plaso_is_degraded(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    evidence = tmp_path / "disk.E01"
    evidence.write_bytes(b"evidence")
    workspace = tmp_path / "case"
    event_log = workspace / "exports" / "System.evtx"
    event_log.parent.mkdir(parents=True)
    event_log.write_bytes(b"evtx")
    opened = server.case_open_readonly(
        server.CaseOpenReadonlyInput(
            case_id="case1",
            evidence_path=str(evidence),
            case_workspace=str(workspace),
        )
    )

    def fake_run_command(tool_name: str, args: list[str], **kwargs: object) -> object:
        raise server.ToolError("Missing required artifact definition: MacOSLocalTime")

    def fake_python_evtx_reader(
        path: Path,
        *,
        evidence_id: str,
        max_records: int,
        event_ids: set[int],
    ) -> tuple[list[server.EventRecord], bool]:
        assert path == event_log.resolve()
        assert evidence_id == opened.evidence_id
        assert max_records == 5
        assert event_ids == {7045}
        return (
            [
                server.EventRecord(
                    record_id=f"{opened.evidence_id}:event:System.evtx:1",
                    event_id=7045,
                    channel="system",
                    source_path=str(path),
                    provider="Service Control Manager",
                    rendered_message="A service was installed in the system.",
                )
            ],
            False,
        )

    monkeypatch.setattr(server, "_run_command", fake_run_command)
    monkeypatch.setattr(server, "_read_evtx_records_with_python_evtx", fake_python_evtx_reader)

    output = server.extract_event_records(
        server.ExtractEventRecordsInput(
            evidence_id=opened.evidence_id,
            event_log_paths=[str(event_log)],
            event_ids=[7045],
            max_records=5,
        )
    )

    assert output.parser_status == "ok"
    assert output.command_plan.tool == "python-evtx"
    assert output.records[0].event_id == 7045


def test_write_execution_log_appends_jsonl_inside_registered_workspace(tmp_path: Path) -> None:
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

    request = server.WriteExecutionLogInput(
        run_id="run1",
        case_id="case1",
        step_number=1,
        agent_intent="verify test log",
        tool_name="case_open_readonly",
        arguments={"evidence_id": opened.evidence_id},
        parser_status="ok",
        evidence_id=opened.evidence_id,
    )

    first = server.write_execution_log(request)
    second = server.write_execution_log(
        request.model_copy(update={"step_number": 2, "agent_intent": "verify append"})
    )

    assert first.appended is True
    assert second.log_path == first.log_path
    assert Path(first.log_path).is_relative_to(workspace.resolve())
    lines = Path(first.log_path).read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[1])["step_number"] == 2
