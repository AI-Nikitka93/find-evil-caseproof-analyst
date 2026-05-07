from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from .claim_policy import CorrectionLedgerEntry
from .reporting import render_correction_ledger


FindingStatus = Literal["confirmed", "inferred", "dropped", "corrected", "needs_human_review"]


@dataclass(frozen=True, slots=True)
class Finding:
    finding_id: str
    title: str
    status: FindingStatus
    evidence_refs: list[str]
    tool_trace: list[str]
    confidence: str


@dataclass(frozen=True, slots=True)
class EvidenceBookEntry:
    finding_id: str
    evidence_ref: str
    source_reference: str
    artifact_family: str
    extraction_action: str
    parser_status: str
    review_notes: str


@dataclass(frozen=True, slots=True)
class AccuracySummary:
    dataset: str
    methodology: str
    findings_accuracy: str
    false_positives: list[str]
    missed_artifacts: list[str]
    hallucination_controls: list[str]
    evidence_integrity: str
    limits: list[str]
    untested_families: list[str] | None = None
    rejected_unsupported_claims: list[str] | None = None
    baseline_comparison: str | None = None


@dataclass(frozen=True, slots=True)
class OutputPackageInput:
    case_id: str
    output_dir: Path
    executive_summary: str
    scope: list[str]
    confirmed_findings: list[Finding]
    inferred_findings: list[Finding]
    rejected_claims: list[str]
    limitations: list[str]
    next_actions: list[str]
    evidence_book: list[EvidenceBookEntry]
    correction_entries: list[CorrectionLedgerEntry]
    accuracy: AccuracySummary
    execution_steps: list[dict[str, object]]
    synthetic_historical_path: str | None = None


@dataclass(frozen=True, slots=True)
class OutputPackageResult:
    created_files: dict[str, Path]


@dataclass(frozen=True, slots=True)
class QualityGateResult:
    passed: bool
    blockers: list[str]


OUTPUT_FILENAMES = {
    "final_analyst_report": "final_analyst_report.md",
    "evidence_book": "evidence_book.md",
    "correction_ledger": "correction_ledger.md",
    "real_run_accuracy_report": "real_run_accuracy_report.md",
    "execution_log_review": "execution_log_review.md",
    "judge_summary": "judge_summary.md",
    "reviewer_glossary": "reviewer_glossary.md",
    "quality_gate_summary": "quality_gate_summary.md",
    "artifact_index": "artifact_index.json",
}


TOKEN_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"\bsk-ant-[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9_]{8,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{8,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]{8,}\b", re.IGNORECASE),
)
WINDOWS_PATH_RE = re.compile(r"(?<![A-Za-z])(?:[A-Za-z]:\\[^\s`\"']+)")
USER_HOME_RE = re.compile(r"(?i)\b(?:C:\\Users\\|/Users/|/home/)([^\\/\s`\"']+)")
MACHINE_NAME_RE = re.compile(r"\b(?:DESKTOP|LAPTOP|WIN|PC)-[A-Z0-9-]{4,}\b", re.IGNORECASE)


def public_safe_redact(text: str) -> str:
    redacted = text
    for pattern in TOKEN_PATTERNS:
        redacted = pattern.sub("[TOKEN]", redacted)
    redacted = USER_HOME_RE.sub(lambda match: match.group(0).replace(match.group(1), "[USER]"), redacted)
    redacted = WINDOWS_PATH_RE.sub("[LOCAL_PATH]", redacted)
    redacted = MACHINE_NAME_RE.sub("[MACHINE]", redacted)
    return redacted


def _bullet(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- None recorded"


def _finding_block(finding: Finding) -> str:
    evidence = ", ".join(finding.evidence_refs) if finding.evidence_refs else "none"
    trace = ", ".join(finding.tool_trace) if finding.tool_trace else "none"
    return "\n".join(
        [
            f"- {finding.finding_id}: {finding.title}",
            f"  - Status: {finding.status}",
            f"  - Evidence: {evidence}",
            f"  - Tool trace: {trace}",
            f"  - Confidence: {finding.confidence}",
        ]
    )


def render_final_analyst_report(package: OutputPackageInput) -> str:
    confirmed = "\n".join(_finding_block(item) for item in package.confirmed_findings) or "- None"
    inferred = "\n".join(_finding_block(item) for item in package.inferred_findings) or "- None"
    return "\n".join(
        [
            "# Final Analyst Report",
            "",
            "## Executive Summary",
            package.executive_summary,
            "",
            "## Scope",
            _bullet(package.scope),
            "",
            "## Confirmed Findings",
            confirmed,
            "",
            "## Inferred Findings",
            inferred,
            "",
            "## Rejected Claims",
            _bullet(package.rejected_claims),
            "",
            "## Limitations",
            _bullet(package.limitations),
            "",
            "## Next Analyst Actions",
            _bullet(package.next_actions),
        ]
    )


def render_evidence_book(entries: list[EvidenceBookEntry]) -> str:
    blocks = ["# Evidence Book"]
    for entry in entries:
        blocks.append(
            "\n".join(
                [
                    f"## Finding {entry.finding_id}",
                    f"- Evidence reference: {entry.evidence_ref}",
                    f"- Source reference: {entry.source_reference}",
                    f"- Artifact family: {entry.artifact_family}",
                    f"- Extraction action: {entry.extraction_action}",
                    f"- Parser status: {entry.parser_status}",
                    f"- Review notes: {entry.review_notes}",
                ]
            )
        )
    if len(blocks) == 1:
        blocks.append("No evidence entries recorded.")
    return "\n\n".join(blocks)


def render_real_run_accuracy_report(summary: AccuracySummary) -> str:
    baseline = summary.baseline_comparison or "Future scope until a fair, reproducible baseline run exists."
    return "\n".join(
        [
            "# Real Run Accuracy Report",
            "",
            "## Dataset",
            summary.dataset,
            "",
            "## Methodology",
            summary.methodology,
            "",
            "## Findings Accuracy",
            summary.findings_accuracy,
            "",
            "## False Positives",
            _bullet(summary.false_positives),
            "",
            "## Missed Artifacts",
            _bullet(summary.missed_artifacts),
            "",
            "## Untested Families And Unknowns",
            _bullet(summary.untested_families or []),
            "",
            "## Hallucination Controls",
            _bullet(summary.hallucination_controls),
            "",
            "## Rejected Unsupported Claims",
            _bullet(summary.rejected_unsupported_claims or []),
            "",
            "## Baseline Comparison",
            baseline,
            "",
            "## Evidence Integrity",
            summary.evidence_integrity,
            "",
            "## Limits",
            _bullet(summary.limits),
        ]
    )


def render_judge_summary(package: OutputPackageInput) -> str:
    first_finding = package.confirmed_findings[0].finding_id if package.confirmed_findings else "no confirmed finding"
    first_evidence = package.evidence_book[0].evidence_ref if package.evidence_book else "no evidence entry"
    correction_pointer = "correction_ledger.md" if package.correction_entries else "no correction event recorded"
    return "\n".join(
        [
            "# Judge Summary",
            "",
            "## Inspect first",
            "- final_analyst_report.md",
            "- evidence_book.md",
            "- correction_ledger.md",
            "- real_run_accuracy_report.md",
            "- execution_log_review.md",
            "",
            "## Self-correction",
            f"Self-correction appears in `{correction_pointer}` and rejected claim handling.",
            "",
            "## Evidence chain",
            f"Start with `{first_finding}` and evidence reference `{first_evidence}`.",
            "",
            "## Real-run status",
            "Use the accuracy report and dataset documentation together; synthetic fixture material is historical only.",
        ]
    )


def render_reviewer_glossary() -> str:
    terms = {
        "Evidence source": "The original case data or derived artifact that supports a claim.",
        "Claim": "A candidate analytical statement that must be verified before it can become a finding.",
        "Finding": "A claim promoted into the report after evidence review.",
        "Inferred": "A finding with support, but with remaining uncertainty that must stay visible.",
        "Unsupported": "A claim that lacks enough evidence and must not appear as confirmed.",
        "Parser failure": "A tool or parser result that is missing, partial, unreadable or degraded.",
        "Spoliation": "Any change to original evidence that could damage evidentiary integrity.",
    }
    blocks = ["# Reviewer Glossary"]
    for term, definition in terms.items():
        blocks.append(f"## {term}\n{definition}")
    return "\n\n".join(blocks)


def validate_report_quality(report: str) -> QualityGateResult:
    lower = report.lower()
    blockers: list[str] = []
    if "raw log" in lower or "execute_shell_cmd output" in lower or ".jsonl" in lower:
        blockers.append("raw_log_dump")
    if (
        "confirmed evil without evidence" in lower
        or "confirmed without supporting evidence" in lower
        or ("without evidence" in lower and "confirmed" in lower)
    ):
        blockers.append("unsupported_confident_language")
    for required in ("Executive Summary", "Confirmed Findings", "Rejected Claims", "Limitations"):
        if required not in report:
            blockers.append(f"missing_section:{required}")
    return QualityGateResult(passed=not blockers, blockers=blockers)


def validate_evidence_book_quality(
    entries: list[EvidenceBookEntry],
    confirmed_findings: list[Finding],
) -> QualityGateResult:
    blockers: list[str] = []
    if confirmed_findings and not entries:
        blockers.append("missing_evidence_book_entries")
    for entry in entries:
        if not entry.evidence_ref.strip():
            blockers.append("missing_evidence_reference")
        if not entry.source_reference.strip():
            blockers.append("missing_source_reference")
        if not entry.extraction_action.strip():
            blockers.append("missing_extraction_action")
        if "source says" in f"{entry.source_reference} {entry.review_notes}".lower():
            blockers.append("ambiguous_source_language")
    entry_links = {(entry.finding_id, entry.evidence_ref) for entry in entries}
    for finding in confirmed_findings:
        if not finding.evidence_refs:
            blockers.append(f"confirmed_finding_without_evidence:{finding.finding_id}")
            continue
        if not any((finding.finding_id, ref) in entry_links for ref in finding.evidence_refs):
            blockers.append(f"missing_confirmed_finding_link:{finding.finding_id}")
    return QualityGateResult(passed=not blockers, blockers=sorted(set(blockers)))


def validate_correction_ledger_quality(entries: list[CorrectionLedgerEntry]) -> QualityGateResult:
    blockers: list[str] = []
    if not entries:
        blockers.append("missing_visible_correction")
    staged_markers = ("fake", "staged", "demo correction", "scripted correction")
    for entry in entries:
        if not entry.reason_challenged.strip():
            blockers.append("missing_challenge_reason")
        if not entry.follow_up_action.strip():
            blockers.append("missing_follow_up_action")
        text = f"{entry.original_candidate} {entry.reason_challenged} {entry.follow_up_action}".lower()
        if any(marker in text for marker in staged_markers):
            blockers.append("staged_correction_language")
    return QualityGateResult(passed=not blockers, blockers=sorted(set(blockers)))


def render_quality_gate_summary(package: OutputPackageInput, final_report: str) -> str:
    checks = {
        "report_quality": validate_report_quality(final_report),
        "evidence_book_quality": validate_evidence_book_quality(package.evidence_book, package.confirmed_findings),
        "correction_ledger_quality": validate_correction_ledger_quality(package.correction_entries),
    }
    blocks = ["# Quality Gate Summary"]
    for name, result in checks.items():
        blocks.append(
            "\n".join(
                [
                    f"## {name}",
                    f"Passed: {str(result.passed).lower()}",
                    "Blockers:",
                    _bullet(result.blockers),
                ]
            )
        )
    return "\n\n".join(blocks)


def render_execution_log_review(execution_steps: list[dict[str, object]]) -> str:
    blocks = ["# Execution Log Review Surface"]
    for step in execution_steps:
        blocks.append(
            "\n".join(
                [
                    f"- Step: {step.get('step_number', 'unknown')}",
                    f"  - Tool: {step.get('tool_name', 'unknown')}",
                    f"  - Claim: {step.get('claim_id', 'unlinked')}",
                    f"  - Evidence: {step.get('evidence_ref', 'unlinked')}",
                ]
            )
        )
    if len(blocks) == 1:
        blocks.append("No execution steps recorded.")
    return "\n\n".join(blocks)


def render_traceability_chain(
    *,
    finding_id: str,
    claim_id: str,
    evidence_ref: str,
    execution_action: str,
    source_reference: str,
) -> str:
    return f"{finding_id} -> {claim_id} -> {evidence_ref} -> {execution_action} -> {source_reference}"


def generate_output_package(package: OutputPackageInput) -> OutputPackageResult:
    package.output_dir.mkdir(parents=True, exist_ok=True)
    files = {key: package.output_dir / name for key, name in OUTPUT_FILENAMES.items()}
    final_report = render_final_analyst_report(package)
    rendered = {
        "final_analyst_report": final_report,
        "evidence_book": render_evidence_book(package.evidence_book),
        "correction_ledger": render_correction_ledger(package.correction_entries),
        "real_run_accuracy_report": render_real_run_accuracy_report(package.accuracy),
        "execution_log_review": render_execution_log_review(package.execution_steps),
        "judge_summary": render_judge_summary(package),
        "reviewer_glossary": render_reviewer_glossary(),
        "quality_gate_summary": render_quality_gate_summary(package, final_report),
    }
    for key, text in rendered.items():
        files[key].write_text(public_safe_redact(text), encoding="utf-8")

    index: dict[str, object] = {
        key: path.name for key, path in files.items() if key != "artifact_index"
    }
    index["case_id"] = package.case_id
    index["synthetic_historical_fixture"] = package.synthetic_historical_path
    index["stable_entrypoints"] = {
        "readme": "README.md",
        "dataset_documentation": "docs/dataset_documentation.md",
        "accuracy_report": files["real_run_accuracy_report"].name,
        "final_report": files["final_analyst_report"].name,
        "evidence_book": files["evidence_book"].name,
        "correction_ledger": files["correction_ledger"].name,
        "execution_log_review": files["execution_log_review"].name,
        "judge_summary": files["judge_summary"].name,
    }
    index["traceability_chains"] = [
        render_traceability_chain(
            finding_id=entry.finding_id,
            claim_id=entry.finding_id,
            evidence_ref=entry.evidence_ref,
            execution_action=entry.extraction_action,
            source_reference=entry.source_reference,
        )
        for entry in package.evidence_book
    ]
    index["inputs"] = {
        "confirmed_findings": [asdict(item) for item in package.confirmed_findings],
        "inferred_findings": [asdict(item) for item in package.inferred_findings],
    }
    files["artifact_index"].write_text(
        public_safe_redact(json.dumps(index, indent=2, ensure_ascii=True)),
        encoding="utf-8",
    )
    return OutputPackageResult(created_files=files)
