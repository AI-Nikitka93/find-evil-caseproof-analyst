from pathlib import Path

from src.design_quality import audit_design_package


ROOT = Path(__file__).resolve().parents[1]


def test_design_package_is_complete_for_phase6_opening_slice() -> None:
    report = audit_design_package(ROOT)

    assert report.status == "ok", report.failed_checks


def test_design_audit_blocks_missing_stitch_ready_sections(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "DESIGN.md").write_text(
        "# DESIGN.md\n\n## Product Summary\nForensic clarity over decorative AI dashboard.\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "design_research_note_2026-05-06.md").write_text(
        "Lazyweb stop condition and google-labs-code/design.md.",
        encoding="utf-8",
    )

    report = audit_design_package(tmp_path)

    assert report.status == "blocked"
    assert "design_md_sections" in report.failed_checks


def test_design_audit_blocks_research_without_required_source_coverage(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "DESIGN.md").write_text(
        "\n".join(
            [
                "# DESIGN.md",
                "Forensic clarity over decorative AI dashboard.",
                "Evidence-first reading.",
                "Trust through hierarchy.",
                "## Product Summary",
                "## Design Principle",
                "## Visual Direction",
                "## Color Palette",
                "## Typography",
                "## Information Hierarchy",
                "## Report Surfaces",
                "## Diagrams",
                "## States And Edge Cases",
                "## Stitch Usage",
                "## Non-goals",
            ]
        ),
        encoding="utf-8",
    )
    (tmp_path / "docs" / "design_research_note_2026-05-06.md").write_text(
        "A vague moodboard without source coverage.",
        encoding="utf-8",
    )

    report = audit_design_package(tmp_path)

    assert report.status == "blocked"
    assert "design_research_sources" in report.failed_checks
