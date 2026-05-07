from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REQUIRED_DESIGN_SECTIONS = (
    "Product Summary",
    "Design Principle",
    "Visual Direction",
    "Color Palette",
    "Typography",
    "Information Hierarchy",
    "Report Surfaces",
    "Diagrams",
    "States And Edge Cases",
    "Stitch Usage",
    "Non-goals",
)

REQUIRED_DESIGN_MARKERS = (
    "forensic clarity over decorative AI dashboard",
    "evidence-first reading",
    "trust through hierarchy",
    "plastic AI dashboard",
    "Google Stitch",
    "Final Analyst Report",
    "Evidence Book",
    "Correction Ledger",
    "Real Run Accuracy Report",
)

REQUIRED_RESEARCH_MARKERS = (
    "google-labs-code/design.md",
    "VoltAgent/awesome-design-md",
    "kzhrknt/awesome-design-md-jp",
    "bergside/awesome-design-skills",
    "shaom/brand-to-design-md-skill",
    "hasi98/designpull",
    "aboul3ata/lazyweb-skill",
    "Lazyweb stop condition",
    "non-copying",
    "forensic clarity",
)

SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}", re.IGNORECASE),
)


@dataclass(frozen=True, slots=True)
class DesignAuditCheck:
    name: str
    ok: bool
    detail: str


@dataclass(frozen=True, slots=True)
class DesignAuditReport:
    status: str
    checks: list[DesignAuditCheck]
    failed_checks: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "checks": [asdict(check) for check in self.checks],
            "failed_checks": self.failed_checks,
        }


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _contains_secret(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def _missing_markers(text: str, markers: tuple[str, ...]) -> list[str]:
    lowered = text.lower()
    return [marker for marker in markers if marker.lower() not in lowered]


def audit_design_package(root: Path) -> DesignAuditReport:
    checks: list[DesignAuditCheck] = []
    design_path = root / "DESIGN.md"
    research_path = root / "docs" / "design_research_note_2026-05-06.md"

    design_exists = design_path.is_file()
    checks.append(
        DesignAuditCheck(
            name="design_md_exists",
            ok=design_exists,
            detail="DESIGN.md exists" if design_exists else "DESIGN.md is missing",
        )
    )
    design_text = _read(design_path) if design_exists else ""

    missing_sections = [section for section in REQUIRED_DESIGN_SECTIONS if f"## {section}" not in design_text]
    checks.append(
        DesignAuditCheck(
            name="design_md_sections",
            ok=not missing_sections,
            detail="missing: " + ", ".join(missing_sections) if missing_sections else "required Stitch-ready sections exist",
        )
    )

    missing_markers = _missing_markers(design_text, REQUIRED_DESIGN_MARKERS)
    checks.append(
        DesignAuditCheck(
            name="design_md_forensic_identity",
            ok=not missing_markers,
            detail="missing: " + ", ".join(missing_markers) if missing_markers else "forensic identity and report surfaces are explicit",
        )
    )

    hex_colors = set(re.findall(r"#[0-9A-Fa-f]{6}\b", design_text))
    checks.append(
        DesignAuditCheck(
            name="design_md_tokens",
            ok=len(hex_colors) >= 6 and "components:" in design_text and "typography:" in design_text,
            detail=f"hex_colors={len(hex_colors)}, components={'components:' in design_text}, typography={'typography:' in design_text}",
        )
    )

    research_exists = research_path.is_file()
    checks.append(
        DesignAuditCheck(
            name="design_research_note_exists",
            ok=research_exists,
            detail="design research note exists" if research_exists else "design research note is missing",
        )
    )
    research_text = _read(research_path) if research_exists else ""

    missing_research = _missing_markers(research_text, REQUIRED_RESEARCH_MARKERS)
    checks.append(
        DesignAuditCheck(
            name="design_research_sources",
            ok=not missing_research,
            detail="missing: " + ", ".join(missing_research) if missing_research else "required design-to-code and Lazyweb coverage exists",
        )
    )

    combined = design_text + "\n" + research_text
    checks.append(
        DesignAuditCheck(
            name="design_no_public_secrets",
            ok=not _contains_secret(combined),
            detail="no obvious token values found" if not _contains_secret(combined) else "secret-like value found",
        )
    )

    failed = [check.name for check in checks if not check.ok]
    return DesignAuditReport(status="ok" if not failed else "blocked", checks=checks, failed_checks=failed)
