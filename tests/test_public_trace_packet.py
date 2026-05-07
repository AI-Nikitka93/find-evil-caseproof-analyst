from pathlib import Path

from scripts.generate_public_trace_packet import (
    generate_public_trace_packet,
    sanitize_execution_records,
    validate_public_text,
    validate_trace_records,
)


def test_sanitized_public_trace_removes_local_paths_and_keeps_correction() -> None:
    records = [
        {
            "case_id": "CASE-RD01",
            "run_id": "real-1",
            "step_number": 1,
            "timestamp_utc": "2026-05-06T00:00:00Z",
            "agent_intent": "Open evidence.",
            "tool_name": "case_open_readonly",
            "parser_status": "ok",
            "arguments": {
                "evidence_path": r"M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01",
                "case_workspace": r"M:\Projects\Konkurs\Find Evil!\cases\CASE-RD01",
            },
            "evidence_id": "ev-local",
            "output_reference": "reports/artifact_index.json",
            "correction_reason": None,
            "token_usage": None,
        },
        {
            "case_id": "CASE-RD01",
            "run_id": "real-1",
            "step_number": 2,
            "timestamp_utc": "2026-05-06T00:00:01Z",
            "agent_intent": "Identify filesystem boundary.",
            "tool_name": "list_partitions",
            "parser_status": "ok",
            "arguments": {"image_path": r"M:\Projects\Konkurs\Find Evil!\evidence\base-rd-01-cdrive.E01"},
            "evidence_id": "ev-local",
            "output_reference": "reports/evidence_book.md",
            "correction_reason": None,
            "token_usage": None,
        },
        {
            "case_id": "CASE-RD01",
            "run_id": "real-1",
            "step_number": 3,
            "timestamp_utc": "2026-05-06T00:00:02Z",
            "agent_intent": "Inventory filesystem.",
            "tool_name": "filesystem_inventory",
            "parser_status": "ok",
            "arguments": {"recursive": True},
            "evidence_id": "ev-local",
            "output_reference": "exports/high_signal_inventory.json",
            "correction_reason": None,
            "token_usage": None,
        },
        {
            "case_id": "CASE-RD01",
            "run_id": "real-1",
            "step_number": 4,
            "timestamp_utc": "2026-05-06T00:00:03Z",
            "agent_intent": "Parse registry content.",
            "tool_name": "extract_registry_persistence",
            "parser_status": "ok",
            "arguments": {"hive": "SOFTWARE"},
            "evidence_id": "ev-local",
            "output_reference": "exports/registry_content_summary.json",
            "correction_reason": None,
            "token_usage": None,
        },
        {
            "case_id": "CASE-RD01",
            "run_id": "real-1",
            "step_number": 5,
            "timestamp_utc": "2026-05-06T00:00:04Z",
            "agent_intent": "Challenge unsupported claim.",
            "tool_name": "verify_claim",
            "parser_status": "ok",
            "arguments": {"claim": "Confirmed compromise or persistence on RD01"},
            "evidence_id": "ev-local",
            "output_reference": "reports/correction_ledger.md",
            "correction_reason": "Unsupported compromise claim dropped from confirmed findings.",
            "token_usage": None,
        },
    ]

    sanitized = sanitize_execution_records(records, case_id="CASE-RD01")
    rendered = "\n".join(str(record) for record in sanitized)

    assert validate_trace_records(sanitized) == []
    assert validate_public_text(rendered) == []
    assert "M:\\" not in rendered
    assert "evidence/base-rd-01-cdrive.E01" in rendered
    assert "[RUN_EVIDENCE_ID]" in rendered
    assert "Unsupported compromise claim dropped" in rendered


def test_generate_public_trace_packet_writes_required_files(tmp_path: Path) -> None:
    workspace = tmp_path / "CASE-RD01"
    log = workspace / "logs" / "agent_execution.jsonl"
    log.parent.mkdir(parents=True)
    log.write_text(
        "\n".join(
            [
                '{"step_number":1,"timestamp_utc":"2026-05-06T00:00:00Z","agent_intent":"open","tool_name":"case_open_readonly","parser_status":"ok","arguments":{},"evidence_id":"ev","output_reference":"reports/artifact_index.json","correction_reason":null,"token_usage":null,"run_id":"r"}',
                '{"step_number":2,"timestamp_utc":"2026-05-06T00:00:01Z","agent_intent":"partition","tool_name":"list_partitions","parser_status":"ok","arguments":{},"evidence_id":"ev","output_reference":"reports/evidence_book.md","correction_reason":null,"token_usage":null,"run_id":"r"}',
                '{"step_number":3,"timestamp_utc":"2026-05-06T00:00:02Z","agent_intent":"inventory","tool_name":"filesystem_inventory","parser_status":"ok","arguments":{},"evidence_id":"ev","output_reference":"exports/high_signal_inventory.json","correction_reason":null,"token_usage":null,"run_id":"r"}',
                '{"step_number":4,"timestamp_utc":"2026-05-06T00:00:03Z","agent_intent":"registry","tool_name":"extract_registry_persistence","parser_status":"ok","arguments":{},"evidence_id":"ev","output_reference":"exports/registry_content_summary.json","correction_reason":null,"token_usage":null,"run_id":"r"}',
                '{"step_number":5,"timestamp_utc":"2026-05-06T00:00:04Z","agent_intent":"verify","tool_name":"verify_claim","parser_status":"ok","arguments":{},"evidence_id":"ev","output_reference":"reports/correction_ledger.md","correction_reason":"Unsupported compromise claim dropped from confirmed findings.","token_usage":null,"run_id":"r"}',
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    public_log = tmp_path / "public.jsonl"
    public_trace = tmp_path / "public.md"
    result = generate_public_trace_packet(case_workspace=workspace, public_log_path=public_log, public_trace_path=public_trace)

    assert result["status"] == "ok"
    assert result["records"] == 5
    assert public_log.is_file()
    assert public_trace.is_file()
    assert "Public Real Traceability Packet" in public_trace.read_text(encoding="utf-8")
