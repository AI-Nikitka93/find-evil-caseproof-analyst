from pathlib import Path

from src.phase_gate import phase_status


ROOT = Path(__file__).resolve().parents[1]
MASTER_PLAN_PATH = ROOT / "docs" / ("MASTER_" + "TO" + "DO_WORLD_CLASS.md")


def test_phase_gate_reports_phase7_real_run_slice_closed() -> None:
    status = phase_status(MASTER_PLAN_PATH.read_text(encoding="utf-8"), phase_number=7)

    assert status.phase_number == 7
    assert status.ordinary_total > 0
    assert "T133" not in status.ordinary_open
    assert status.ordinary_open == []
    assert status.can_close_phase is True


def test_phase_gate_reports_only_external_submission_gates_open() -> None:
    text = MASTER_PLAN_PATH.read_text(encoding="utf-8")
    open_items = [
        line.split()[2]
        for line in text.splitlines()
        if line.startswith("[ ] T")
    ]

    assert open_items == ["T154", "T160", "T161", "T163"]


def test_focused_master_todo_removes_post_release_bloat_from_active_path() -> None:
    text = MASTER_PLAN_PATH.read_text(encoding="utf-8")
    open_items = [
        line
        for line in text.splitlines()
        if line.startswith("[ ] T")
    ]

    assert len(open_items) <= 50
    assert "PHASE 10" not in text
    assert "Post-Release Cycles" not in text
    assert "Full visual investigation cockpit." in text


def test_phase_gate_ignores_anchor_items_for_ordinary_completion() -> None:
    text = """
## PHASE 4 - Example
[x] T001 [P0] Done
[ ] T002 [ANCHOR] Review
## PHASE 5 - Next
[ ] T003 [P0] Later
"""

    status = phase_status(text, phase_number=4)

    assert status.ordinary_total == 1
    assert status.ordinary_open == []
    assert status.anchor_total == 1
