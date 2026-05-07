from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ConfidenceTarget = Literal["confirmed", "inferred"]
VerifierStatus = Literal["confirmed", "inferred", "unsupported", "needs_human_review"]
FinalStatus = Literal["confirmed", "inferred", "dropped", "corrected", "needs_human_review"]


@dataclass(frozen=True, slots=True)
class CandidateClaim:
    claim_id: str
    artifact_family: str
    observed_fact: str
    evidence_reference_expectation: str
    confidence_target: ConfidenceTarget
    claim_text: str
    evidence_id: str | None = None


@dataclass(frozen=True, slots=True)
class CorrectionLedgerEntry:
    original_candidate: str
    reason_challenged: str
    follow_up_action: str
    final_status: FinalStatus
    evidence_references: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ClaimDecision:
    final_status: FinalStatus
    report_section: str
    ledger_entry: CorrectionLedgerEntry


@dataclass(frozen=True, slots=True)
class EvidenceSignal:
    source: str
    fact_key: str
    fact_value: str


@dataclass(frozen=True, slots=True)
class EvidenceConflict:
    reason: str
    fact_key: str
    values: tuple[str, ...]
    sources: tuple[str, ...]
    final_status: FinalStatus = "needs_human_review"


@dataclass(frozen=True, slots=True)
class AutonomyBudget:
    iteration: int
    max_iterations: int
    tool_calls: int
    tool_call_budget: int


@dataclass(frozen=True, slots=True)
class StopReason:
    kind: str
    analyst_message: str


@dataclass(frozen=True, slots=True)
class RetryDecision:
    allow_retry: bool
    final_status: FinalStatus | None
    analyst_message: str


@dataclass(frozen=True, slots=True)
class ParserUncertainty:
    artifact_family: str
    parser_status: str
    final_status: FinalStatus
    report_section: str
    analyst_message: str


def draft_claim(
    *,
    claim_id: str,
    artifact_family: str,
    observed_fact: str,
    evidence_reference_expectation: str,
    confidence_target: ConfidenceTarget,
    evidence_id: str | None = None,
) -> CandidateClaim:
    claim_text = f"{artifact_family}: {observed_fact}"
    return CandidateClaim(
        claim_id=claim_id,
        artifact_family=artifact_family,
        observed_fact=observed_fact,
        evidence_reference_expectation=evidence_reference_expectation,
        confidence_target=confidence_target,
        claim_text=claim_text,
        evidence_id=evidence_id,
    )


def build_controlled_unsupported_claim(
    *,
    evidence_id: str,
    artifact_family: str,
    observed_fact: str,
) -> CandidateClaim:
    return draft_claim(
        claim_id="controlled-unsupported-claim",
        artifact_family=artifact_family,
        observed_fact=observed_fact,
        evidence_reference_expectation="linked evidence reference required before confirmation",
        confidence_target="confirmed",
        evidence_id=evidence_id,
    )


def resolve_claim_verification(
    *,
    claim: CandidateClaim,
    verifier_status: VerifierStatus,
    supporting_evidence: list[str],
) -> ClaimDecision:
    evidence_refs = tuple(supporting_evidence)
    if verifier_status == "confirmed" and evidence_refs:
        final_status: FinalStatus = "confirmed"
        section = "Confirmed Findings"
        reason = "verified_with_supporting_evidence"
        follow_up = "none"
    elif verifier_status == "confirmed":
        final_status = "needs_human_review"
        section = "Needs Human Review"
        reason = "missing_support_for_confirmed"
        follow_up = "do not report as confirmed until supporting evidence exists"
    elif verifier_status == "inferred":
        final_status = "inferred"
        section = "Inferred Findings"
        reason = "related_but_incomplete_support"
        follow_up = "label limitation and avoid confirmed language"
    elif verifier_status == "unsupported":
        final_status = "dropped"
        section = "Unsupported Dropped"
        reason = "unsupported_claim"
        follow_up = "record dropped claim in correction ledger"
    else:
        final_status = "needs_human_review"
        section = "Needs Human Review"
        reason = "human_review_required"
        follow_up = "stop before overclaiming"

    return ClaimDecision(
        final_status=final_status,
        report_section=section,
        ledger_entry=CorrectionLedgerEntry(
            original_candidate=claim.claim_text,
            reason_challenged=reason,
            follow_up_action=follow_up,
            final_status=final_status,
            evidence_references=evidence_refs,
        ),
    )


def detect_evidence_conflict(signals: list[EvidenceSignal]) -> EvidenceConflict | None:
    by_fact: dict[str, list[EvidenceSignal]] = {}
    for signal in signals:
        by_fact.setdefault(signal.fact_key, []).append(signal)

    for fact_key, related in by_fact.items():
        values = tuple(sorted({signal.fact_value for signal in related}))
        if len(values) > 1:
            sources = tuple(sorted({signal.source for signal in related}))
            return EvidenceConflict(
                reason="evidence_conflict",
                fact_key=fact_key,
                values=values,
                sources=sources,
            )
    return None


def visible_stop_reason(budget: AutonomyBudget) -> StopReason | None:
    if budget.iteration >= budget.max_iterations:
        return StopReason(
            kind="iteration_budget_exhausted",
            analyst_message="Stopped because the max iteration budget was reached before safe completion.",
        )
    if budget.tool_calls >= budget.tool_call_budget:
        return StopReason(
            kind="tool_call_budget_exhausted",
            analyst_message="Stopped because the tool-call budget was reached before safe completion.",
        )
    return None


def retry_decision(*, tool_name: str, same_tool_failures: int, max_same_tool_failures: int = 2) -> RetryDecision:
    if same_tool_failures >= max_same_tool_failures:
        return RetryDecision(
            allow_retry=False,
            final_status="needs_human_review",
            analyst_message=(
                f"Stopped retrying {tool_name} because the bounded retry limit was reached; "
                "remaining uncertainty requires human review."
            ),
        )
    return RetryDecision(
        allow_retry=True,
        final_status=None,
        analyst_message=f"One bounded retry is still allowed for {tool_name}.",
    )


def visible_parser_uncertainty(*, artifact_family: str, parser_status: str, tool_name: str) -> ParserUncertainty:
    return ParserUncertainty(
        artifact_family=artifact_family,
        parser_status=parser_status,
        final_status="needs_human_review",
        report_section="Needs Human Review",
        analyst_message=(
            f"{artifact_family} from {tool_name} has parser status {parser_status}; "
            "do not treat this artifact family as complete without review."
        ),
    )


def public_step_rationale(*, next_step: str, reason: str) -> str:
    return f"Next step: {next_step}. Reason: {reason}."
