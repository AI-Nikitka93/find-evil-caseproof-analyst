from pathlib import Path
import asyncio

import src.agent as agent


ROOT = Path(__file__).resolve().parents[1]
AGENT_PATH = ROOT / "src" / "agent.py"
PROMPTS_PATH = ROOT / "src" / "prompts.py"


def test_agent_files_exist() -> None:
    assert AGENT_PATH.exists()
    assert PROMPTS_PATH.exists()


def test_agent_has_bounded_stdio_mcp_execution_loop() -> None:
    source = AGENT_PATH.read_text(encoding="utf-8")

    assert "MAX_ITERATIONS = 20" in source
    assert "GLOBAL_TIMEOUT_SECONDS" in source
    assert "stdio_client.stdio_client" in source
    assert "StdioServerParameters" in source
    assert 'DEFAULT_MCP_SERVER_COMMAND = "python"' in source
    assert 'os.environ.get("MCP_SERVER_COMMAND", DEFAULT_MCP_SERVER_COMMAND)' in source
    assert 'args=["-m", "src.server"]' in source
    assert "while iteration < max_iterations" in source
    assert "if not tool_uses:" in source
    assert "report_path.write_text" in source
    assert "input(" not in source


def test_agent_uses_env_api_key_and_handles_tool_errors() -> None:
    source = AGENT_PATH.read_text(encoding="utf-8")

    assert 'os.environ.get(env_var)' in source
    assert "select_runtime_provider" in source
    assert "ToolExecutionError" in source
    assert '"is_error": True' in source
    assert "write_execution_log" in source
    assert "token_budget" in source


def test_api_readiness_uses_free_provider_when_anthropic_is_missing(monkeypatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("GROQ_API_KEY", "secret-value")
    monkeypatch.setenv("OPENROUTER_API_KEY", "secret-value")
    monkeypatch.setenv("FIND_EVIL_AGENT_PROVIDER", "auto")

    report = agent.build_api_readiness_report()
    serialized = str(report)
    statuses = {item["provider"]: item["runtime_status"] for item in report["providers"]}

    assert report["current_runtime"] == "openrouter"
    assert report["current_runtime_ready"] is True
    assert report["required_for_current_agent"] == "OPENROUTER_API_KEY"
    assert "Ready to run with openrouter." in report["recommendation"]
    assert statuses["anthropic"] == "implemented"
    assert statuses["groq"] == "implemented"
    assert statuses["openrouter"] == "implemented"
    assert "secret-value" not in serialized


def test_tool_input_repair_only_adds_known_case_context() -> None:
    task_state = agent.TaskState(
        run_id="run-test",
        case_id="CASE-RD01",
        evidence_path="M:/evidence/base-rd-01-cdrive.E01",
        case_workspace="M:/cases/CASE-RD01",
        report_path=Path("report.md"),
        evidence_id="ev-test",
    )

    repaired = agent._repair_tool_input_from_task_state("list_partitions", {"sector_size": 512}, task_state)

    assert repaired["evidence_id"] == "ev-test"
    assert repaired["image_path"] == "M:/evidence/base-rd-01-cdrive.E01"
    assert repaired["sector_size"] == 512
    assert "selected_partition_start_sector" not in repaired

    malformed = agent._repair_tool_input_from_task_state("list_partitions", "ev-test", task_state)  # type: ignore[arg-type]
    assert malformed["evidence_id"] == "ev-test"
    assert malformed["image_path"] == "M:/evidence/base-rd-01-cdrive.E01"


def test_write_execution_log_input_repair_fills_required_fields() -> None:
    task_state = agent.TaskState(
        run_id="run-test",
        case_id="CASE-RD01",
        evidence_path="M:/evidence/base-rd-01-cdrive.E01",
        case_workspace="M:/cases/CASE-RD01",
        report_path=Path("report.md"),
        evidence_id="ev-test",
    )

    repaired = agent._repair_tool_input_from_task_state(
        "write_execution_log",
        {"agent_intent": "Record dropped unsupported claim.", "tool_name": "verify_claim"},
        task_state,
    )

    assert repaired["run_id"] == "run-test"
    assert repaired["case_id"] == "CASE-RD01"
    assert repaired["step_number"] == 1
    assert repaired["parser_status"] == "ok"
    assert repaired["evidence_id"] == "ev-test"
    assert repaired["agent_intent"] == "Record dropped unsupported claim."
    assert repaired["tool_name"] == "verify_claim"


def test_tool_input_repair_bounds_common_inventory_and_timeline_args() -> None:
    task_state = agent.TaskState(
        run_id="run-test",
        case_id="CASE-RD01",
        evidence_path="M:/evidence/base-rd-01-cdrive.E01",
        case_workspace="M:/cases/CASE-RD01",
        report_path=Path("report.md"),
        evidence_id="ev-test",
    )

    inventory = agent._repair_tool_input_from_task_state("filesystem_inventory", {}, task_state)
    timeline = agent._repair_tool_input_from_task_state(
        "build_timeline",
        {"image_path": "M:/evidence/base-rd-01-cdrive.E01", "max_records": 5000},
        task_state,
    )

    assert inventory["evidence_id"] == "ev-test"
    assert inventory["image_path"] == "M:/evidence/base-rd-01-cdrive.E01"
    assert inventory["partition_start_sector"] == 0
    assert inventory["recursive"] is False
    assert inventory["max_entries"] == 250
    assert timeline["evidence_id"] == "ev-test"
    assert timeline["source_path"] == "M:/evidence/base-rd-01-cdrive.E01"
    assert timeline["max_records"] == 5000
    assert "image_path" not in timeline


def test_non_report_model_text_is_not_written_as_final_report() -> None:
    task_state = agent.TaskState(
        run_id="run-test",
        case_id="CASE-RD01",
        evidence_path="M:/evidence/base-rd-01-cdrive.E01",
        case_workspace="M:/cases/CASE-RD01",
        report_path=Path("report.md"),
    )

    assert agent._looks_like_final_report("I'll begin by opening the case.") is False
    fallback = agent._fallback_final_report(task_state)

    assert "Confirmed Findings" in fallback
    assert "Needs Human Review" in fallback
    assert "I'll begin" not in fallback


def test_final_limit_message_distinguishes_iterations_from_tool_budget() -> None:
    orchestration = agent.OrchestrationState(max_iterations=4, tool_call_budget=60)
    orchestration.iteration = 4
    orchestration.tool_calls = 3

    message = agent._build_final_report_limit_message(orchestration)

    assert "max_iterations reached" in message
    assert "Tool calls used: 3/60" in message
    assert "Do not claim the tool-call budget was exhausted" in message


def test_safe_execution_log_uses_fastmcp_request_wrapper() -> None:
    class FakeSession:
        def __init__(self) -> None:
            self.calls: list[tuple[str, dict[str, object]]] = []

        async def call_tool(self, name: str, *, arguments: dict[str, object], read_timeout_seconds: object) -> None:
            self.calls.append((name, arguments))

    async def run_check() -> FakeSession:
        session = FakeSession()
        task_state = agent.TaskState(
            run_id="run-test",
            case_id="CASE-RD01",
            evidence_path="M:/evidence/base-rd-01-cdrive.E01",
            case_workspace="M:/cases/CASE-RD01",
            report_path=Path("report.md"),
            evidence_id="ev-test",
        )
        await agent._safe_write_execution_log(
            session,  # type: ignore[arg-type]
            task_state,
            agent.OrchestrationState(),
            step_number=1,
            tool_name="case_open_readonly",
            arguments={"request": {"case_id": "CASE-RD01"}},
            parser_status="ok",
            agent_intent="Agent called case_open_readonly",
        )
        return session

    session = asyncio.run(run_check())

    assert session.calls
    name, arguments = session.calls[0]
    assert name == "write_execution_log"
    assert set(arguments) == {"request"}
    assert arguments["request"]["tool_name"] == "case_open_readonly"  # type: ignore[index]


def test_unknown_model_tool_call_is_rejected_before_mcp_session() -> None:
    class FakeToolUse:
        id = "bad-tool-call"
        name = "None"
        input = {"request": {"evidence_id": "ev-test"}}

    class FakeSession:
        def __init__(self) -> None:
            self.called = False

        async def call_tool(self, *args: object, **kwargs: object) -> None:
            self.called = True

    async def run_check() -> tuple[dict[str, object], FakeSession, agent.TaskState]:
        session = FakeSession()
        task_state = agent.TaskState(
            run_id="run-test",
            case_id="CASE-RD01",
            evidence_path="M:/evidence/base-rd-01-cdrive.E01",
            case_workspace="M:/cases/CASE-RD01",
            report_path=Path("report.md"),
            evidence_id="ev-test",
        )
        result = await agent._call_mcp_tool(
            session,  # type: ignore[arg-type]
            task_state,
            agent.OrchestrationState(),
            tool_use=FakeToolUse(),
            valid_tool_names={"case_open_readonly", "list_partitions"},
        )
        return result, session, task_state

    result, session, task_state = asyncio.run(run_check())

    assert result["is_error"] is True
    assert "Unknown MCP tool requested by model: None" in str(result["content"])
    assert session.called is False
    assert task_state.local_events[-1]["event"] == "unknown_tool_rejected"


def test_large_tool_payload_is_compacted_before_model_context() -> None:
    payload = {
        "parser_status": "ok",
        "records": [
            {"record_id": f"rec-{index}", "path": "Windows/System32/config/SYSTEM", "description": "x" * 3000}
            for index in range(100)
        ],
    }

    compacted = agent._compact_tool_payload_for_model(payload)
    serialized = agent.json.dumps(compacted, ensure_ascii=True)

    assert compacted["model_context_truncated"] is True
    assert len(compacted["records"]) == agent.MAX_TOOL_RESULT_LIST_ITEMS
    assert compacted["records_original_count"] == 100
    assert len(compacted["records"][0]["description"]) < 2200
    assert len(serialized) < 80_000


def test_report_markdown_normalizer_separates_model_smashed_headings() -> None:
    normalized = agent._normalize_report_markdown("## Scope- Case\n\n## Unsupported Dropped- none")

    assert "## Scope\n- Case" in normalized
    assert "## Unsupported Dropped\n- none" in normalized
    assert normalized.endswith("\n")


def test_prompt_requires_verified_claims_and_tool_sequence() -> None:
    source = PROMPTS_PATH.read_text(encoding="utf-8")

    for expected in (
        "Senior DFIR Analyst",
        "case_open_readonly",
        "list_partitions",
        "filesystem_inventory",
        "build_timeline",
        "extract_registry_persistence",
        "extract_event_records",
        "verify_claim",
        "write_execution_log",
        "The runtime automatically logs every MCP tool call.",
        "Confirmed",
        "Unsupported dropped",
        "Correction Ledger",
        "Corrected",
        "Needs human review",
    ):
        assert expected in source


def test_prompt_requires_visible_disposition_for_every_candidate_claim() -> None:
    source = PROMPTS_PATH.read_text(encoding="utf-8")

    for expected in (
        "every candidate claim is confirmed, inferred, dropped, corrected, or marked needs human review",
        "A finding may be labeled Confirmed only if verify_claim returns confirmed with linked supporting evidence.",
        "Unsupported claims must be dropped from the main findings and listed under Unsupported dropped and Correction Ledger.",
        "Do not omit a rejected candidate claim",
        "parser failure, unsupported claim, evidence conflict, missing artifact family, ambiguous timestamp, and unsafe request",
    ):
        assert expected in source
