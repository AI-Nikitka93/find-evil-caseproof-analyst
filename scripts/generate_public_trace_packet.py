from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.output_package import public_safe_redact


PUBLIC_LOG_PATH = PROJECT_ROOT / "docs" / "public_real_execution_log_sample.jsonl"
PUBLIC_TRACE_PATH = PROJECT_ROOT / "docs" / "public_real_traceability_packet.md"
DEFAULT_CASE_WORKSPACE = PROJECT_ROOT / "cases" / "CASE-RD01"
REQUIRED_TOOLS = (
    "case_open_readonly",
    "list_partitions",
    "filesystem_inventory",
    "extract_registry_persistence",
    "extract_event_records",
    "verify_claim",
)
LOCAL_PATH_PATTERN = re.compile(r"(?i)(?:[A-Z]:\\|/home/|/Users/|C:\\Users\\)")
TOKEN_PATTERN = re.compile(
    r"(?i)(sk-[A-Za-z0-9_-]{8,}|sk-ant-[A-Za-z0-9_-]{8,}|gsk_[A-Za-z0-9_-]{8,}|github_pat_[A-Za-z0-9_]{8,}|ghp_[A-Za-z0-9]{8,}|Bearer\s+[A-Za-z0-9._-]{8,})"
)


def _public_path_label(path: Path, *, case_id: str) -> str:
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        if path.name == "agent_execution.jsonl":
            return f"cases/{case_id}/logs/agent_execution.jsonl"
        return path.name


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid_jsonl_line:{index}") from exc
        if not isinstance(payload, dict):
            raise ValueError(f"non_object_jsonl_line:{index}")
        records.append(payload)
    return records


def _sanitize_value(value: Any, case_id: str) -> Any:
    if isinstance(value, dict):
        return {key: _sanitize_value(item, case_id) for key, item in sorted(value.items())}
    if isinstance(value, list):
        return [_sanitize_value(item, case_id) for item in value]
    if not isinstance(value, str):
        return value

    cleaned = value
    cleaned = re.sub(r"(?i)[A-Z]:\\[^\"'\n\r]+\\evidence\\base-rd-01-cdrive\.E01", "evidence/base-rd-01-cdrive.E01", cleaned)
    cleaned = re.sub(r"(?i)[A-Z]:\\[^\"'\n\r]+\\cases\\[^\"'\n\r]+", f"cases/{case_id}", cleaned)
    return public_safe_redact(cleaned)


def sanitize_execution_records(records: list[dict[str, Any]], *, case_id: str) -> list[dict[str, Any]]:
    sanitized: list[dict[str, Any]] = []
    for record in records:
        sanitized.append(
            {
                "case_id": case_id,
                "run_id": _sanitize_value(record.get("run_id"), case_id),
                "step_number": record.get("step_number"),
                "timestamp_utc": record.get("timestamp_utc"),
                "agent_intent": _sanitize_value(record.get("agent_intent"), case_id),
                "tool_name": record.get("tool_name"),
                "parser_status": record.get("parser_status"),
                "arguments": _sanitize_value(record.get("arguments", {}), case_id),
                "evidence_id": "[RUN_EVIDENCE_ID]" if record.get("evidence_id") else None,
                "output_reference": _sanitize_value(record.get("output_reference"), case_id),
                "correction_reason": _sanitize_value(record.get("correction_reason"), case_id),
                "token_usage": record.get("token_usage"),
            }
        )
    return sanitized


def validate_public_text(text: str) -> list[str]:
    blockers: list[str] = []
    if LOCAL_PATH_PATTERN.search(text):
        blockers.append("local_path_leak")
    if TOKEN_PATTERN.search(text):
        blockers.append("token_like_value")
    return blockers


def select_latest_run(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    fallback_key = "[missing-run-id]"
    for record in records:
        grouped.setdefault(str(record.get("run_id") or fallback_key), []).append(record)
    if not grouped:
        return []
    _, selected = max(
        grouped.items(),
        key=lambda item: max(str(record.get("timestamp_utc") or "") for record in item[1]),
    )
    return sorted(selected, key=lambda record: int(record.get("step_number") or 0))


def validate_trace_records(records: list[dict[str, Any]]) -> list[str]:
    blockers: list[str] = []
    tools = [str(record.get("tool_name", "")) for record in records]
    for required in REQUIRED_TOOLS:
        if required not in tools:
            blockers.append(f"missing_tool:{required}")
    if not any(record.get("correction_reason") for record in records):
        blockers.append("missing_visible_correction_reason")
    for expected_step, record in enumerate(records, start=1):
        if record.get("step_number") != expected_step:
            blockers.append("non_sequential_steps")
            break
        if not record.get("timestamp_utc"):
            blockers.append("missing_timestamp")
        if not record.get("parser_status"):
            blockers.append("missing_parser_status")
    return sorted(set(blockers))


def render_trace_markdown(records: list[dict[str, Any]], *, case_id: str, source_log: Path) -> str:
    source_label = _public_path_label(source_log, case_id=case_id)
    rows = [
        "| Step | Tool | Parser | Output | Correction | Intent |",
        "|---:|---|---|---|---|---|",
    ]
    for record in records:
        correction = record.get("correction_reason") or ""
        rows.append(
            "| {step} | `{tool}` | `{parser}` | `{output}` | {correction} | {intent} |".format(
                step=record.get("step_number"),
                tool=record.get("tool_name"),
                parser=record.get("parser_status"),
                output=record.get("output_reference") or "",
                correction=correction or "None",
                intent=str(record.get("agent_intent", "")).replace("|", "/"),
            )
        )

    return "\n".join(
        [
            "# Public Real Traceability Packet",
            "",
            "Date: 2026-05-07",
            f"Case: `{case_id}`",
            "Source: redacted excerpt generated from the local real-run execution log.",
            "",
            "## Purpose",
            "",
            "This packet gives judges a public-safe view of the real CASE-RD01 tool",
            "sequence without publishing the ignored local `cases/` workspace or the",
            "private `evidence/` directory.",
            "",
            "It preserves the information needed for the FIND EVIL audit-trail",
            "requirement: step order, timestamp, tool name, parser status, output",
            "reference, token-usage field, and the visible self-correction reason.",
            "For deterministic backend-only steps, `token_usage` may be `null`;",
            "autonomous AI smoke logs carry model usage when the provider returns it.",
            "",
            "## Public Files",
            "",
            "- `docs/public_real_execution_log_sample.jsonl`: sanitized JSONL trace.",
            "- `docs/public_real_traceability_packet.md`: this reviewer walkthrough.",
            "",
            "## Sanitization",
            "",
            "- Local absolute paths are replaced with repository-relative public labels.",
            "- Original evidence bytes and raw case exports are not included.",
            "- API keys, bearer tokens, and local user or machine identifiers are blocked.",
            "- The per-run internal evidence identifier is replaced with `[RUN_EVIDENCE_ID]`.",
            "",
            "## Source Log",
            "",
            f"- Local source path: `{source_label}`",
            "- Public replacement path: `docs/public_real_execution_log_sample.jsonl`",
            "",
            "## Step Trace",
            "",
            *rows,
            "",
            "## Self-Correction Signal",
            "",
            "The final `verify_claim` step challenges the tempting claim",
            "`Confirmed compromise or persistence on RD01` and records the correction",
            "reason `Unsupported compromise claim dropped from confirmed findings.`",
            "That is the public demo moment: the system refuses to upgrade artifact",
            "presence and bounded event/registry content into a confirmed malicious finding",
            "without cross-artifact evidence.",
            "",
            "## Limits",
            "",
            "- This is a redacted execution-log excerpt, not the full local case workspace.",
            "- Registry Run-key, service content, and bounded event-log content are parsed",
            "  in this run; full timeline and deeper cross-artifact correlation remain future work.",
            "- The public log proves traceability for the bounded real run, not full",
            "  incident reconstruction.",
        ]
    )


def generate_public_trace_packet(
    *,
    case_workspace: Path = DEFAULT_CASE_WORKSPACE,
    public_log_path: Path = PUBLIC_LOG_PATH,
    public_trace_path: Path = PUBLIC_TRACE_PATH,
) -> dict[str, Any]:
    log_path = case_workspace / "logs" / "agent_execution.jsonl"
    if not log_path.is_file():
        raise FileNotFoundError(f"missing real execution log: {log_path}")

    case_id = case_workspace.name
    raw_records = _load_jsonl(log_path)
    selected_records = select_latest_run(raw_records)
    sanitized_records = sanitize_execution_records(selected_records, case_id=case_id)
    record_blockers = validate_trace_records(sanitized_records)

    public_log_text = "\n".join(json.dumps(record, ensure_ascii=True, sort_keys=True) for record in sanitized_records) + "\n"
    markdown = render_trace_markdown(sanitized_records, case_id=case_id, source_log=log_path)
    text_blockers = validate_public_text(public_log_text + "\n" + markdown)
    blockers = sorted(set([*record_blockers, *text_blockers]))

    public_log_path.parent.mkdir(parents=True, exist_ok=True)
    public_log_path.write_text(public_log_text, encoding="utf-8")
    public_trace_path.write_text(markdown, encoding="utf-8")

    return {
        "status": "ok" if not blockers else "blocked",
        "case_id": case_id,
        "source_log": _public_path_label(log_path, case_id=case_id),
        "public_log": _public_path_label(public_log_path, case_id=case_id),
        "public_trace": _public_path_label(public_trace_path, case_id=case_id),
        "records": len(sanitized_records),
        "blockers": blockers,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate public-safe real execution trace artifacts.")
    parser.add_argument("--case-workspace", type=Path, default=DEFAULT_CASE_WORKSPACE)
    parser.add_argument("--public-log-path", type=Path, default=PUBLIC_LOG_PATH)
    parser.add_argument("--public-trace-path", type=Path, default=PUBLIC_TRACE_PATH)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = generate_public_trace_packet(
        case_workspace=args.case_workspace,
        public_log_path=args.public_log_path,
        public_trace_path=args.public_trace_path,
    )
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=True))
    else:
        print(f"Public trace packet status: {result['status']}")
        print(f"Records: {result['records']}")
        print(f"Public log: {result['public_log']}")
        print(f"Public trace: {result['public_trace']}")
        if result["blockers"]:
            print("Blockers: " + ", ".join(result["blockers"]))
    if args.strict and result["status"] != "ok":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
