from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .claim_policy import CorrectionLedgerEntry


OutcomeStatus = Literal["confirmed", "inferred", "dropped", "corrected", "needs_human_review"]
REQUIRED_OUTPUT_NAMES = ("report", "evidence_book", "correction_ledger", "agent_execution")


@dataclass(frozen=True, slots=True)
class RunAcceptanceInput:
    completed: bool
    clear_stop_reason: str | None
    unhandled_claim_ids: list[str]
    correction_events: int
    output_paths: list[str]


@dataclass(frozen=True, slots=True)
class RunAcceptanceResult:
    accepted: bool
    blockers: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class ArtifactOutcome:
    name: str
    status: OutcomeStatus
    evidence_refs: list[str]


@dataclass(frozen=True, slots=True)
class ReviewerQualityChecklist:
    ready: bool
    items: dict[str, bool]
    blockers: list[str] = field(default_factory=list)


def render_correction_ledger(entries: list[CorrectionLedgerEntry]) -> str:
    if not entries:
        return "Correction Ledger\n\nNo correction events recorded."
    blocks = ["Correction Ledger"]
    for index, entry in enumerate(entries, start=1):
        refs = ", ".join(entry.evidence_references) if entry.evidence_references else "none"
        blocks.append(
            "\n".join(
                [
                    f"{index}. Original candidate: {entry.original_candidate}",
                    f"   Reason challenged: {entry.reason_challenged}",
                    f"   Follow-up action: {entry.follow_up_action}",
                    f"   Final status: {entry.final_status}",
                    f"   Evidence references: {refs}",
                ]
            )
        )
    return "\n\n".join(blocks)


def build_no_evil_found_report(*, case_id: str, checked_scope: list[str], remaining_uncertainty: list[str]) -> str:
    scope = "\n".join(f"- {item}" for item in checked_scope) or "- No scope recorded"
    uncertainty = "\n".join(f"- {item}" for item in remaining_uncertainty) or "- No remaining uncertainty recorded"
    return "\n".join(
        [
            "# FIND EVIL Disk Triage Report",
            "",
            f"Case ID: {case_id}",
            "",
            "No confirmed malicious finding was produced.",
            "",
            "Checked scope:",
            scope,
            "",
            "Remaining uncertainty:",
            uncertainty,
            "",
            "This result does not clear the evidence; it only states that no supported malicious finding was confirmed in the checked scope.",
        ]
    )


def render_degraded_artifact_notice(
    *,
    artifact_family: str,
    failed_tool: str,
    why_it_matters: str,
    remaining_unknowns: list[str],
) -> str:
    unknowns = "\n".join(f"- {item}" for item in remaining_unknowns) or "- No unknowns recorded"
    return "\n".join(
        [
            f"Artifact family unavailable: {artifact_family}",
            f"Failed tool: {failed_tool}",
            f"Why it matters: {why_it_matters}",
            "Remaining unknowns:",
            unknowns,
        ]
    )


def evaluate_real_run_acceptance(run: RunAcceptanceInput) -> RunAcceptanceResult:
    blockers: list[str] = []
    if not run.completed and not run.clear_stop_reason:
        blockers.append("missing_clear_stop_reason")
    if run.unhandled_claim_ids:
        blockers.append("unhandled_claims")
    if run.correction_events < 1:
        blockers.append("missing_correction_event")
    present_outputs = {name for name in REQUIRED_OUTPUT_NAMES if any(name in path for path in run.output_paths)}
    if present_outputs != set(REQUIRED_OUTPUT_NAMES):
        blockers.append("missing_required_outputs")
    return RunAcceptanceResult(accepted=not blockers, blockers=blockers)


def build_reviewer_quality_check(
    *,
    sequence_complete: bool,
    failures_visible: bool,
    self_correction_visible: bool,
    bounded_stop: bool,
    final_findings: list[ArtifactOutcome],
) -> ReviewerQualityChecklist:
    unsupported_confirmed = [
        finding.name for finding in final_findings if finding.status == "confirmed" and not finding.evidence_refs
    ]
    items = {
        "sequence_quality": sequence_complete,
        "failure_handling": failures_visible,
        "self_correction": self_correction_visible,
        "boundedness": bounded_stop,
        "no_unsupported_final_claims": not unsupported_confirmed,
    }
    blockers = [f"Confirmed finding lacks evidence support: {name}" for name in unsupported_confirmed]
    for item, passed in items.items():
        if not passed and item != "no_unsupported_final_claims":
            blockers.append(f"Reviewer checklist failed: {item}")
    return ReviewerQualityChecklist(ready=all(items.values()), items=items, blockers=blockers)
