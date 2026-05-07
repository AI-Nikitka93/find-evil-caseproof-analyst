from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .claim_policy import CorrectionLedgerEntry
from .output_package import public_safe_redact


REQUIRED_REAL_RUN_OUTPUTS = (
    "reports/final_analyst_report.md",
    "reports/evidence_book.md",
    "reports/correction_ledger.md",
    "reports/real_run_accuracy_report.md",
    "exports/correlation_summary.json",
    "logs/agent_execution.jsonl",
)
ACCEPTED_UNSUPPORTED_DISPOSITIONS = {"dropped", "downgraded", "needs_human_review", "corrected"}
CONFIRMED_FINDING_RE = re.compile(r"^\s*-\s*(?P<id>[A-Za-z]+-\d+|T\d+|F-\d+|F\d+)\b.*", re.MULTILINE)
PRIVATE_SURFACE_PATTERNS = (
    re.compile(r"[A-Za-z]:\\[^\s`\"']+"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"\bsk-ant-[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9_]{8,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{8,}\b"),
)


@dataclass(frozen=True, slots=True)
class RealRunOutputSet:
    passed: bool
    missing_outputs: list[str]


@dataclass(frozen=True, slots=True)
class ValidationGateResult:
    passed: bool
    blockers: list[str]


@dataclass(frozen=True, slots=True)
class RealValidationAudit:
    status: str
    checks: dict[str, bool]
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class EvidenceSnapshot:
    path: str
    size_bytes: int
    modified_ns: int
    sha256: str | None = None


def validate_real_run_outputs(case_workspace: Path) -> RealRunOutputSet:
    missing = [relative for relative in REQUIRED_REAL_RUN_OUTPUTS if not (case_workspace / relative).is_file()]
    return RealRunOutputSet(passed=not missing, missing_outputs=missing)


def snapshot_evidence(path: Path, *, sha256: str | None = None) -> EvidenceSnapshot:
    stat = path.stat()
    return EvidenceSnapshot(
        path=str(path.resolve()),
        size_bytes=stat.st_size,
        modified_ns=stat.st_mtime_ns,
        sha256=sha256,
    )


def validate_original_evidence_unchanged(before: EvidenceSnapshot, after: EvidenceSnapshot) -> ValidationGateResult:
    blockers: list[str] = []
    if before.path != after.path:
        blockers.append("evidence_path_changed")
    if before.size_bytes != after.size_bytes:
        blockers.append("evidence_size_changed")
    if before.modified_ns != after.modified_ns:
        blockers.append("evidence_modified_time_changed")
    if before.sha256 and after.sha256 and before.sha256.lower() != after.sha256.lower():
        blockers.append("evidence_hash_changed")
    return ValidationGateResult(passed=not blockers, blockers=blockers)


def validate_outputs_under_workspace(output_paths: list[Path], workspace_path: Path) -> ValidationGateResult:
    blockers: list[str] = []
    workspace = workspace_path.resolve()
    for path in output_paths:
        try:
            if not path.resolve().is_relative_to(workspace):
                blockers.append(f"output_outside_workspace:{path}")
        except FileNotFoundError:
            blockers.append(f"output_missing:{path}")
    return ValidationGateResult(passed=not blockers, blockers=blockers)


def validate_final_report_evidence_links(report_text: str) -> ValidationGateResult:
    blockers: list[str] = []
    confirmed_section = report_text.split("## Confirmed Findings", 1)[-1]
    if "##" in confirmed_section:
        confirmed_section = confirmed_section.split("##", 1)[0]
    matches = list(CONFIRMED_FINDING_RE.finditer(confirmed_section))
    for index, match in enumerate(matches):
        block_end = matches[index + 1].start() if index + 1 < len(matches) else len(confirmed_section)
        block = confirmed_section[match.start() : block_end]
        if "evidence" not in block.lower() and "ev-" not in block.lower():
            blockers.append(f"confirmed_finding_without_evidence:{match.group('id')}")
    return ValidationGateResult(passed=not blockers, blockers=blockers)


def validate_unsupported_claim_handling(
    *,
    candidate_claim_ids: list[str],
    final_dispositions: dict[str, str],
) -> ValidationGateResult:
    blockers = [
        f"unhandled_unsupported_claim:{claim_id}"
        for claim_id in candidate_claim_ids
        if final_dispositions.get(claim_id) not in ACCEPTED_UNSUPPORTED_DISPOSITIONS
    ]
    return ValidationGateResult(passed=not blockers, blockers=blockers)


def validate_self_correction_presence(entries: list[CorrectionLedgerEntry]) -> ValidationGateResult:
    blockers: list[str] = []
    if not entries:
        blockers.append("missing_visible_self_correction")
    for index, entry in enumerate(entries, start=1):
        if not entry.reason_challenged.strip():
            blockers.append(f"correction_missing_reason:{index}")
        if not entry.follow_up_action.strip():
            blockers.append(f"correction_missing_followup:{index}")
        if entry.final_status not in ACCEPTED_UNSUPPORTED_DISPOSITIONS:
            blockers.append(f"correction_invalid_final_status:{index}")
    return ValidationGateResult(passed=not blockers, blockers=blockers)


def validate_parser_failure_behavior(*, parser_status: str, visible_notice: str) -> ValidationGateResult:
    blockers: list[str] = []
    if parser_status not in {"failed", "partial"}:
        blockers.append("parser_status_not_degraded")
    lowered = visible_notice.lower()
    for marker in ("failed", "partial", "unknown", "cannot be confirmed"):
        if marker in lowered:
            break
    else:
        blockers.append("parser_failure_not_visible")
    return ValidationGateResult(passed=not blockers, blockers=blockers)


def validate_no_confirmed_finding_report(report_text: str) -> ValidationGateResult:
    lowered = report_text.lower()
    blockers: list[str] = []
    if "no confirmed" not in lowered:
        blockers.append("missing_no_confirmed_statement")
    if "scope" not in lowered:
        blockers.append("missing_scope_statement")
    if "clean" in lowered or "no evil" in lowered and "confirmed" not in lowered:
        blockers.append("overclaims_clean_result")
    return ValidationGateResult(passed=not blockers, blockers=blockers)


def validate_degraded_environment_behavior(preflight_report: dict[str, Any]) -> ValidationGateResult:
    blockers: list[str] = []
    if preflight_report.get("status") != "blocked":
        blockers.append("degraded_environment_not_blocked")
    failed = set(preflight_report.get("failed_checks", []))
    if not failed:
        blockers.append("degraded_environment_missing_failed_checks")
    checks = preflight_report.get("checks", [])
    if not isinstance(checks, list) or not all("detail" in item for item in checks if isinstance(item, dict)):
        blockers.append("degraded_environment_missing_details")
    return ValidationGateResult(passed=not blockers, blockers=blockers)


def validate_correlation_summary(summary: dict[str, Any]) -> ValidationGateResult:
    blockers: list[str] = []
    if not isinstance(summary.get("confirmed_compromise"), bool):
        blockers.append("missing_confirmed_compromise_boolean")
    if not summary.get("status"):
        blockers.append("missing_correlation_status")
    findings = summary.get("correlation_findings", [])
    if not isinstance(findings, list):
        blockers.append("invalid_correlation_findings")
        findings = []
    for finding in findings:
        if not isinstance(finding, dict):
            blockers.append("invalid_correlation_finding")
            continue
        finding_id = str(finding.get("finding_id") or "unknown")
        refs = finding.get("evidence_refs", [])
        if not isinstance(refs, list) or not refs:
            blockers.append(f"correlation_finding_without_evidence:{finding_id}")
    rejected = summary.get("rejected_claims", [])
    rejected_text = " ".join(str(item).lower() for item in rejected) if isinstance(rejected, list) else ""
    if "confirmed compromise" not in rejected_text:
        blockers.append("missing_rejected_compromise_claim")
    return ValidationGateResult(passed=not blockers, blockers=blockers)


def validate_redaction_surfaces(surface_texts: dict[str, str]) -> ValidationGateResult:
    blockers: list[str] = []
    for name, text in surface_texts.items():
        redacted = public_safe_redact(text)
        for pattern in PRIVATE_SURFACE_PATTERNS:
            if pattern.search(redacted):
                blockers.append(f"unredacted_private_value:{name}")
                break
    return ValidationGateResult(passed=not blockers, blockers=sorted(set(blockers)))


def validate_spoliation_resistance(
    *,
    server_source: str,
    evidence_path: Path,
    log_path: Path,
    workspace_path: Path,
) -> ValidationGateResult:
    blockers: list[str] = []
    forbidden_public_tools = ("delete_original_evidence", "overwrite_evidence", "raw_shell", "rm_original")
    for name in forbidden_public_tools:
        if f"def {name}(" in server_source:
            blockers.append(f"unsafe_public_tool:{name}")
    if "shell=True" in server_source:
        blockers.append("generic_shell_execution_enabled")
    if not evidence_path.is_file():
        blockers.append("evidence_missing_after_test")
    try:
        if not log_path.resolve().is_relative_to(workspace_path.resolve()):
            blockers.append("blocked_action_log_outside_workspace")
    except FileNotFoundError:
        blockers.append("blocked_action_log_missing")
    return ValidationGateResult(passed=not blockers, blockers=blockers)


def audit_real_validation_workspace(case_workspace: Path) -> RealValidationAudit:
    output_result = validate_real_run_outputs(case_workspace)
    checks = {"required_outputs_exist": output_result.passed}
    blockers = [f"missing_output:{item}" for item in output_result.missing_outputs]

    report_path = case_workspace / "reports" / "final_analyst_report.md"
    if report_path.is_file():
        report_result = validate_final_report_evidence_links(report_path.read_text(encoding="utf-8", errors="replace"))
        checks["confirmed_findings_have_evidence"] = report_result.passed
        blockers.extend(report_result.blockers)
    else:
        checks["confirmed_findings_have_evidence"] = False

    ledger_path = case_workspace / "reports" / "correction_ledger.md"
    checks["correction_ledger_present"] = ledger_path.is_file()
    if not ledger_path.is_file():
        blockers.append("missing_correction_ledger")

    log_path = case_workspace / "logs" / "agent_execution.jsonl"
    checks["execution_log_parseable"] = _jsonl_parseable(log_path)
    if log_path.is_file() and not checks["execution_log_parseable"]:
        blockers.append("execution_log_not_parseable")

    correlation_path = case_workspace / "exports" / "correlation_summary.json"
    if correlation_path.is_file():
        try:
            correlation_payload = json.loads(correlation_path.read_text(encoding="utf-8", errors="replace"))
        except json.JSONDecodeError:
            correlation_result = ValidationGateResult(False, ["correlation_summary_not_json"])
        else:
            correlation_result = validate_correlation_summary(correlation_payload)
    else:
        correlation_result = ValidationGateResult(False, ["missing_correlation_summary"])
    checks["correlation_summary_valid"] = correlation_result.passed
    blockers.extend(correlation_result.blockers)

    return RealValidationAudit(
        status="ok" if all(checks.values()) and not blockers else "blocked",
        checks=checks,
        blockers=sorted(set(blockers)),
    )


def _jsonl_parseable(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip():
                json.loads(line)
    except json.JSONDecodeError:
        return False
    return True
