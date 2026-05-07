from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE_MD = ROOT / "docs" / "STATE.md"
STATE_JSON = ROOT / "docs" / "state.json"


def _parse_state_block(text: str) -> dict[str, object]:
    inside = False
    state: dict[str, object] = {}

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "```state":
            inside = True
            continue
        if inside and line == "```":
            break
        if not inside or ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value == "[]":
            state[key] = []
        elif value.startswith("[") and value.endswith("]"):
            state[key] = json.loads(value)
        else:
            state[key] = value

    required = {
        "current_goal",
        "current_task",
        "status",
        "active_step",
        "next_step",
        "blockers",
        "artifacts",
        "updated_at",
    }
    missing = sorted(required - state.keys())
    if missing:
        raise ValueError(f"STATE.md is missing fields: {', '.join(missing)}")

    return state


def main() -> None:
    state = _parse_state_block(STATE_MD.read_text(encoding="utf-8"))
    STATE_JSON.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
