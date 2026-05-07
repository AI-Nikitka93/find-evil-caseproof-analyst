from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from pathlib import PureWindowsPath
from typing import Any, Literal
from uuid import uuid4

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from pydantic import BaseModel, ConfigDict, Field


mcp = FastMCP("Evidence-Locked Disk Triage MCP")


ParserStatus = Literal["not_started", "ok", "partial", "failed"]
HashStatus = Literal["not_checked", "matched", "mismatched", "unavailable"]
ClaimStatus = Literal["confirmed", "inferred", "unsupported", "needs_human_review"]
DEFAULT_TIMEOUT_SECONDS = int(os.getenv("FIND_EVIL_TOOL_TIMEOUT_SECONDS", "300"))
MAX_STDERR_CHARS = 2000
DEFAULT_WSL_DISTRO = "Ubuntu"
WSL_TOOL_ALIASES = {"rip.pl": "regripper"}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CommandPlan(StrictModel):
    tool: str
    arguments: list[str] = Field(default_factory=list)
    parser: str
    expected_output: str


class EvidenceReference(StrictModel):
    evidence_id: str
    source_path: str
    description: str
    artifact_path: str | None = None
    offset_bytes: int | None = Field(default=None, ge=0)
    timestamp_utc: datetime | None = None
    record_id: str | None = None


class CaseOpenReadonlyInput(StrictModel):
    case_id: str
    evidence_path: str
    case_workspace: str
    expected_sha256: str | None = None
    mount_required: bool = True
    analyst_notes: str | None = None


class CaseWorkspace(StrictModel):
    case_id: str
    workspace_path: str
    analysis_dir: str
    exports_dir: str
    reports_dir: str


class CaseOpenReadonlyOutput(StrictModel):
    evidence_id: str
    case_id: str
    evidence_path: str
    workspace: CaseWorkspace
    readonly_enforced: bool
    original_writable_exposed: bool
    hash_status: HashStatus
    parser_status: ParserStatus
    messages: list[str] = Field(default_factory=list)


class ListPartitionsInput(StrictModel):
    evidence_id: str
    image_path: str
    sector_size: int = Field(default=512, ge=1)
    include_unallocated: bool = True


class PartitionInfo(StrictModel):
    slot: str
    start_sector: int = Field(ge=0)
    end_sector: int | None = Field(default=None, ge=0)
    length_sectors: int | None = Field(default=None, ge=0)
    size_bytes: int | None = Field(default=None, ge=0)
    description: str
    filesystem_type: str | None = None
    is_allocated: bool


class ListPartitionsOutput(StrictModel):
    evidence_id: str
    parser_status: ParserStatus
    partitions: list[PartitionInfo] = Field(default_factory=list)
    selected_partition_start_sector: int | None = Field(default=None, ge=0)
    command_plan: CommandPlan


class FilesystemInventoryInput(StrictModel):
    evidence_id: str
    image_path: str
    partition_start_sector: int = Field(ge=0)
    root_inode: str | None = None
    recursive: bool = True
    include_deleted: bool = True
    path_filters: list[str] = Field(default_factory=list)
    max_entries: int = Field(default=5000, ge=1)


FileEntryType = Literal["file", "directory", "deleted", "unknown"]
InventorySourceTool = Literal["fls", "istat", "icat", "unknown"]


class FileMetadataRecord(StrictModel):
    record_id: str
    path: str
    entry_type: FileEntryType
    inode: str | None = None
    allocated: bool | None = None
    size_bytes: int | None = Field(default=None, ge=0)
    modified_utc: datetime | None = None
    accessed_utc: datetime | None = None
    changed_utc: datetime | None = None
    created_utc: datetime | None = None
    source_tool: InventorySourceTool = "fls"
    hash_md5: str | None = None
    hash_sha256: str | None = None


class FilesystemInventoryOutput(StrictModel):
    evidence_id: str
    parser_status: ParserStatus
    records: list[FileMetadataRecord] = Field(default_factory=list)
    truncated: bool
    command_plan: CommandPlan


TimelineMode = Literal["plaso_json_line", "plaso_json", "dynamic_csv", "bodyfile"]


class BuildTimelineInput(StrictModel):
    evidence_id: str
    source_path: str
    mode: TimelineMode = "plaso_json_line"
    parser_preset: str = "win_gen"
    timezone: str = "UTC"
    start_utc: datetime | None = None
    end_utc: datetime | None = None
    max_records: int = Field(default=10000, ge=1)


class TimelineRecord(StrictModel):
    record_id: str
    timestamp_utc: datetime
    source: str
    description: str
    source_long: str | None = None
    artifact_path: str | None = None
    parser: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)


class BuildTimelineOutput(StrictModel):
    evidence_id: str
    parser_status: ParserStatus
    timeline_path: str | None = None
    records: list[TimelineRecord] = Field(default_factory=list)
    truncated: bool
    command_plan: list[CommandPlan] = Field(default_factory=list)


RegistryPluginScope = Literal["run_keys", "services", "scheduled_tasks", "all_persistence"]
RegistryOutputMode = Literal["text", "tln"]
PersistenceType = Literal["run_key", "service", "scheduled_task", "startup_folder", "unknown"]
RegistrySourceTool = Literal["regripper", "plaso", "unknown"]


class ExtractRegistryPersistenceInput(StrictModel):
    evidence_id: str
    hive_paths: list[str] = Field(min_length=1)
    plugin_scope: RegistryPluginScope = "all_persistence"
    output_mode: RegistryOutputMode = "text"
    max_records: int = Field(default=1000, ge=1)


class RegistryPersistenceRecord(StrictModel):
    record_id: str
    hive_path: str
    registry_path: str
    persistence_type: PersistenceType
    value_name: str | None = None
    value_data: str | None = None
    last_write_utc: datetime | None = None
    source_tool: RegistrySourceTool = "regripper"
    evidence_refs: list[EvidenceReference] = Field(default_factory=list)


class ExtractRegistryPersistenceOutput(StrictModel):
    evidence_id: str
    parser_status: ParserStatus
    records: list[RegistryPersistenceRecord] = Field(default_factory=list)
    truncated: bool
    command_plan: CommandPlan


EventChannel = Literal["security", "system", "application", "powershell", "other"]


class ExtractEventRecordsInput(StrictModel):
    evidence_id: str
    event_log_paths: list[str] = Field(min_length=1)
    channels: list[EventChannel] = Field(default_factory=list)
    event_ids: list[int] = Field(default_factory=list)
    start_utc: datetime | None = None
    end_utc: datetime | None = None
    max_records: int = Field(default=2000, ge=1)


class EventRecord(StrictModel):
    record_id: str
    event_id: int = Field(ge=0)
    channel: EventChannel
    source_path: str
    timestamp_utc: datetime | None = None
    provider: str | None = None
    rendered_message: str | None = None
    fields: dict[str, Any] = Field(default_factory=dict)


class ExtractEventRecordsOutput(StrictModel):
    evidence_id: str
    parser_status: ParserStatus
    records: list[EventRecord] = Field(default_factory=list)
    truncated: bool
    command_plan: CommandPlan


RequiredConfidence = Literal["confirmed", "inferred"]


class VerifyClaimInput(StrictModel):
    claim_id: str
    claim_text: str
    required_confidence: RequiredConfidence = "confirmed"
    evidence_ids: list[str] = Field(default_factory=list)
    evidence_refs: list[EvidenceReference] = Field(default_factory=list)


class ClaimVerificationResult(StrictModel):
    claim_id: str
    status: ClaimStatus
    rationale: str
    supporting_evidence: list[EvidenceReference] = Field(default_factory=list)
    missing_evidence: list[str] = Field(default_factory=list)
    recommended_followup_tools: list[str] = Field(default_factory=list)


class VerifyClaimOutput(StrictModel):
    result: ClaimVerificationResult


class WriteExecutionLogInput(StrictModel):
    run_id: str
    case_id: str
    step_number: int = Field(ge=1)
    agent_intent: str
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    parser_status: ParserStatus
    evidence_id: str | None = None
    output_reference: str | None = None
    token_usage: dict[str, int] | None = None
    correction_reason: str | None = None


class ExecutionLogRecord(StrictModel):
    run_id: str
    case_id: str
    step_number: int
    timestamp_utc: datetime
    tool_name: str
    arguments: dict[str, Any]
    parser_status: ParserStatus
    agent_intent: str
    evidence_id: str | None = None
    output_reference: str | None = None
    token_usage: dict[str, int] | None = None
    correction_reason: str | None = None


class WriteExecutionLogOutput(StrictModel):
    appended: bool
    log_path: str
    record: ExecutionLogRecord


@dataclass(slots=True)
class CaseState:
    case_id: str
    evidence_id: str
    evidence_path: Path
    workspace_path: Path
    analysis_dir: Path
    exports_dir: Path
    reports_dir: Path
    logs_dir: Path


CASE_BY_EVIDENCE: dict[str, CaseState] = {}
CASE_BY_ID: dict[str, CaseState] = {}
EVIDENCE_INDEX: dict[str, list[EvidenceReference]] = {}


MMLS_ROW_RE = re.compile(
    r"^\s*\d{3}:\s+(?P<slot>\S+)\s+"
    r"(?P<start>\d+)\s+(?P<end>\d+)\s+(?P<length>\d+)\s+"
    r"(?P<size>\S+)\s+(?P<description>.+?)\s*$"
)
FLS_ROW_RE = re.compile(
    r"^\s*(?P<kind>[A-Za-z?]/[A-Za-z?])\s+"
    r"(?P<deleted>\*)?\s*(?P<inode>[^:]+):\s*(?P<path>.+?)\s*$"
)
EVENT_ID_RE = re.compile(r"\b(?:event[_\s-]*id|eventidentifier)\D+(?P<event_id>\d+)", re.IGNORECASE)


def _raise_tool_error(message: str) -> None:
    raise ToolError(message)


def _has_parent_segment(path_text: str) -> bool:
    normalized = path_text.replace("\\", "/")
    return any(part == ".." for part in normalized.split("/"))


def _resolve_input_path(path_text: str, *, must_exist: bool, label: str) -> Path:
    if not path_text or not path_text.strip():
        _raise_tool_error(f"{label} is required")
    if _has_parent_segment(path_text):
        _raise_tool_error(f"Path traversal rejected for {label}")

    path = Path(path_text).expanduser().resolve(strict=False)
    if must_exist and not path.exists():
        _raise_tool_error(f"{label} does not exist: {path}")
    return path


def _ensure_workspace_child(path: Path, workspace: Path, *, label: str) -> Path:
    resolved = path.resolve(strict=False)
    workspace_resolved = workspace.resolve(strict=False)
    if not _is_relative_to(resolved, workspace_resolved) and resolved != workspace_resolved:
        _raise_tool_error(f"{label} must stay inside case workspace")
    return resolved


def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        return path.resolve(strict=False).is_relative_to(base.resolve(strict=False))
    except ValueError:
        return False


def _workspace_file(state: CaseState, directory: Path, filename: str, *, label: str) -> Path:
    if _has_parent_segment(filename) or Path(filename).is_absolute():
        _raise_tool_error(f"Path traversal rejected for {label}")
    target = _ensure_workspace_child(directory / filename, state.workspace_path, label=label)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def _get_case_by_evidence(evidence_id: str) -> CaseState:
    state = CASE_BY_EVIDENCE.get(evidence_id)
    if state is None:
        _raise_tool_error(f"Unknown evidence_id: {evidence_id}")
    return state


def _get_case_for_log(case_id: str, evidence_id: str | None) -> CaseState:
    if evidence_id:
        return _get_case_by_evidence(evidence_id)
    state = CASE_BY_ID.get(case_id)
    if state is None:
        _raise_tool_error(f"Unknown case_id: {case_id}")
    return state


def _validate_registered_evidence(state: CaseState, path_text: str) -> Path:
    image_path = _resolve_input_path(path_text, must_exist=True, label="image_path")
    if image_path != state.evidence_path:
        _raise_tool_error("image_path must match registered read-only evidence")
    return image_path


def _tool_runtime() -> str:
    runtime = os.getenv("FIND_EVIL_TOOL_RUNTIME", "auto").strip().lower() or "auto"
    if runtime == "native":
        return "native"
    if runtime in {"auto", "wsl"} and os.name == "nt":
        return "wsl"
    return "native"


def _windows_path_to_wsl(path_text: str) -> str:
    match = re.match(r"^(?P<drive>[A-Za-z]):[\\/](?P<rest>.*)$", path_text)
    if not match:
        return path_text
    drive = match.group("drive").lower()
    rest = match.group("rest").replace("\\", "/")
    return f"/mnt/{drive}/{rest}"


def _translate_command_arg(arg: str, runtime: str) -> str:
    if runtime != "wsl":
        return arg
    if re.match(r"^[A-Za-z]:[\\/]", arg):
        return _windows_path_to_wsl(str(PureWindowsPath(arg)))
    return arg


def _execution_args(tool_name: str, args: list[str]) -> list[str]:
    runtime = _tool_runtime()
    if runtime != "wsl":
        return args
    distro = os.getenv("FIND_EVIL_WSL_DISTRO", DEFAULT_WSL_DISTRO).strip() or DEFAULT_WSL_DISTRO
    executable = WSL_TOOL_ALIASES.get(tool_name, tool_name)
    translated = [executable, *(_translate_command_arg(arg, runtime) for arg in args[1:])]
    return ["wsl", "-d", distro, "--", *translated]


def _run_command(tool_name: str, args: list[str], *, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> subprocess.CompletedProcess[str]:
    if not args or args[0] != tool_name:
        _raise_tool_error(f"Refusing non-allowlisted command for {tool_name}")
    execution_args = _execution_args(tool_name, args)
    try:
        result = subprocess.run(
            execution_args,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as exc:
        _raise_tool_error(f"{tool_name} is not available in configured runtime: {exc}")
    except subprocess.TimeoutExpired as exc:
        _raise_tool_error(f"{tool_name} timed out after {timeout} seconds: {exc}")

    if result.returncode != 0:
        details = (result.stderr or result.stdout or "").strip()[:MAX_STDERR_CHARS]
        _raise_tool_error(f"{tool_name} failed with exit code {result.returncode}: {details}")
    return result


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _new_evidence_id(case_id: str, evidence_path: Path) -> str:
    stat = evidence_path.stat()
    raw = f"{case_id}|{evidence_path}|{stat.st_size}|{stat.st_mtime_ns}|{uuid4()}"
    return "ev-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


def _parse_size(size_text: str, fallback_sectors: int | None = None, sector_size: int = 512) -> int | None:
    normalized = size_text.strip().replace(",", "")
    match = re.match(r"^(?P<number>\d+(?:\.\d+)?)(?P<unit>[KMGTP]?i?B?|B)?$", normalized, re.IGNORECASE)
    if match:
        value = float(match.group("number"))
        unit = (match.group("unit") or "B").upper()
        multipliers = {
            "B": 1,
            "": 1,
            "K": 1024,
            "KB": 1024,
            "KIB": 1024,
            "M": 1024**2,
            "MB": 1024**2,
            "MIB": 1024**2,
            "G": 1024**3,
            "GB": 1024**3,
            "GIB": 1024**3,
            "T": 1024**4,
            "TB": 1024**4,
            "TIB": 1024**4,
            "P": 1024**5,
            "PB": 1024**5,
            "PIB": 1024**5,
        }
        if unit in multipliers:
            return int(value * multipliers[unit])
    if fallback_sectors is not None:
        return fallback_sectors * sector_size
    return None


def _detect_filesystem(description: str) -> str | None:
    lowered = description.lower()
    for name in ("NTFS", "exFAT", "FAT32", "FAT16", "FAT", "EXT4", "EXT3", "EXT2", "HFS", "APFS", "UFS"):
        if name.lower() in lowered:
            return name
    return None


def _parse_mmls_output(output: str, sector_size: int = 512) -> list[PartitionInfo]:
    partitions: list[PartitionInfo] = []
    for line in output.splitlines():
        match = MMLS_ROW_RE.match(line)
        if not match:
            continue
        length = int(match.group("length"))
        description = match.group("description").strip()
        slot = match.group("slot")
        allocated = not (
            slot.startswith("-")
            or slot.lower() == "meta"
            or "unallocated" in description.lower()
            or "table" in description.lower()
        )
        partitions.append(
            PartitionInfo(
                slot=slot,
                start_sector=int(match.group("start")),
                end_sector=int(match.group("end")),
                length_sectors=length,
                size_bytes=_parse_size(match.group("size"), length, sector_size),
                description=description,
                filesystem_type=_detect_filesystem(description),
                is_allocated=allocated,
            )
        )
    if not partitions:
        _raise_tool_error("mmls output did not contain a parseable partition table")
    return partitions


def _partition_from_volume_fsstat(output: str, image_path: Path, sector_size: int = 512) -> PartitionInfo:
    fs_match = re.search(r"File System Type:\s*(?P<fs>[^\r\n]+)", output, re.IGNORECASE)
    total_sector_match = re.search(r"Total Sector Range:\s*0\s*-\s*(?P<end>\d+)", output, re.IGNORECASE)
    if not fs_match:
        _raise_tool_error("mmls returned no partitions and fsstat did not identify a filesystem")
    end_sector = int(total_sector_match.group("end")) if total_sector_match else None
    length_sectors = end_sector + 1 if end_sector is not None else None
    return PartitionInfo(
        slot="volume",
        start_sector=0,
        end_sector=end_sector,
        length_sectors=length_sectors,
        size_bytes=image_path.stat().st_size if image_path.exists() else None,
        description=f"Volume image filesystem: {fs_match.group('fs').strip()}",
        filesystem_type=fs_match.group("fs").strip().split()[0],
        is_allocated=True,
    )


def _entry_type(kind: str, allocated: bool) -> FileEntryType:
    if not allocated:
        return "deleted"
    first = kind.split("/", 1)[0].lower()
    if first == "d":
        return "directory"
    if first == "r" or first == "l" or first == "v":
        return "file"
    return "unknown"


def _parse_fls_output(output: str, *, evidence_id: str, max_entries: int) -> list[FileMetadataRecord]:
    records: list[FileMetadataRecord] = []
    for line in output.splitlines():
        if len(records) >= max_entries:
            break
        match = FLS_ROW_RE.match(line)
        if not match:
            continue
        path = match.group("path").strip()
        if not path:
            continue
        allocated = match.group("deleted") != "*"
        inode = match.group("inode").strip()
        record_id = f"{evidence_id}:fls:{len(records) + 1}:{inode}"
        records.append(
            FileMetadataRecord(
                record_id=record_id,
                path=path,
                inode=inode,
                entry_type=_entry_type(match.group("kind"), allocated),
                allocated=allocated,
            )
        )
    return records


def _parse_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        raw = float(value)
        if raw > 10_000_000_000_000:
            raw = raw / 1_000_000
        elif raw > 10_000_000_000:
            raw = raw / 1000
        return datetime.fromtimestamp(raw, tz=timezone.utc)

    text = str(value).strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    for candidate in (text, text.replace(" ", "T", 1)):
        try:
            parsed = datetime.fromisoformat(candidate)
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def _read_json_line_timeline(path: Path, *, evidence_id: str, max_records: int) -> tuple[list[TimelineRecord], bool]:
    records: list[TimelineRecord] = []
    truncated = False
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_number, line in enumerate(handle, start=1):
            if len(records) >= max_records:
                truncated = True
                break
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            timestamp = _parse_datetime(
                payload.get("datetime")
                or payload.get("timestamp")
                or payload.get("date_time")
                or payload.get("__timestamp")
            )
            if timestamp is None:
                continue
            message = payload.get("message") or payload.get("display_name") or payload.get("timestamp_desc") or "timeline event"
            record = TimelineRecord(
                record_id=f"{evidence_id}:timeline:{line_number}",
                timestamp_utc=timestamp,
                source=str(payload.get("source") or payload.get("parser") or "plaso"),
                source_long=payload.get("source_long"),
                artifact_path=payload.get("filename") or payload.get("display_name"),
                description=str(message),
                parser=payload.get("parser"),
                confidence=0.85,
            )
            records.append(record)
    return records, truncated


def _event_channel_from_path(path: Path) -> EventChannel:
    name = path.stem.lower()
    if "security" in name:
        return "security"
    if "system" in name:
        return "system"
    if "application" in name:
        return "application"
    if "powershell" in name or "power" in name:
        return "powershell"
    return "other"


def _event_id_from_payload(payload: dict[str, Any]) -> int:
    for key in ("event_id", "EventID", "event_identifier", "EventIdentifier"):
        value = payload.get(key)
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
    searchable = json.dumps(payload, ensure_ascii=True)
    match = EVENT_ID_RE.search(searchable)
    if match:
        return int(match.group("event_id"))
    return 0


def _write_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True, sort_keys=True) + "\n")


def _remember_reference(evidence_id: str, reference: EvidenceReference) -> None:
    EVIDENCE_INDEX.setdefault(evidence_id, []).append(reference)


def _remember_timeline_records(evidence_id: str, records: list[TimelineRecord], source_path: str) -> None:
    for record in records:
        _remember_reference(
            evidence_id,
            EvidenceReference(
                evidence_id=evidence_id,
                source_path=source_path,
                artifact_path=record.artifact_path,
                timestamp_utc=record.timestamp_utc,
                record_id=record.record_id,
                description=record.description,
            ),
        )


def _filter_records_by_time(
    records: list[TimelineRecord],
    start_utc: datetime | None,
    end_utc: datetime | None,
) -> list[TimelineRecord]:
    filtered = []
    start = _parse_datetime(start_utc)
    end = _parse_datetime(end_utc)
    for record in records:
        timestamp = record.timestamp_utc
        if start and timestamp < start:
            continue
        if end and timestamp > end:
            continue
        filtered.append(record)
    return filtered


@mcp.tool()
def case_open_readonly(request: CaseOpenReadonlyInput) -> CaseOpenReadonlyOutput:
    """Register a forensic image, bind it to a case workspace, and enforce read-only handling.

    Use this before any triage step. The backend implementation never writes to
    the original evidence path and returns a stable evidence_id for later tools.
    """
    evidence_path = _resolve_input_path(request.evidence_path, must_exist=True, label="evidence_path")
    if not evidence_path.is_file():
        _raise_tool_error(f"evidence_path must be a file: {evidence_path}")

    workspace_path = _resolve_input_path(request.case_workspace, must_exist=False, label="case_workspace")
    if workspace_path == evidence_path:
        _raise_tool_error("case_workspace cannot be the original evidence file")

    analysis_dir = _ensure_workspace_child(workspace_path / "analysis", workspace_path, label="analysis_dir")
    exports_dir = _ensure_workspace_child(workspace_path / "exports", workspace_path, label="exports_dir")
    reports_dir = _ensure_workspace_child(workspace_path / "reports", workspace_path, label="reports_dir")
    logs_dir = _ensure_workspace_child(workspace_path / "logs", workspace_path, label="logs_dir")
    for directory in (analysis_dir, exports_dir, reports_dir, logs_dir):
        directory.mkdir(parents=True, exist_ok=True)

    hash_status: HashStatus = "not_checked"
    messages = ["Evidence registered as read-only input; outputs are restricted to case workspace."]
    if request.expected_sha256:
        actual_sha256 = _hash_file(evidence_path)
        if actual_sha256.lower() == request.expected_sha256.lower():
            hash_status = "matched"
            messages.append("Expected SHA-256 matched.")
        else:
            _raise_tool_error("Evidence SHA-256 mismatch; refusing to open case.")

    evidence_id = _new_evidence_id(request.case_id, evidence_path)
    state = CaseState(
        case_id=request.case_id,
        evidence_id=evidence_id,
        evidence_path=evidence_path,
        workspace_path=workspace_path,
        analysis_dir=analysis_dir,
        exports_dir=exports_dir,
        reports_dir=reports_dir,
        logs_dir=logs_dir,
    )
    CASE_BY_EVIDENCE[evidence_id] = state
    CASE_BY_ID[request.case_id] = state
    _remember_reference(
        evidence_id,
        EvidenceReference(
            evidence_id=evidence_id,
            source_path=str(evidence_path),
            description="Registered forensic image",
        ),
    )

    return CaseOpenReadonlyOutput(
        evidence_id=evidence_id,
        case_id=request.case_id,
        evidence_path=str(evidence_path),
        workspace=CaseWorkspace(
            case_id=request.case_id,
            workspace_path=str(workspace_path),
            analysis_dir=str(analysis_dir),
            exports_dir=str(exports_dir),
            reports_dir=str(reports_dir),
        ),
        readonly_enforced=True,
        original_writable_exposed=False,
        hash_status=hash_status,
        parser_status="ok",
        messages=messages,
    )


@mcp.tool()
def list_partitions(request: ListPartitionsInput) -> ListPartitionsOutput:
    """Inspect partition layout and filesystem hints for a registered disk image."""
    state = _get_case_by_evidence(request.evidence_id)
    image_path = _validate_registered_evidence(state, request.image_path)
    args = ["mmls", "-B", str(image_path)]
    command_tool = "mmls"
    command_args = args
    try:
        result = _run_command("mmls", args)
        partitions = _parse_mmls_output(result.stdout, sector_size=request.sector_size)
    except Exception as exc:
        if "not available" in str(exc):
            raise
        fsstat_args = ["fsstat", str(image_path)]
        fsstat_result = _run_command("fsstat", fsstat_args)
        partitions = [_partition_from_volume_fsstat(fsstat_result.stdout, image_path, request.sector_size)]
        command_tool = "fsstat"
        command_args = fsstat_args
    if not request.include_unallocated:
        partitions = [partition for partition in partitions if partition.is_allocated]
    selected = next((partition.start_sector for partition in partitions if partition.is_allocated), None)
    for partition in partitions:
        _remember_reference(
            request.evidence_id,
            EvidenceReference(
                evidence_id=request.evidence_id,
                source_path=str(image_path),
                offset_bytes=partition.start_sector * request.sector_size,
                record_id=f"{request.evidence_id}:partition:{partition.slot}",
                description=f"Partition {partition.slot}: {partition.description}",
            ),
        )
    return ListPartitionsOutput(
        evidence_id=request.evidence_id,
        parser_status="ok",
        partitions=partitions,
        selected_partition_start_sector=selected,
        command_plan=CommandPlan(
            tool=command_tool,
            arguments=command_args,
            parser="mmls_text_table_or_volume_fsstat",
            expected_output="partition table or volume filesystem",
        ),
    )


@mcp.tool()
def filesystem_inventory(request: FilesystemInventoryInput) -> FilesystemInventoryOutput:
    """Enumerate filesystem entries from a selected partition without exposing shell access."""
    state = _get_case_by_evidence(request.evidence_id)
    image_path = _validate_registered_evidence(state, request.image_path)
    for path_filter in request.path_filters:
        if _has_parent_segment(path_filter) or Path(path_filter).is_absolute():
            _raise_tool_error("Path traversal rejected for path_filters")

    args = ["fls"]
    if request.recursive:
        args.append("-r")
    args.extend(["-p", "-o", str(request.partition_start_sector), str(image_path)])
    if request.root_inode:
        args.append(request.root_inode)
    result = _run_command("fls", args)
    records = _parse_fls_output(result.stdout, evidence_id=request.evidence_id, max_entries=request.max_entries)
    if not request.include_deleted:
        records = [record for record in records if record.allocated is not False]
    if request.path_filters:
        lowered_filters = [item.lower() for item in request.path_filters]
        records = [record for record in records if any(item in record.path.lower() for item in lowered_filters)]
    truncated = len(records) >= request.max_entries
    for record in records:
        _remember_reference(
            request.evidence_id,
            EvidenceReference(
                evidence_id=request.evidence_id,
                source_path=str(image_path),
                record_id=record.record_id,
                description=f"Filesystem entry {record.path}",
            ),
        )
    return FilesystemInventoryOutput(
        evidence_id=request.evidence_id,
        parser_status="partial" if truncated else "ok",
        records=records,
        truncated=truncated,
        command_plan=CommandPlan(
            tool="fls",
            arguments=args,
            parser="fls_text_listing",
            expected_output="filesystem inventory",
        ),
    )


@mcp.tool()
def build_timeline(request: BuildTimelineInput) -> BuildTimelineOutput:
    """Build a normalized forensic timeline from image-derived artifacts."""
    state = _get_case_by_evidence(request.evidence_id)
    source_path = _resolve_input_path(request.source_path, must_exist=True, label="source_path")
    if source_path != state.evidence_path and not _is_relative_to(source_path, state.workspace_path):
        _raise_tool_error("source_path must be registered evidence or a case workspace artifact")
    if request.mode != "plaso_json_line":
        _raise_tool_error("Only plaso_json_line mode is implemented for the backend MVP")

    storage_file = _workspace_file(state, state.analysis_dir, f"{request.evidence_id}.plaso", label="plaso storage")
    jsonl_file = _workspace_file(state, state.exports_dir, f"{request.evidence_id}_timeline.jsonl", label="timeline export")
    log2timeline_args = [
        "log2timeline.py",
        "--parsers",
        request.parser_preset,
        "--timezone",
        request.timezone,
        "--unattended",
        str(storage_file),
        str(source_path),
    ]
    psort_args = ["psort.py", "-o", "json_line", "-w", str(jsonl_file), str(storage_file)]
    _run_command("log2timeline.py", log2timeline_args, timeout=DEFAULT_TIMEOUT_SECONDS * 4)
    _run_command("psort.py", psort_args, timeout=DEFAULT_TIMEOUT_SECONDS * 4)
    if not jsonl_file.exists():
        _raise_tool_error("psort.py completed but did not create a JSON Lines timeline")
    records, truncated = _read_json_line_timeline(jsonl_file, evidence_id=request.evidence_id, max_records=request.max_records)
    records = _filter_records_by_time(records, request.start_utc, request.end_utc)
    _remember_timeline_records(request.evidence_id, records, str(source_path))
    return BuildTimelineOutput(
        evidence_id=request.evidence_id,
        parser_status="partial" if truncated else "ok",
        timeline_path=str(jsonl_file),
        records=records,
        truncated=truncated,
        command_plan=[
            CommandPlan(
                tool="log2timeline.py",
                arguments=log2timeline_args,
                parser="plaso_storage",
                expected_output="plaso storage file",
            ),
            CommandPlan(
                tool="psort.py",
                arguments=psort_args,
                parser="plaso_json_line",
                expected_output="timeline JSON Lines",
            ),
        ],
    )


def _registry_plugin_args(scope: RegistryPluginScope, output_mode: RegistryOutputMode) -> list[str]:
    if output_mode == "tln" or scope == "all_persistence":
        return ["-aT"]
    plugin_by_scope = {
        "run_keys": "run",
        "services": "services",
        "scheduled_tasks": "tasks",
    }
    plugin = plugin_by_scope.get(scope)
    if plugin is None:
        _raise_tool_error(f"Unsupported registry plugin scope: {scope}")
    return ["-p", plugin]


def _persistence_type_from_text(text: str) -> PersistenceType:
    lowered = text.lower()
    if "run" in lowered:
        return "run_key"
    if "service" in lowered:
        return "service"
    if "task" in lowered:
        return "scheduled_task"
    if "startup" in lowered:
        return "startup_folder"
    return "unknown"


def _parse_regripper_output(
    output: str,
    *,
    evidence_id: str,
    hive_path: Path,
    max_records: int,
) -> list[RegistryPersistenceRecord]:
    records: list[RegistryPersistenceRecord] = []
    current_key = ""
    current_service_name: str | None = None
    for line_number, line in enumerate(output.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        lowered_stripped = stripped.lower()
        if re.match(r"^[a-z0-9_]+ v\.\d+", lowered_stripped) or lowered_stripped.startswith("("):
            continue
        if lowered_stripped.startswith("lists services/drivers"):
            continue
        if line == line.lstrip() and "\\" in stripped and "=" not in stripped and len(stripped) < 260:
            current_key = stripped
            current_service_name = None
            continue
        key_lower = current_key.lower()
        if "\\run" in key_lower and " - " in stripped:
            value_name, value_data = [part.strip() for part in stripped.split(" - ", 1)]
            reference = EvidenceReference(
                evidence_id=evidence_id,
                source_path=str(hive_path),
                record_id=f"{evidence_id}:registry:{line_number}",
                description=f"{current_key}: {value_name} - {value_data}"[:500],
            )
            records.append(
                RegistryPersistenceRecord(
                    record_id=f"{evidence_id}:registry:{line_number}",
                    hive_path=str(hive_path),
                    registry_path=current_key,
                    persistence_type="run_key",
                    value_name=value_name,
                    value_data=value_data,
                    source_tool="regripper",
                    evidence_refs=[reference],
                )
            )
            if len(records) >= max_records:
                break
            continue
        if key_lower.endswith("\\services") and "=" in stripped:
            name, value = [part.strip() for part in stripped.split("=", 1)]
            if name == "Name" and value:
                current_service_name = value
                continue
            if name == "ImagePath" and current_service_name:
                service_key = f"{current_key}\\{current_service_name}"
                reference = EvidenceReference(
                    evidence_id=evidence_id,
                    source_path=str(hive_path),
                    record_id=f"{evidence_id}:registry:{line_number}",
                    description=f"{service_key}: ImagePath = {value}"[:500],
                )
                records.append(
                    RegistryPersistenceRecord(
                        record_id=f"{evidence_id}:registry:{line_number}",
                        hive_path=str(hive_path),
                        registry_path=service_key,
                        persistence_type="service",
                        value_name=current_service_name,
                        value_data=value,
                        source_tool="regripper",
                        evidence_refs=[reference],
                    )
                )
                if len(records) >= max_records:
                    break
                continue
            continue
        if not any(token in lowered_stripped for token in ("run", "service", "task", "startup", "autorun")):
            continue
        if len(records) >= max_records:
            break
        value_name = None
        value_data = None
        if "=" in stripped:
            value_name, value_data = [part.strip() for part in stripped.split("=", 1)]
        reference = EvidenceReference(
            evidence_id=evidence_id,
            source_path=str(hive_path),
            record_id=f"{evidence_id}:registry:{line_number}",
            description=stripped[:500],
        )
        records.append(
            RegistryPersistenceRecord(
                record_id=f"{evidence_id}:registry:{line_number}",
                hive_path=str(hive_path),
                registry_path=current_key or stripped[:200],
                persistence_type=_persistence_type_from_text(stripped),
                value_name=value_name,
                value_data=value_data,
                source_tool="regripper",
                evidence_refs=[reference],
            )
        )
    return records


@mcp.tool()
def extract_registry_persistence(
    request: ExtractRegistryPersistenceInput,
) -> ExtractRegistryPersistenceOutput:
    """Extract Windows persistence signals from registry hives."""
    state = _get_case_by_evidence(request.evidence_id)
    plugin_args = _registry_plugin_args(request.plugin_scope, request.output_mode)
    all_records: list[RegistryPersistenceRecord] = []
    last_args: list[str] = []
    truncated = False
    for hive_text in request.hive_paths:
        hive_path = _resolve_input_path(hive_text, must_exist=True, label="hive_path")
        raw_output = _workspace_file(
            state,
            state.exports_dir,
            f"{request.evidence_id}_{hive_path.stem}_{request.plugin_scope}_regripper.txt",
            label="registry export",
        )
        args = ["rip.pl", "-r", str(hive_path), *plugin_args]
        last_args = args
        result = _run_command("rip.pl", args)
        raw_output.write_text(result.stdout, encoding="utf-8", errors="replace")
        remaining = request.max_records - len(all_records)
        if remaining <= 0:
            truncated = True
            break
        records = _parse_regripper_output(
            result.stdout,
            evidence_id=request.evidence_id,
            hive_path=hive_path,
            max_records=remaining,
        )
        all_records.extend(records)
        for record in records:
            for reference in record.evidence_refs:
                _remember_reference(request.evidence_id, reference)
    return ExtractRegistryPersistenceOutput(
        evidence_id=request.evidence_id,
        parser_status="partial" if truncated else "ok",
        records=all_records,
        truncated=truncated,
        command_plan=CommandPlan(
            tool="rip.pl",
            arguments=last_args,
            parser="regripper_text",
            expected_output="registry persistence records",
        ),
    )


def _read_json_line_events(
    path: Path,
    *,
    evidence_id: str,
    source_path: Path,
    max_records: int,
    event_ids: set[int],
) -> tuple[list[EventRecord], bool]:
    records: list[EventRecord] = []
    truncated = False
    channel = _event_channel_from_path(source_path)
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_number, line in enumerate(handle, start=1):
            if len(records) >= max_records:
                truncated = True
                break
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            event_id = _event_id_from_payload(payload)
            if event_ids and event_id not in event_ids:
                continue
            timestamp = _parse_datetime(payload.get("datetime") or payload.get("timestamp") or payload.get("__timestamp"))
            message = payload.get("message") or payload.get("display_name") or json.dumps(payload, ensure_ascii=True)[:500]
            records.append(
                EventRecord(
                    record_id=f"{evidence_id}:event:{source_path.name}:{line_number}",
                    event_id=event_id,
                    timestamp_utc=timestamp,
                    provider=payload.get("provider") or payload.get("source") or payload.get("parser"),
                    channel=channel,
                    rendered_message=str(message),
                    fields=payload,
                    source_path=str(source_path),
                )
            )
    return records, truncated


def _read_evtx_records_with_python_evtx(
    path: Path,
    *,
    evidence_id: str,
    max_records: int,
    event_ids: set[int],
) -> tuple[list[EventRecord], bool]:
    try:
        from Evtx.Evtx import Evtx  # type: ignore[import-not-found]
    except ImportError as exc:
        _raise_tool_error("python-evtx fallback is unavailable; install requirements.txt")
        raise AssertionError("unreachable") from exc

    records: list[EventRecord] = []
    truncated = False
    channel = _event_channel_from_path(path)
    namespace = {"event": "http://schemas.microsoft.com/win/2004/08/events/event"}
    with Evtx(str(path)) as event_log:
        for index, record in enumerate(event_log.records(), start=1):
            if len(records) >= max_records:
                truncated = True
                break
            try:
                xml_text = record.xml()
                root = ET.fromstring(xml_text)
            except Exception:
                continue
            event_id_element = root.find("./event:System/event:EventID", namespace)
            try:
                event_id = int((event_id_element.text if event_id_element is not None else "0") or "0")
            except ValueError:
                event_id = 0
            if event_ids and event_id not in event_ids:
                continue
            provider_element = root.find("./event:System/event:Provider", namespace)
            time_element = root.find("./event:System/event:TimeCreated", namespace)
            timestamp_text = time_element.attrib.get("SystemTime") if time_element is not None else None
            provider = provider_element.attrib.get("Name") if provider_element is not None else None
            records.append(
                EventRecord(
                    record_id=f"{evidence_id}:event:{path.name}:{index}",
                    event_id=event_id,
                    channel=channel,
                    source_path=str(path),
                    timestamp_utc=_parse_datetime(timestamp_text),
                    provider=provider,
                    rendered_message=xml_text[:1000],
                    fields={
                        "parser": "python-evtx",
                        "record_number": index,
                        "xml_excerpt": xml_text[:3000],
                    },
                )
            )
    return records, truncated


@mcp.tool()
def extract_event_records(request: ExtractEventRecordsInput) -> ExtractEventRecordsOutput:
    """Extract selected Windows event records relevant to incident triage."""
    state = _get_case_by_evidence(request.evidence_id)
    event_ids = set(request.event_ids)
    all_records: list[EventRecord] = []
    truncated = False
    last_args: list[str] = []
    command_tool = "psort.py"
    command_parser = "plaso_event_json_line"
    for event_log_text in request.event_log_paths:
        event_log_path = _resolve_input_path(event_log_text, must_exist=True, label="event_log_path")
        channel = _event_channel_from_path(event_log_path)
        if request.channels and channel not in request.channels:
            continue
        storage_file = _workspace_file(
            state,
            state.analysis_dir,
            f"{request.evidence_id}_{event_log_path.stem}.plaso",
            label="event storage",
        )
        jsonl_file = _workspace_file(
            state,
            state.exports_dir,
            f"{request.evidence_id}_{event_log_path.stem}_events.jsonl",
            label="event export",
        )
        log2timeline_args = [
            "log2timeline.py",
            "--parsers",
            "winevtx",
            "--timezone",
            "UTC",
            "--unattended",
            str(storage_file),
            str(event_log_path),
        ]
        psort_args = ["psort.py", "-o", "json_line", "-w", str(jsonl_file), str(storage_file)]
        last_args = psort_args
        try:
            _run_command("log2timeline.py", log2timeline_args, timeout=DEFAULT_TIMEOUT_SECONDS * 2)
            _run_command("psort.py", psort_args, timeout=DEFAULT_TIMEOUT_SECONDS * 2)
            records, file_truncated = _read_json_line_events(
                jsonl_file,
                evidence_id=request.evidence_id,
                source_path=event_log_path,
                max_records=request.max_records - len(all_records),
                event_ids=event_ids,
            )
            command_tool = "psort.py"
            command_parser = "plaso_event_json_line"
        except ToolError:
            last_args = ["python-evtx", str(event_log_path)]
            records, file_truncated = _read_evtx_records_with_python_evtx(
                event_log_path,
                evidence_id=request.evidence_id,
                max_records=request.max_records - len(all_records),
                event_ids=event_ids,
            )
            command_tool = "python-evtx"
            command_parser = "python_evtx_xml"
        records = [
            record
            for record in records
            if (request.start_utc is None or (record.timestamp_utc and record.timestamp_utc >= request.start_utc))
            and (request.end_utc is None or (record.timestamp_utc and record.timestamp_utc <= request.end_utc))
        ]
        all_records.extend(records)
        truncated = truncated or file_truncated or len(all_records) >= request.max_records
        for record in records:
            _remember_reference(
                request.evidence_id,
                EvidenceReference(
                    evidence_id=request.evidence_id,
                    source_path=str(event_log_path),
                    record_id=record.record_id,
                    timestamp_utc=record.timestamp_utc,
                    description=record.rendered_message or f"Event {record.event_id}",
                ),
            )
        if truncated:
            break
    return ExtractEventRecordsOutput(
        evidence_id=request.evidence_id,
        parser_status="partial" if truncated else "ok",
        records=all_records,
        truncated=truncated,
        command_plan=CommandPlan(
            tool=command_tool,
            arguments=last_args,
            parser=command_parser,
            expected_output="Windows event records",
        ),
    )


def _claim_tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9_.$\\/-]{4,}", text.lower()) if token not in {"with", "from", "that", "this"}}


@mcp.tool()
def verify_claim(request: VerifyClaimInput) -> VerifyClaimOutput:
    """Verify an investigative claim against normalized evidence references."""
    refs = list(request.evidence_refs)
    missing: list[str] = []
    for evidence_id in request.evidence_ids:
        stored = EVIDENCE_INDEX.get(evidence_id)
        if stored:
            refs.extend(stored)
        else:
            missing.append(evidence_id)

    tokens = _claim_tokens(request.claim_text)
    supporting = []
    for reference in refs:
        haystack = f"{reference.description} {reference.source_path} {reference.artifact_path or ''}".lower()
        if not tokens or any(token in haystack for token in tokens):
            supporting.append(reference)

    if supporting and request.required_confidence == "confirmed":
        status: ClaimStatus = "confirmed"
        rationale = "Claim has direct linked evidence references."
    elif supporting:
        status = "inferred"
        rationale = "Claim has related evidence references but confidence target allows inference."
    elif refs:
        status = "unsupported"
        rationale = "Evidence was available, but no reference matched the claim text."
    else:
        status = "needs_human_review" if missing else "unsupported"
        rationale = "No usable evidence references were available for this claim."

    return VerifyClaimOutput(
        result=ClaimVerificationResult(
            claim_id=request.claim_id,
            status=status,
            rationale=rationale,
            supporting_evidence=supporting,
            missing_evidence=missing,
            recommended_followup_tools=[] if supporting else ["filesystem_inventory", "build_timeline", "extract_registry_persistence"],
        )
    )


@mcp.tool()
def write_execution_log(request: WriteExecutionLogInput) -> WriteExecutionLogOutput:
    """Append an audit-log record for an agent action and its evidence references."""
    state = _get_case_for_log(request.case_id, request.evidence_id)
    log_path = _workspace_file(state, state.logs_dir, "agent_execution.jsonl", label="execution log")
    record = ExecutionLogRecord(
        run_id=request.run_id,
        case_id=request.case_id,
        step_number=request.step_number,
        timestamp_utc=datetime.now(timezone.utc),
        tool_name=request.tool_name,
        arguments=request.arguments,
        parser_status=request.parser_status,
        agent_intent=request.agent_intent,
        evidence_id=request.evidence_id,
        output_reference=request.output_reference,
        token_usage=request.token_usage,
        correction_reason=request.correction_reason,
    )
    _write_jsonl(log_path, record.model_dump(mode="json"))
    if request.evidence_id:
        _remember_reference(
            request.evidence_id,
            EvidenceReference(
                evidence_id=request.evidence_id,
                source_path=str(log_path),
                record_id=f"{request.run_id}:{request.step_number}",
                description=f"Execution log entry for {request.tool_name}",
            ),
        )
    return WriteExecutionLogOutput(appended=True, log_path=str(log_path), record=record)


if __name__ == "__main__":
    mcp.run(transport="stdio")
