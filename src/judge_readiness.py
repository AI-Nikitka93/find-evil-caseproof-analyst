from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from scripts.final_submission_audit import GitSyncStatus, build_final_submission_audit

from .real_validation import (
    validate_correlation_summary,
    validate_final_report_evidence_links,
)


CRITERIA = (
    "Autonomous Execution Quality",
    "IR Accuracy",
    "Breadth And Depth",
    "Constraint Implementation",
    "Audit Trail Quality",
    "Usability And Documentation",
)
PUBLIC_TOOL_NAMES = (
    "case_open_readonly",
    "list_partitions",
    "filesystem_inventory",
    "build_timeline",
    "extract_registry_persistence",
    "extract_event_records",
    "verify_claim",
    "write_execution_log",
)


@dataclass(frozen=True, slots=True)
class ProofPoint:
    name: str
    ok: bool
    detail: str


@dataclass(frozen=True, slots=True)
class CriterionAssessment:
    criterion: str
    score: int
    max_score: int
    proof_points: list[ProofPoint]
    gaps: list[str]


def _read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _json(path: Path) -> Any:
    try:
        return json.loads(_read(path))
    except json.JSONDecodeError:
        return None


def _jsonl_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in _read(path).splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            return []
        if isinstance(payload, dict):
            records.append(payload)
    return records


def _score(proof_points: list[ProofPoint]) -> int:
    if not proof_points:
        return 0
    passed = sum(1 for point in proof_points if point.ok)
    return round(17 * passed / len(proof_points))


def _assessment(criterion: str, proof_points: list[ProofPoint]) -> CriterionAssessment:
    gaps = [point.name for point in proof_points if not point.ok]
    return CriterionAssessment(
        criterion=criterion,
        score=_score(proof_points),
        max_score=17,
        proof_points=proof_points,
        gaps=gaps,
    )


def _point(name: str, ok: bool, detail: str) -> ProofPoint:
    return ProofPoint(name=name, ok=ok, detail=detail)


def _trace_facts(root: Path) -> dict[str, Any]:
    records = _jsonl_records(root / "docs" / "public_real_execution_log_sample.jsonl")
    tools = {str(record.get("tool_name", "")) for record in records}
    return {
        "records": records,
        "tools": tools,
        "has_open": "case_open_readonly" in tools,
        "has_verifier": "verify_claim" in tools,
        "has_correction": any(bool(record.get("correction_reason")) for record in records),
        "has_registry_or_event": bool({"extract_registry_persistence", "extract_event_records"} & tools),
    }


def _local_final_gates_ok(final_audit: dict[str, Any]) -> bool:
    for name, gate in final_audit.get("local_gates", {}).items():
        if name == "judge_max_readiness_report":
            continue
        if name == "required_files" and gate.get("detail") == "missing: docs/judge_max_readiness_report.md":
            continue
        if not bool(gate.get("ok")):
            return False
    return True


def _submission_blockers_without_bootstrap_self_reference(final_audit: dict[str, Any]) -> list[str]:
    blockers = list(final_audit.get("blockers", []))
    local_gates = final_audit.get("local_gates", {})
    if local_gates.get("required_files", {}).get("detail") == "missing: docs/judge_max_readiness_report.md":
        blockers = [item for item in blockers if item != "required_files"]
    return [item for item in blockers if item != "judge_max_readiness_report"]


def build_judge_readiness_report(
    *,
    root: Path,
    demo_video_url: str | None = None,
    devpost_url: str | None = None,
    git_status: GitSyncStatus | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    trace = _trace_facts(root)
    final_audit = build_final_submission_audit(
        root=root,
        demo_video_url=demo_video_url,
        devpost_url=devpost_url,
        git_status=git_status,
    )
    final_report_text = _read(root / "cases" / "CASE-RD01" / "reports" / "final_analyst_report.md")
    final_report_links = validate_final_report_evidence_links(final_report_text)
    correlation_payload = _json(root / "cases" / "CASE-RD01" / "exports" / "correlation_summary.json")
    correlation_valid = (
        validate_correlation_summary(correlation_payload).passed if isinstance(correlation_payload, dict) else False
    )
    server_source = _read(root / "src" / "server.py")
    prompt_source = _read(root / "src" / "prompts.py")
    agent_source = _read(root / "src" / "agent.py")
    correction_text = _read(root / "cases" / "CASE-RD01" / "reports" / "correction_ledger.md").lower()

    assessments = [
        _assessment(
            "Autonomous Execution Quality",
            [
                _point("bounded_agent_loop", "MAX_ITERATIONS" in agent_source, "Agent exposes a hard iteration cap."),
                _point("tool_planning_prompt", "verify_claim" in prompt_source, "Prompt requires claim verification."),
                _point("real_tool_sequence_trace", trace["has_open"] and trace["has_verifier"], "Public trace includes case open and verifier calls."),
                _point("visible_self_correction", trace["has_correction"], "Public trace records a correction reason."),
                _point("demo_rehearsal_ready", bool(final_audit["local_gates"].get("demo_rehearsal_assets", {}).get("ok")), "Demo rehearsal assets are locally ready."),
                _point("autonomous_smoke_documented", (root / "docs" / "autonomous_smoke_hardening_2026-05-07.md").is_file(), "Autonomous smoke hardening note exists."),
            ],
        ),
        _assessment(
            "IR Accuracy",
            [
                _point("accuracy_report_present", (root / "docs" / "accuracy_report.md").is_file(), "Accuracy report exists."),
                _point("real_run_accuracy_present", (root / "cases" / "CASE-RD01" / "reports" / "real_run_accuracy_report.md").is_file(), "Real-run accuracy report exists."),
                _point("confirmed_findings_link_evidence", final_report_links.passed, "Confirmed findings carry evidence references."),
                _point("correlation_summary_valid", correlation_valid, "Correlation summary passes validation."),
                _point("compromise_not_overclaimed", isinstance(correlation_payload, dict) and correlation_payload.get("confirmed_compromise") is False, "Compromise disposition is explicit and false."),
                _point("unsupported_claim_dropped", "unsupported" in correction_text and "dropped" in correction_text, "Correction ledger records a dropped unsupported claim."),
            ],
        ),
        _assessment(
            "Breadth And Depth",
            [
                _point("root_inventory_present", (root / "cases" / "CASE-RD01" / "exports" / "root_inventory.json").is_file(), "Root inventory exists."),
                _point("high_signal_inventory_present", (root / "cases" / "CASE-RD01" / "exports" / "high_signal_inventory.json").is_file(), "High-signal inventory exists."),
                _point("registry_content_present", (root / "cases" / "CASE-RD01" / "exports" / "registry_content_summary.json").is_file(), "Registry content summary exists."),
                _point("event_content_present", (root / "cases" / "CASE-RD01" / "exports" / "event_content_summary.json").is_file(), "Event content summary exists."),
                _point("cross_artifact_correlation_present", correlation_valid, "Registry/event correlation exists and validates."),
                _point("timeline_anchor_or_limitation_present", bool(correlation_payload.get("timeline_anchors")) if isinstance(correlation_payload, dict) else False, "Timeline anchors are preserved in bounded correlation."),
                _point("replay_consistency_present", (root / "cases" / "CASE-RD01" / "reports" / "replay_consistency.md").is_file(), "Replay consistency report exists."),
            ],
        ),
        _assessment(
            "Constraint Implementation",
            [
                _point("all_public_tool_names_present", all(f"def {name}" in server_source for name in PUBLIC_TOOL_NAMES), "Eight public MCP tool names are present."),
                _point("no_generic_shell", "shell=True" not in server_source, "Server source does not enable shell=True."),
                _point("subprocess_is_allowlisted_style", "subprocess.run(" in server_source and "check=False" in server_source, "Subprocess execution is explicit and non-throwing."),
                _point("architecture_doc_present", (root / "docs" / "architecture.md").is_file(), "Architecture doc exists."),
                _point("mcp_architecture_doc_present", (root / "docs" / "mcp_architecture.md").is_file(), "MCP architecture doc exists."),
                _point("trust_boundary_doc_present", (root / "docs" / "trust_boundary_contract.md").is_file(), "Trust boundary contract exists."),
                _point("final_submission_audit_exists", (root / "scripts" / "final_submission_audit.py").is_file(), "Final submission audit script exists."),
            ],
        ),
        _assessment(
            "Audit Trail Quality",
            [
                _point("public_jsonl_trace_parseable", bool(trace["records"]), "Public JSONL trace parses."),
                _point("trace_includes_open_verify_correction", trace["has_open"] and trace["has_verifier"] and trace["has_correction"], "Trace includes open, verify, and correction."),
                _point("trace_includes_artifact_depth", trace["has_registry_or_event"], "Trace includes registry or event depth."),
                _point("public_trace_packet_present", (root / "docs" / "public_real_traceability_packet.md").is_file(), "Public trace packet exists."),
                _point("reviewer_walkthrough_present", (root / "docs" / "reviewer_traceability_walkthrough.md").is_file(), "Reviewer walkthrough exists."),
                _point("local_execution_log_parseable", bool(_jsonl_records(root / "cases" / "CASE-RD01" / "logs" / "agent_execution.jsonl")), "Local execution log parses."),
                _point("evidence_book_present", (root / "cases" / "CASE-RD01" / "reports" / "evidence_book.md").is_file(), "Evidence book exists."),
            ],
        ),
        _assessment(
            "Usability And Documentation",
            [
                _point("readme_present", (root / "README.md").is_file(), "README exists."),
                _point("judge_runbook_present", (root / "docs" / "judge_try_it_out.md").is_file(), "Judge try-it-out runbook exists."),
                _point("submission_package_present", (root / "docs" / "final_submission_package.md").is_file(), "Devpost paste package exists."),
                _point("dataset_documentation_present", (root / "docs" / "dataset_documentation.md").is_file(), "Dataset documentation exists."),
                _point("demo_script_present", (root / "docs" / "demo_video_script.md").is_file(), "Demo script exists."),
                _point("narration_notes_present", (root / "docs" / "demo_narration_notes.md").is_file(), "Narration notes exist."),
                _point("demo_rehearsal_script_present", (root / "scripts" / "demo_rehearsal.py").is_file(), "Demo rehearsal script exists."),
            ],
        ),
    ]
    score_map = {assessment.criterion: assessment.score for assessment in assessments}
    submission_blockers = _submission_blockers_without_bootstrap_self_reference(final_audit)
    return {
        "status": "max_local_judge_ready" if all(score == 17 for score in score_map.values()) else "needs_work",
        "criterion_score_summary": {
            "all_criteria_at_17": all(score == 17 for score in score_map.values()),
            "scores": score_map,
            "total": sum(score_map.values()),
            "max_total": 17 * len(CRITERIA),
        },
        "criteria": [asdict(assessment) for assessment in assessments],
        "submission_gate": {
            "status": "ready" if not submission_blockers else "blocked",
            "score": final_audit["score"],
            "blockers": submission_blockers,
            "external_gates": final_audit["external_gates"],
        },
        "boundary": (
            "A 17/17 local criterion map is not the same as final Devpost submission. "
            "Public demo video and submitted Devpost URL remain external gates until supplied."
        ),
    }


def render_judge_readiness_markdown(report: dict[str, Any]) -> str:
    summary = report["criterion_score_summary"]
    lines = [
        "# Judge Max Readiness Report",
        "",
        f"Status: **{report['status']}**",
        "",
        "## Criterion Scorecard",
        "",
        "| Criterion | Score | Gaps |",
        "|---|---:|---|",
    ]
    for criterion in report["criteria"]:
        gaps = ", ".join(criterion["gaps"]) if criterion["gaps"] else "None"
        lines.append(f"| {criterion['criterion']} | {criterion['score']}/17 | {gaps} |")
    lines.extend(
        [
            "",
            f"Total: **{summary['total']}/{summary['max_total']}**",
            f"All criteria at 17/17: **{str(summary['all_criteria_at_17']).lower()}**",
            "",
            "## External submission gate",
            "",
            f"Status: **{report['submission_gate']['status']}**",
            f"Score: **{report['submission_gate']['score']}/100**",
            "Blockers: " + (", ".join(report["submission_gate"]["blockers"]) if report["submission_gate"]["blockers"] else "None"),
            "",
            "## Boundary",
            "",
            report["boundary"],
            "",
        ]
    )
    return "\n".join(lines)
