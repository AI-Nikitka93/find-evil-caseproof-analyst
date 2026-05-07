from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REQUIRED_VISUAL_STATES = (
    "evidence",
    "correction",
    "verified",
    "inferred",
    "unsupported",
    "blocked_unsafe_action",
    "human_review",
)

README_REQUIRED_ORDER = (
    "## Promise",
    "## Quick Status",
    "## Real Validation Status",
    "## What It Does",
    "## Try-It-Out Instructions",
    "## Key Artifacts",
    "## Current Limitations",
    "## Contribution Path",
)

DEGRADED_STATE_MARKERS = (
    "No evidence file",
    "Missing SIFT runtime",
    "No confirmed finding",
    "Partial parser output",
    "Unsupported claim",
    "Blocked unsafe action",
)
FORBIDDEN_PUBLIC_PLACEHOLDER_MARKERS = (
    "placeholder",
    "TODO",
    "later implementation",
    "future work",
    "fake backend",
    "mock system",
    "simulated integration",
)


@dataclass(frozen=True, slots=True)
class VisualState:
    state: str
    label: str
    symbol: str
    color_token: str
    evidence_rule: str
    usage: str


@dataclass(frozen=True, slots=True)
class VisualAuditCheck:
    name: str
    ok: bool
    detail: str


@dataclass(frozen=True, slots=True)
class VisualAuditReport:
    status: str
    checks: list[VisualAuditCheck]
    failed_checks: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "checks": [asdict(check) for check in self.checks],
            "failed_checks": self.failed_checks,
        }


def visual_state_catalog() -> list[VisualState]:
    return [
        VisualState("evidence", "Evidence", "EVD", "trace", "Must point to a source reference.", "Evidence book records and trace links."),
        VisualState("correction", "Correction", "COR", "caution-fill", "Must show the challenged claim and final outcome.", "Correction ledger rows."),
        VisualState("verified", "Verified", "VER", "verified", "Allowed only after evidence-linked verification.", "Confirmed finding labels."),
        VisualState("inferred", "Inferred", "INF", "inferred", "Requires support plus visible uncertainty.", "Supported but uncertain findings."),
        VisualState("unsupported", "Unsupported", "UNS", "unsupported", "Must not appear as a confirmed finding.", "Rejected or dropped claims."),
        VisualState("blocked_unsafe_action", "Blocked Unsafe Action", "BLK", "blocked", "Must name the unavailable unsafe capability.", "Spoliation and refusal states."),
        VisualState("human_review", "Human Review", "HRV", "blocked", "Requires analyst review before promotion.", "Ambiguous or degraded evidence states."),
    ]


def render_trust_boundary_diagram() -> str:
    return "\n".join(
        [
            "```mermaid",
            "flowchart LR",
            '    Evidence["Original Evidence<br/>input-only disk image"] --> Open["case_open_readonly"]',
            '    Open --> Server["Custom MCP Server<br/>eight fixed tools"]',
            '    Agent["AI Agent<br/>bounded loop"] <-->|"MCP stdio"| Server',
            '    Server --> Tools["Read-only forensic tools<br/>mmls, fls, timeline, registry, events"]',
            '    Tools --> Workspace["Generated case workspace<br/>reports, logs, derived artifacts"]',
            '    Workspace --> Outputs["Final outputs<br/>report, evidence book, correction ledger, accuracy report, logs"]',
            '    Unsafe["Unsafe mutation request<br/>delete, overwrite, raw shell"] -. "not routable" .-> Boundary["Safety boundary"]',
            '    Evidence -. "never written by product" .-> Boundary',
            "```",
        ]
    )


def render_evidence_chain_diagram() -> str:
    return "\n".join(
        [
            "```mermaid",
            "flowchart LR",
            '    Finding["Final Finding"] --> Claim["Candidate Claim"]',
            '    Claim --> Evidence["Evidence Record"]',
            '    Evidence --> Action["Execution Action"]',
            '    Action --> Source["Source Reference"]',
            '    Source --> Review["Reviewer can replay or inspect"]',
            "```",
        ]
    )


def render_correction_loop_diagram() -> str:
    return "\n".join(
        [
            "```mermaid",
            "flowchart LR",
            '    Unsupported["Unsupported Candidate Claim"] --> Challenge["Verifier Challenge"]',
            '    Challenge --> Followup["Targeted Follow-up"]',
            '    Followup --> Corrected["Corrected"]',
            '    Followup --> Downgraded["Downgraded"]',
            '    Followup --> Dropped["Dropped"]',
            '    Followup --> Human["Needs Human Review"]',
            "```",
        ]
    )


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def _ordered_markers(text: str, markers: tuple[str, ...]) -> tuple[bool, str]:
    positions: list[int] = []
    missing: list[str] = []
    for marker in markers:
        pos = text.find(marker)
        if pos < 0:
            missing.append(marker)
        positions.append(pos)
    if missing:
        return False, "missing: " + ", ".join(missing)
    if positions != sorted(positions):
        return False, "markers are out of order"
    return True, "required hierarchy is present"


def _contains_all(text: str, markers: tuple[str, ...]) -> tuple[bool, str]:
    missing = [marker for marker in markers if marker not in text]
    return (not missing, "missing: " + ", ".join(missing) if missing else "all markers present")


def audit_visual_package(root: Path) -> VisualAuditReport:
    checks: list[VisualAuditCheck] = []
    readme = _read(root / "README.md")
    design = _read(root / "DESIGN.md")
    architecture = _read(root / "docs" / "architecture.md")
    asset_policy = _read(root / "docs" / "visual_asset_policy.md")
    demo_notes = _read(root / "docs" / "demo_narration_notes.md")
    visual_qa = _read(root / "docs" / "visual_qa_checklist.md")

    ok, detail = _ordered_markers(readme, README_REQUIRED_ORDER)
    checks.append(VisualAuditCheck("readme_information_hierarchy", ok, detail))

    state_markers = tuple(state.label for state in visual_state_catalog())
    ok, detail = _contains_all(design + "\n" + asset_policy, state_markers)
    checks.append(VisualAuditCheck("iconography_state_coverage", ok, detail))

    ok, detail = _contains_all(
        asset_policy,
        (
            "Reference search",
            "Style brief",
            "Individual generation",
            "Manual curation",
            "AI critique",
            "Rejection rule",
            "Fallback no-AI visual plan",
        ),
    )
    checks.append(VisualAuditCheck("visual_asset_production_cycle", ok, detail))

    diagrams_ok, diagrams_detail = _contains_all(
        architecture,
        (
            "Judge-Readable Trust Boundary Diagram",
            "Evidence Chain Diagram",
            "Correction Loop Diagram",
            "Original Evidence",
            "Final Finding",
            "Verifier Challenge",
        ),
    )
    checks.append(VisualAuditCheck("architecture_diagrams", diagrams_ok, diagrams_detail))

    ok, detail = _contains_all(readme + "\n" + design + "\n" + demo_notes, DEGRADED_STATE_MARKERS)
    checks.append(VisualAuditCheck("empty_degraded_states", ok, detail))

    visual_language_ok = all(
        marker in (readme + "\n" + design + "\n" + architecture + "\n" + demo_notes)
        for marker in ("forensic clarity", "evidence-first", "no decorative dashboard")
    )
    checks.append(
        VisualAuditCheck(
            "cross_surface_visual_language",
            visual_language_ok,
            "shared forensic visual language is present" if visual_language_ok else "shared visual language marker missing",
        )
    )

    bad_markers = re.findall(r"(?i)plastic ai dashboard|green status theater|fake command center", readme + "\n" + architecture + "\n" + demo_notes)
    checks.append(
        VisualAuditCheck(
            "no_public_decorative_dashboard_promise",
            not bad_markers,
            "no public decorative-dashboard wording found" if not bad_markers else "public anti-pattern wording leaked: " + ", ".join(sorted(set(bad_markers))),
        )
    )

    qa_ok, qa_detail = _contains_all(
        visual_qa,
        (
            "No clipped text",
            "Diagrams readable in repository view",
            "No decorative clutter",
            "No misleading green status",
            "No visual masking",
        ),
    )
    checks.append(VisualAuditCheck("visual_qa_checklist", qa_ok, qa_detail))

    no_mask_ok = "Visual polish cannot close, hide, or soften real SIFT validation blockers" in visual_qa
    checks.append(
        VisualAuditCheck(
            "visual_layer_does_not_mask_validation",
            no_mask_ok,
            "visual no-mask rule is explicit" if no_mask_ok else "visual no-mask rule missing",
        )
    )

    public_visual_docs = readme + "\n" + architecture + "\n" + asset_policy + "\n" + demo_notes + "\n" + visual_qa
    placeholder_hits = [
        marker
        for marker in FORBIDDEN_PUBLIC_PLACEHOLDER_MARKERS
        if marker.lower() in public_visual_docs.lower()
    ]
    checks.append(
        VisualAuditCheck(
            "no_public_placeholder_markers",
            not placeholder_hits,
            "no public placeholder markers found" if not placeholder_hits else "hits: " + ", ".join(placeholder_hits),
        )
    )

    failed = [check.name for check in checks if not check.ok]
    return VisualAuditReport(status="ok" if not failed else "blocked", checks=checks, failed_checks=failed)
