from __future__ import annotations

import re
from dataclasses import dataclass


TASK_RE = re.compile(r"^\[(?P<mark>[ x])\]\s+T(?P<id>\d{3})\s+\[(?P<priority>[^\]]+)\]\s+(?P<title>.+)$")
PHASE_RE = re.compile(r"^## PHASE\s+(?P<number>\d+)\b", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class PhaseStatus:
    phase_number: int
    ordinary_total: int
    ordinary_open: list[str]
    anchor_total: int
    anchor_open: list[str]

    @property
    def can_close_phase(self) -> bool:
        return self.ordinary_total > 0 and not self.ordinary_open


def _phase_lines(todo_text: str, phase_number: int) -> list[str]:
    lines = todo_text.splitlines()
    start: int | None = None
    end = len(lines)
    for index, line in enumerate(lines):
        match = PHASE_RE.match(line)
        if not match:
            continue
        number = int(match.group("number"))
        if number == phase_number:
            start = index + 1
            continue
        if start is not None and number != phase_number:
            end = index
            break
    return [] if start is None else lines[start:end]


def phase_status(todo_text: str, *, phase_number: int) -> PhaseStatus:
    ordinary_total = 0
    ordinary_open: list[str] = []
    anchor_total = 0
    anchor_open: list[str] = []
    for line in _phase_lines(todo_text, phase_number):
        match = TASK_RE.match(line)
        if not match:
            continue
        task_id = f"T{match.group('id')}"
        priority = match.group("priority")
        checked = match.group("mark") == "x"
        if priority == "ANCHOR":
            anchor_total += 1
            if not checked:
                anchor_open.append(task_id)
            continue
        ordinary_total += 1
        if not checked:
            ordinary_open.append(task_id)
    return PhaseStatus(
        phase_number=phase_number,
        ordinary_total=ordinary_total,
        ordinary_open=ordinary_open,
        anchor_total=anchor_total,
        anchor_open=anchor_open,
    )
