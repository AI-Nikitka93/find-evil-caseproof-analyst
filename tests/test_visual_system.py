from pathlib import Path

from src.visual_system import (
    REQUIRED_VISUAL_STATES,
    audit_visual_package,
    render_correction_loop_diagram,
    render_evidence_chain_diagram,
    render_trust_boundary_diagram,
    visual_state_catalog,
)


ROOT = Path(__file__).resolve().parents[1]


def test_visual_state_catalog_covers_required_forensic_states() -> None:
    catalog = visual_state_catalog()
    states = {item.state for item in catalog}
    symbols = [item.symbol for item in catalog]

    assert states == set(REQUIRED_VISUAL_STATES)
    assert all(item.label and item.evidence_rule and item.usage for item in catalog)
    assert len(symbols) == len(set(symbols))


def test_mermaid_diagrams_are_repository_readable_and_not_placeholders() -> None:
    diagrams = [
        render_trust_boundary_diagram(),
        render_evidence_chain_diagram(),
        render_correction_loop_diagram(),
    ]

    for diagram in diagrams:
        assert diagram.startswith("```mermaid\nflowchart LR")
        assert "placeholder" not in diagram.lower()
        assert "TODO" not in diagram

    assert "Original Evidence" in diagrams[0]
    assert "Final Finding" in diagrams[1]
    assert "Verifier Challenge" in diagrams[2]


def test_visual_package_audit_passes_current_project() -> None:
    report = audit_visual_package(ROOT)

    assert report.status == "ok", report.failed_checks


def test_visual_package_audit_blocks_missing_readme_hierarchy(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "README.md").write_text("# README\n", encoding="utf-8")
    (tmp_path / "DESIGN.md").write_text("# DESIGN.md\n", encoding="utf-8")
    (tmp_path / "docs" / "architecture.md").write_text("", encoding="utf-8")
    (tmp_path / "docs" / "visual_asset_policy.md").write_text("", encoding="utf-8")
    (tmp_path / "docs" / "demo_narration_notes.md").write_text("", encoding="utf-8")
    (tmp_path / "docs" / "visual_qa_checklist.md").write_text("", encoding="utf-8")

    report = audit_visual_package(tmp_path)

    assert report.status == "blocked"
    assert "readme_information_hierarchy" in report.failed_checks
    assert "visual_qa_checklist" in report.failed_checks


def test_visual_package_audit_blocks_public_placeholder_markers(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "README.md").write_text(
        "\n".join(
            [
                "## Promise",
                "forensic clarity evidence-first no decorative dashboard",
                "## Quick Status",
                "placeholder",
                "## Real Validation Status",
                "No evidence file Missing SIFT runtime No confirmed finding Partial parser output Unsupported claim Blocked unsafe action",
                "## What It Does",
                "## Try-It-Out Instructions",
                "## Key Artifacts",
                "## Current Limitations",
                "## Contribution Path",
            ]
        ),
        encoding="utf-8",
    )
    (tmp_path / "DESIGN.md").write_text(
        "Evidence Correction Verified Inferred Unsupported Blocked Unsafe Action Human Review",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "architecture.md").write_text(
        "Judge-Readable Trust Boundary Diagram Evidence Chain Diagram Correction Loop Diagram Original Evidence Final Finding Verifier Challenge",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "visual_asset_policy.md").write_text(
        "Evidence Correction Verified Inferred Unsupported Blocked Unsafe Action Human Review Reference search Style brief Individual generation Manual curation AI critique Rejection rule Fallback no-AI visual plan",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "demo_narration_notes.md").write_text("", encoding="utf-8")
    (tmp_path / "docs" / "visual_qa_checklist.md").write_text(
        "No clipped text Diagrams readable in repository view No decorative clutter No misleading green status No visual masking Visual polish cannot close, hide, or soften real SIFT validation blockers",
        encoding="utf-8",
    )

    report = audit_visual_package(tmp_path)

    assert report.status == "blocked"
    assert "no_public_placeholder_markers" in report.failed_checks
