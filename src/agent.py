from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import uuid4

from anthropic import AsyncAnthropic
from mcp import ClientSession
import mcp.client.stdio as stdio_client

try:
    from .prompts import SYSTEM_PROMPT, build_initial_user_prompt
except ImportError:
    from prompts import SYSTEM_PROMPT, build_initial_user_prompt


MAX_ITERATIONS = 20
GLOBAL_TIMEOUT_SECONDS = 1800
TOOL_TIMEOUT_SECONDS = 300
TOOL_CALL_BUDGET = 60
TOKEN_BUDGET = 120_000
MAX_OUTPUT_TOKENS = 4000
DEFAULT_MODEL = "claude-sonnet-4-5-20250929"
DEFAULT_MCP_SERVER_COMMAND = "python"
LOCAL_ENV_FILE = ".env.local"
DEFAULT_AGENT_PROVIDER = "auto"
OPENAI_COMPATIBLE_TIMEOUT_SECONDS = 120
API_PROVIDER_ENV = {
    "anthropic": {
        "env_var": "ANTHROPIC_API_KEY",
        "model_env_var": "ANTHROPIC_MODEL",
        "runtime_status": "implemented",
        "default_model": DEFAULT_MODEL,
        "purpose": "Primary runtime for the current autonomous MCP agent.",
    },
    "google_gemini": {
        "env_var": "GOOGLE_API_KEY",
        "model_env_var": "GEMINI_MODEL",
        "runtime_status": "candidate_adapter_required",
        "default_model": "gemini-3.1-flash",
        "purpose": "Low-cost or free-tier candidate if a Gemini adapter is added later.",
    },
    "groq": {
        "env_var": "GROQ_API_KEY",
        "model_env_var": "GROQ_MODEL",
        "runtime_status": "implemented",
        "default_model": "llama-3.3-70b-versatile",
        "base_url": "https://api.groq.com/openai/v1/chat/completions",
        "purpose": "Free-plan OpenAI-compatible runtime for the autonomous MCP agent.",
    },
    "openrouter": {
        "env_var": "OPENROUTER_API_KEY",
        "model_env_var": "OPENROUTER_MODEL",
        "runtime_status": "implemented",
        "default_model": "openrouter/free",
        "base_url": "https://openrouter.ai/api/v1/chat/completions",
        "purpose": "Free or low-cost OpenAI-compatible routing runtime for the autonomous MCP agent.",
    },
    "openai": {
        "env_var": "OPENAI_API_KEY",
        "model_env_var": "OPENAI_MODEL",
        "runtime_status": "candidate_adapter_required",
        "default_model": "gpt-5-mini",
        "purpose": "Optional Responses API runtime candidate if an OpenAI adapter is added later.",
    },
}
IMPLEMENTED_PROVIDER_PRIORITY = ("openrouter", "groq", "anthropic")


def _env_value_is_header_safe(value: str | None) -> bool:
    if not value:
        return False
    try:
        value.encode("ascii")
    except UnicodeEncodeError:
        return False
    return not any(character.isspace() for character in value)


class AgentRuntimeError(RuntimeError):
    """Raised for agent configuration and runtime boundary failures."""


class ToolExecutionError(RuntimeError):
    """Raised when a tool budget or execution boundary is violated."""


@dataclass(slots=True)
class OrchestrationState:
    max_iterations: int = MAX_ITERATIONS
    global_timeout_seconds: int = GLOBAL_TIMEOUT_SECONDS
    tool_call_budget: int = TOOL_CALL_BUDGET
    token_budget: int = TOKEN_BUDGET
    iteration: int = 0
    tool_calls: int = 0
    token_usage: dict[str, int] = field(default_factory=lambda: {"input_tokens": 0, "output_tokens": 0})


@dataclass(slots=True)
class TaskState:
    run_id: str
    case_id: str
    evidence_path: str
    case_workspace: str
    report_path: Path
    evidence_id: str | None = None
    last_text: str = ""
    local_events: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class RuntimeSelection:
    provider: str
    api_key: str
    model: str


@dataclass(slots=True)
class NormalizedToolUse:
    id: str
    name: str
    input: dict[str, Any]
    type: str = "tool_use"


@dataclass(slots=True)
class NormalizedUsage:
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass(slots=True)
class NormalizedResponse:
    content: list[Any]
    usage: NormalizedUsage = field(default_factory=NormalizedUsage)


def _json_default(value: Any) -> str:
    return str(value)


def _block_to_dict(block: Any) -> dict[str, Any]:
    if hasattr(block, "model_dump"):
        return block.model_dump(mode="json", exclude_none=True)
    if isinstance(block, dict):
        return block
    return {"type": getattr(block, "type", "text"), "text": str(block)}


def _result_to_payload(result: Any) -> dict[str, Any]:
    if hasattr(result, "model_dump"):
        return result.model_dump(mode="json", exclude_none=True)
    if isinstance(result, dict):
        return result
    return {"result": str(result)}


def _extract_text(content_blocks: list[Any]) -> str:
    parts: list[str] = []
    for block in content_blocks:
        if getattr(block, "type", None) == "text":
            parts.append(getattr(block, "text", ""))
        elif isinstance(block, dict) and block.get("type") == "text":
            parts.append(str(block.get("text", "")))
    return "\n".join(part for part in parts if part).strip()


def _extract_tool_uses(content_blocks: list[Any]) -> list[Any]:
    return [
        block
        for block in content_blocks
        if getattr(block, "type", None) == "tool_use" or (isinstance(block, dict) and block.get("type") == "tool_use")
    ]


def _extract_evidence_id(payload: dict[str, Any]) -> str | None:
    for key in ("structuredContent", "structured_content", "result"):
        value = payload.get(key)
        if isinstance(value, dict) and isinstance(value.get("evidence_id"), str):
            return value["evidence_id"]
    if isinstance(payload.get("evidence_id"), str):
        return payload["evidence_id"]
    return None


def _usage_dict(response: Any) -> dict[str, int]:
    usage = getattr(response, "usage", None)
    if usage is None:
        return {}
    return {
        "input_tokens": int(getattr(usage, "input_tokens", 0) or 0),
        "output_tokens": int(getattr(usage, "output_tokens", 0) or 0),
    }


def _anthropic_tools_from_mcp(tools_result: Any) -> list[dict[str, Any]]:
    tools: list[dict[str, Any]] = []
    for tool in getattr(tools_result, "tools", []):
        schema = getattr(tool, "inputSchema", None) or getattr(tool, "input_schema", None) or {"type": "object"}
        tools.append(
            {
                "name": tool.name,
                "description": tool.description or f"MCP tool {tool.name}",
                "input_schema": schema,
            }
        )
    return tools


def _openai_tools_from_mcp(tools_result: Any) -> list[dict[str, Any]]:
    tools: list[dict[str, Any]] = []
    for tool in getattr(tools_result, "tools", []):
        schema = getattr(tool, "inputSchema", None) or getattr(tool, "input_schema", None) or {"type": "object"}
        tools.append(
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or f"MCP tool {tool.name}",
                    "parameters": schema,
                },
            }
        )
    return tools


def _provider_is_implemented(provider: str) -> bool:
    metadata = API_PROVIDER_ENV.get(provider)
    return bool(metadata and metadata["runtime_status"] == "implemented")


def select_runtime_provider(provider: str | None = None, model: str | None = None) -> RuntimeSelection:
    load_local_env_file()
    requested = (provider or os.environ.get("FIND_EVIL_AGENT_PROVIDER") or DEFAULT_AGENT_PROVIDER).strip().lower()
    if requested in {"", "default"}:
        requested = DEFAULT_AGENT_PROVIDER
    candidates = IMPLEMENTED_PROVIDER_PRIORITY if requested == "auto" else (requested,)

    for candidate in candidates:
        if candidate not in API_PROVIDER_ENV:
            raise AgentRuntimeError(f"Unsupported AI provider: {candidate}")
        if not _provider_is_implemented(candidate):
            raise AgentRuntimeError(f"AI provider is not implemented yet: {candidate}")
        metadata = API_PROVIDER_ENV[candidate]
        env_var = metadata["env_var"]
        api_key = os.environ.get(env_var)
        if _env_value_is_header_safe(api_key):
            selected_model = model or os.environ.get(metadata["model_env_var"]) or metadata["default_model"]
            return RuntimeSelection(provider=candidate, api_key=str(api_key), model=selected_model)
        if requested != "auto":
            raise AgentRuntimeError(f"{env_var} is missing or not ASCII/header-safe")

    needed = ", ".join(API_PROVIDER_ENV[item]["env_var"] for item in IMPLEMENTED_PROVIDER_PRIORITY)
    raise AgentRuntimeError(f"No implemented AI provider is ready. Configure one valid key: {needed}")


def _api_headers(provider: str, api_key: str) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if provider == "openrouter":
        headers["HTTP-Referer"] = "https://github.com/teamdfir/protocol-sift"
        headers["X-Title"] = "Find Evil CaseProof Analyst"
    return headers


def _to_openai_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    converted: list[dict[str, Any]] = []
    for message in messages:
        role = message["role"]
        content = message.get("content")
        if role == "assistant" and isinstance(content, list):
            text_parts: list[str] = []
            tool_calls: list[dict[str, Any]] = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = str(block.get("text", "")).strip()
                    if text:
                        text_parts.append(text)
                elif isinstance(block, dict) and block.get("type") == "tool_use":
                    tool_calls.append(
                        {
                            "id": str(block.get("id")),
                            "type": "function",
                            "function": {
                                "name": str(block.get("name")),
                                "arguments": json.dumps(block.get("input") or {}, ensure_ascii=True),
                            },
                        }
                    )
            assistant_message: dict[str, Any] = {"role": "assistant", "content": "\n".join(text_parts) or None}
            if tool_calls:
                assistant_message["tool_calls"] = tool_calls
            converted.append(assistant_message)
        elif role == "user" and isinstance(content, list) and all(
            isinstance(item, dict) and item.get("type") == "tool_result" for item in content
        ):
            for item in content:
                converted.append(
                    {
                        "role": "tool",
                        "tool_call_id": str(item["tool_use_id"]),
                        "content": str(item.get("content", "")),
                    }
                )
        elif isinstance(content, str):
            converted.append({"role": role, "content": content})
        else:
            converted.append({"role": role, "content": json.dumps(content, ensure_ascii=True, default=_json_default)})
    return converted


def _parse_tool_arguments(raw_arguments: Any) -> dict[str, Any]:
    if isinstance(raw_arguments, dict):
        return raw_arguments
    if raw_arguments in (None, ""):
        return {}
    try:
        parsed = json.loads(str(raw_arguments))
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _repair_tool_input_from_task_state(tool_name: str, tool_input: dict[str, Any], task_state: TaskState) -> dict[str, Any]:
    repaired = dict(tool_input) if isinstance(tool_input, dict) else {}
    if tool_name == "case_open_readonly":
        repaired.setdefault("case_id", task_state.case_id)
        repaired.setdefault("evidence_path", task_state.evidence_path)
        repaired.setdefault("case_workspace", task_state.case_workspace)
        return repaired

    if task_state.evidence_id:
        repaired.setdefault("evidence_id", task_state.evidence_id)
    if tool_name in {
        "list_partitions",
        "filesystem_inventory",
        "build_timeline",
        "extract_registry_persistence",
        "extract_event_records",
    }:
        repaired.setdefault("image_path", task_state.evidence_path)
    return repaired


def _fallback_final_report(task_state: TaskState) -> str:
    evidence_line = (
        f"- Evidence ID: {task_state.evidence_id}" if task_state.evidence_id else "- Evidence ID: unavailable; case open did not complete."
    )
    return "\n".join(
        [
            "# FIND EVIL Disk Triage Report",
            "",
            "## Scope",
            f"- Case ID: {task_state.case_id}",
            f"- Evidence: {task_state.evidence_path}",
            f"- Workspace: {task_state.case_workspace}",
            evidence_line,
            "",
            "## Confirmed Findings",
            "- No confirmed findings. The autonomous loop stopped before any claim was verified.",
            "",
            "## Inferred Findings",
            "- No inferred findings. The available context did not support an evidence-linked inference.",
            "",
            "## Unsupported Dropped",
            "- Any unverified analytical statements are dropped from confirmed findings.",
            "",
            "## Correction Ledger",
            "- Final report generation used the deterministic fallback because the selected model did not return usable final text.",
            "",
            "## Needs Human Review",
            "- Review the execution log and rerun with a higher iteration budget or a stronger tool-calling model before using this as an investigation result.",
            "",
            "## Audit Trail Summary",
            "- The original evidence path was not modified by this fallback report.",
        ]
    )


def _looks_like_final_report(text: str) -> bool:
    lowered = text.lower()
    return all(
        section in lowered
        for section in (
            "confirmed findings",
            "inferred findings",
            "unsupported dropped",
            "correction ledger",
            "needs human review",
            "audit trail",
        )
    )


def _normalize_report_markdown(text: str) -> str:
    normalized = text.replace("\r\n", "\n").strip()
    for heading in (
        "## Scope",
        "## Confirmed Findings",
        "## Inferred Findings",
        "## Unsupported Dropped",
        "## Correction Ledger",
        "## Needs Human Review",
        "## Audit Trail Summary",
    ):
        normalized = normalized.replace(f"{heading}-", f"{heading}\n-")
        normalized = normalized.replace(f"{heading}*", f"{heading}\n*")
    return normalized + "\n"


def _openai_compatible_request(
    *,
    provider: str,
    api_key: str,
    model: str,
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    metadata = API_PROVIDER_ENV[provider]
    body: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_tokens": MAX_OUTPUT_TOKENS,
    }
    if tools:
        body["tools"] = tools
        body["tool_choice"] = "auto"

    request = urllib.request.Request(
        str(metadata["base_url"]),
        data=json.dumps(body, ensure_ascii=True).encode("utf-8"),
        headers=_api_headers(provider, api_key),
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=OPENAI_COMPATIBLE_TIMEOUT_SECONDS) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        raise AgentRuntimeError(f"{provider} API request failed with HTTP {exc.code}: {body_text[:500]}") from exc
    except urllib.error.URLError as exc:
        raise AgentRuntimeError(f"{provider} API request failed: {exc.reason}") from exc


async def _openai_compatible_create(
    *,
    provider: str,
    api_key: str,
    model: str,
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None = None,
) -> NormalizedResponse:
    payload = await asyncio.to_thread(
        _openai_compatible_request,
        provider=provider,
        api_key=api_key,
        model=model,
        messages=messages,
        tools=tools,
    )
    choices = payload.get("choices") or []
    if not choices:
        raise AgentRuntimeError(f"{provider} API returned no choices")
    message = choices[0].get("message") or {}
    blocks: list[Any] = []
    content = message.get("content")
    if isinstance(content, str) and content.strip():
        blocks.append({"type": "text", "text": content})
    for tool_call in message.get("tool_calls") or []:
        function = tool_call.get("function") or {}
        name = function.get("name")
        if not name:
            continue
        blocks.append(
            NormalizedToolUse(
                id=str(tool_call.get("id") or f"tool-{uuid4().hex[:12]}"),
                name=str(name),
                input=_parse_tool_arguments(function.get("arguments")),
            )
        )
    usage = payload.get("usage") or {}
    return NormalizedResponse(
        content=blocks,
        usage=NormalizedUsage(
            input_tokens=int(usage.get("prompt_tokens", 0) or 0),
            output_tokens=int(usage.get("completion_tokens", 0) or 0),
        ),
    )


def load_local_env_file(path: Path | None = None) -> None:
    """Load simple KEY=VALUE pairs from .env.local without overriding the process env."""
    env_path = path or Path(LOCAL_ENV_FILE)
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value and key not in os.environ:
            os.environ[key] = value


def build_api_readiness_report() -> dict[str, Any]:
    """Return API-provider readiness without exposing secret values."""
    load_local_env_file()
    providers: list[dict[str, Any]] = []
    for provider, metadata in API_PROVIDER_ENV.items():
        env_var = metadata["env_var"]
        model_env_var = metadata["model_env_var"]
        value = os.environ.get(env_var)
        configured = bool(value)
        valid = _env_value_is_header_safe(value)
        configured_model = os.environ.get(model_env_var) or metadata["default_model"]
        providers.append(
            {
                "provider": provider,
                "env_var": env_var,
                "configured": configured,
                "valid": valid,
                "model_env_var": model_env_var,
                "selected_model": configured_model,
                "runtime_status": metadata["runtime_status"],
                "purpose": metadata["purpose"],
            }
        )

    try:
        selection = select_runtime_provider()
        current_runtime = selection.provider
        current_ready = True
        required_key = API_PROVIDER_ENV[selection.provider]["env_var"]
        recommendation = f"Ready to run with {selection.provider}."
    except AgentRuntimeError as exc:
        requested = (os.environ.get("FIND_EVIL_AGENT_PROVIDER") or DEFAULT_AGENT_PROVIDER).strip().lower()
        current_runtime = "none" if requested == "auto" else requested
        current_ready = False
        required_key = ", ".join(API_PROVIDER_ENV[item]["env_var"] for item in IMPLEMENTED_PROVIDER_PRIORITY)
        recommendation = str(exc)
    return {
        "current_runtime": current_runtime,
        "current_runtime_ready": current_ready,
        "required_for_current_agent": required_key,
        "mcp_server_command": os.environ.get("MCP_SERVER_COMMAND", DEFAULT_MCP_SERVER_COMMAND),
        "providers": providers,
        "recommendation": recommendation,
    }


async def _safe_write_execution_log(
    session: ClientSession,
    task_state: TaskState,
    orchestration: OrchestrationState,
    *,
    step_number: int,
    tool_name: str,
    arguments: dict[str, Any],
    parser_status: str,
    agent_intent: str,
    output_reference: str | None = None,
    correction_reason: str | None = None,
) -> None:
    if not task_state.evidence_id or tool_name == "write_execution_log":
        return
    payload = {
        "run_id": task_state.run_id,
        "case_id": task_state.case_id,
        "step_number": max(step_number, 1),
        "agent_intent": agent_intent,
        "tool_name": tool_name,
        "arguments": arguments,
        "parser_status": parser_status,
        "evidence_id": task_state.evidence_id,
        "output_reference": output_reference,
        "token_usage": orchestration.token_usage,
        "correction_reason": correction_reason,
    }
    try:
        await session.call_tool(
            "write_execution_log",
            arguments={"request": payload},
            read_timeout_seconds=None,
        )
    except Exception as exc:
        task_state.local_events.append(
            {
                "event": "write_execution_log_failed",
                "tool_name": tool_name,
                "error": str(exc),
            }
        )


async def _call_mcp_tool(
    session: ClientSession,
    task_state: TaskState,
    orchestration: OrchestrationState,
    *,
    tool_use: Any,
) -> dict[str, Any]:
    tool_name = tool_use.name
    raw_tool_input = tool_use.input or {}
    tool_input = raw_tool_input.get("request", raw_tool_input) if isinstance(raw_tool_input, dict) else raw_tool_input
    tool_input = _repair_tool_input_from_task_state(tool_name, tool_input, task_state)
    call_arguments = tool_input if "request" in tool_input else {"request": tool_input}
    orchestration.tool_calls += 1
    if orchestration.tool_calls > orchestration.tool_call_budget:
        raise ToolExecutionError("Tool call budget exhausted")

    try:
        result = await session.call_tool(
            tool_name,
            arguments=call_arguments,
            read_timeout_seconds=None,
        )
        payload = _result_to_payload(result)
        is_error = bool(payload.get("isError") or payload.get("is_error"))
        evidence_id = _extract_evidence_id(payload)
        if evidence_id:
            task_state.evidence_id = evidence_id
        parser_status = "failed" if is_error else "ok"
        await _safe_write_execution_log(
            session,
            task_state,
            orchestration,
            step_number=orchestration.tool_calls,
            tool_name=tool_name,
            arguments=call_arguments,
            parser_status=parser_status,
            agent_intent=f"Agent called {tool_name}",
            output_reference=tool_use.id,
            correction_reason="MCP tool returned error" if is_error else None,
        )
        return {
            "type": "tool_result",
            "tool_use_id": tool_use.id,
            "content": json.dumps(payload, ensure_ascii=True, default=_json_default),
            "is_error": is_error,
        }
    except Exception as exc:
        error_text = f"{tool_name} failed: {exc}"
        await _safe_write_execution_log(
            session,
            task_state,
            orchestration,
            step_number=orchestration.tool_calls,
            tool_name=tool_name,
            arguments=call_arguments,
            parser_status="failed",
            agent_intent=f"Agent attempted {tool_name}",
            output_reference=tool_use.id,
            correction_reason=error_text,
        )
        return {
            "type": "tool_result",
            "tool_use_id": tool_use.id,
            "content": error_text,
            "is_error": True,
        }


async def _create_final_report_without_tools(
    *,
    runtime: RuntimeSelection,
    client: AsyncAnthropic | None,
    messages: list[dict[str, Any]],
    task_state: TaskState,
) -> str:
    final_messages = [
        *messages,
        {
            "role": "user",
            "content": (
                "Hard execution limit reached. Produce the final report now using only "
                "verified or explicitly labeled evidence already present in context. "
                "Do not call tools."
            ),
        },
    ]
    if runtime.provider == "anthropic":
        if client is None:
            raise AgentRuntimeError("Anthropic client is not initialized")
        response = await client.messages.create(
            model=runtime.model,
            max_tokens=MAX_OUTPUT_TOKENS,
            system=SYSTEM_PROMPT,
            messages=final_messages,
        )
    else:
        response = await _openai_compatible_create(
            provider=runtime.provider,
            api_key=runtime.api_key,
            model=runtime.model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *_to_openai_messages(final_messages)],
    )
    text = _extract_text(list(response.content))
    if not text or not _looks_like_final_report(text):
        text = _fallback_final_report(task_state)
    return text


async def run_agent(
    *,
    case_id: str,
    evidence_path: str,
    case_workspace: str,
    report_path: Path,
    provider: str | None = None,
    model: str | None,
    max_iterations: int = MAX_ITERATIONS,
) -> Path:
    runtime = select_runtime_provider(provider=provider, model=model)

    orchestration = OrchestrationState(max_iterations=max_iterations)
    task_state = TaskState(
        run_id=f"run-{uuid4().hex[:16]}",
        case_id=case_id,
        evidence_path=evidence_path,
        case_workspace=case_workspace,
        report_path=report_path,
    )
    messages: list[dict[str, Any]] = [
        {
            "role": "user",
            "content": build_initial_user_prompt(
                case_id=case_id,
                evidence_path=evidence_path,
                case_workspace=case_workspace,
                max_iterations=max_iterations,
                tool_call_budget=orchestration.tool_call_budget,
            ),
        }
    ]
    client = AsyncAnthropic(api_key=runtime.api_key) if runtime.provider == "anthropic" else None

    mcp_server_command = os.environ.get("MCP_SERVER_COMMAND", DEFAULT_MCP_SERVER_COMMAND)
    server_parameters = stdio_client.StdioServerParameters(command=mcp_server_command, args=["-m", "src.server"])
    async with stdio_client.stdio_client(server_parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            mcp_tools = await session.list_tools()
            tools = _anthropic_tools_from_mcp(mcp_tools) if runtime.provider == "anthropic" else _openai_tools_from_mcp(mcp_tools)

            async with asyncio.timeout(orchestration.global_timeout_seconds):
                iteration = 0
                while iteration < max_iterations:
                    orchestration.iteration = iteration + 1
                    if runtime.provider == "anthropic":
                        if client is None:
                            raise AgentRuntimeError("Anthropic client is not initialized")
                        response = await client.messages.create(
                            model=runtime.model,
                            max_tokens=MAX_OUTPUT_TOKENS,
                            system=SYSTEM_PROMPT,
                            messages=messages,
                            tools=tools,
                        )
                    else:
                        response = await _openai_compatible_create(
                            provider=runtime.provider,
                            api_key=runtime.api_key,
                            model=runtime.model,
                            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *_to_openai_messages(messages)],
                            tools=tools,
                        )
                    usage = _usage_dict(response)
                    for key, value in usage.items():
                        orchestration.token_usage[key] = orchestration.token_usage.get(key, 0) + value
                    if sum(orchestration.token_usage.values()) > orchestration.token_budget:
                        task_state.local_events.append({"event": "token_budget_exhausted"})
                        break

                    content_blocks = list(response.content)
                    assistant_text = _extract_text(content_blocks)
                    if assistant_text:
                        task_state.last_text = assistant_text
                    messages.append({"role": "assistant", "content": [_block_to_dict(block) for block in content_blocks]})

                    tool_uses = _extract_tool_uses(content_blocks)
                    if not tool_uses:
                        final_report = assistant_text if _looks_like_final_report(assistant_text) else _fallback_final_report(task_state)
                        report_path.parent.mkdir(parents=True, exist_ok=True)
                        report_path.write_text(_normalize_report_markdown(final_report), encoding="utf-8")
                        return report_path

                    tool_results: list[dict[str, Any]] = []
                    for tool_use in tool_uses:
                        tool_result = await _call_mcp_tool(
                            session,
                            task_state,
                            orchestration,
                            tool_use=tool_use,
                        )
                        tool_results.append(tool_result)
                    messages.append({"role": "user", "content": tool_results})
                    iteration += 1

            final_report = await _create_final_report_without_tools(
                runtime=runtime,
                client=client,
                messages=messages,
                task_state=task_state,
            )
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(_normalize_report_markdown(final_report), encoding="utf-8")
            return report_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run autonomous FIND EVIL disk triage agent.")
    parser.add_argument("--check-api", action="store_true", help="Print API readiness without running the agent.")
    parser.add_argument("--evidence-path", required=False, help="Path to the forensic disk image.")
    parser.add_argument("--case-id", required=False, help="Case identifier for logs and report.")
    parser.add_argument("--case-workspace", default=None, help="Workspace for generated analysis artifacts.")
    parser.add_argument("--report-path", default="report.md", help="Final report path.")
    parser.add_argument(
        "--provider",
        default=None,
        choices=["auto", "anthropic", "groq", "openrouter"],
        help="AI runtime provider. Defaults to FIND_EVIL_AGENT_PROVIDER or auto.",
    )
    parser.add_argument("--model", default=None, help="Model override for the selected provider.")
    parser.add_argument("--max-iterations", type=int, default=MAX_ITERATIONS, help="Hard execution loop limit.")
    args = parser.parse_args(argv)
    if not args.check_api:
        missing = [name for name in ("evidence_path", "case_id") if not getattr(args, name)]
        if missing:
            parser.error("--evidence-path and --case-id are required unless --check-api is used")
    return args


async def async_main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.check_api:
        print(json.dumps(build_api_readiness_report(), indent=2, ensure_ascii=True))
        return 0

    workspace = args.case_workspace or str(Path("cases") / args.case_id)
    report_path = Path(args.report_path).resolve(strict=False)
    try:
        written = await run_agent(
            case_id=args.case_id,
            evidence_path=args.evidence_path,
            case_workspace=workspace,
            report_path=report_path,
            provider=args.provider,
            model=args.model,
            max_iterations=args.max_iterations,
        )
    except asyncio.TimeoutError:
        print(f"Agent timed out after {GLOBAL_TIMEOUT_SECONDS} seconds", file=sys.stderr)
        return 2
    except AgentRuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"Agent failed: {exc}", file=sys.stderr)
        return 1

    print(f"Report written: {written}")
    return 0


def main() -> None:
    raise SystemExit(asyncio.run(async_main()))


if __name__ == "__main__":
    main()
