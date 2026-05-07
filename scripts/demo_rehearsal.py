from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE_PATH = Path("evidence") / "base-rd-01-cdrive.E01"
REQUIRED_CASE_REPORTS = (
    "final_analyst_report.md",
    "evidence_book.md",
    "correction_ledger.md",
    "real_run_accuracy_report.md",
)
REQUIRED_SCRIPT_PHRASES = (
    "live terminal",
    "real evidence",
    "self-correction",
    "trace",
)


@dataclass(frozen=True, slots=True)
class RehearsalGate:
    ok: bool
    detail: str


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _load_public_trace(root: Path) -> tuple[list[dict[str, Any]], str | None]:
    trace_path = root / "docs" / "public_real_execution_log_sample.jsonl"
    if not trace_path.is_file():
        return [], "missing public real execution log sample"
    records: list[dict[str, Any]] = []
    for index, line in enumerate(_read(trace_path).splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            return [], f"invalid JSONL line {index}: {exc.msg}"
        if isinstance(payload, dict):
            records.append(payload)
    return records, None


def _check_demo_script(root: Path) -> RehearsalGate:
    script_path = root / "docs" / "demo_video_script.md"
    narration_path = root / "docs" / "demo_narration_notes.md"
    if not script_path.is_file():
        return RehearsalGate(ok=False, detail="docs/demo_video_script.md is missing")
    if not narration_path.is_file():
        return RehearsalGate(ok=False, detail="docs/demo_narration_notes.md is missing")
    text = _read(script_path).lower()
    missing = [phrase for phrase in REQUIRED_SCRIPT_PHRASES if phrase not in text]
    if missing:
        return RehearsalGate(ok=False, detail="demo script missing required story phrases: " + ", ".join(missing))
    return RehearsalGate(ok=True, detail="demo script covers live terminal, real evidence, self-correction, and traceability")


def _check_case_outputs(root: Path, case_id: str) -> RehearsalGate:
    reports_dir = root / "cases" / case_id / "reports"
    missing = [name for name in REQUIRED_CASE_REPORTS if not (reports_dir / name).is_file()]
    if missing:
        return RehearsalGate(ok=False, detail="missing local case reports: " + ", ".join(missing))
    return RehearsalGate(ok=True, detail=f"local {case_id} report package is present")


def _check_public_trace_story(records: list[dict[str, Any]], error: str | None) -> tuple[RehearsalGate, dict[str, bool]]:
    story = {
        "has_real_evidence_open": False,
        "has_self_correction": False,
        "has_registry_or_event_depth": False,
    }
    if error:
        return RehearsalGate(ok=False, detail=error), story
    tools = {str(record.get("tool_name", "")) for record in records}
    story["has_real_evidence_open"] = "case_open_readonly" in tools
    story["has_self_correction"] = any(
        str(record.get("tool_name", "")) == "verify_claim" and bool(record.get("correction_reason"))
        for record in records
    )
    story["has_registry_or_event_depth"] = bool({"extract_registry_persistence", "extract_event_records"} & tools)
    missing = [name for name, ok in story.items() if not ok]
    if missing:
        return RehearsalGate(ok=False, detail="public trace missing demo story signals: " + ", ".join(missing)), story
    return RehearsalGate(ok=True, detail="public trace proves evidence open, artifact depth, and self-correction"), story


def build_demo_rehearsal_report(
    *,
    root: Path = PROJECT_ROOT,
    case_id: str = "CASE-RD01",
    evidence_path: Path = DEFAULT_EVIDENCE_PATH,
) -> dict[str, Any]:
    root = root.resolve()
    records, trace_error = _load_public_trace(root)
    trace_gate, story = _check_public_trace_story(records, trace_error)
    gates = {
        "demo_script": _check_demo_script(root),
        "self_correction_trace": trace_gate,
        "case_outputs": _check_case_outputs(root, case_id),
    }
    blockers = [name for name, gate in gates.items() if not gate.ok]
    evidence_arg = str(evidence_path)
    workspace_arg = str(Path("cases") / case_id)
    return {
        "status": "ready" if not blockers else "blocked",
        "case_id": case_id,
        "blockers": blockers,
        "gates": {name: asdict(gate) for name, gate in gates.items()},
        "demo_story": story,
        "commands": {
            "api_ready": "py -m src.agent --check-api",
            "sift_ready": "py scripts\\check_env.py --strict",
            "deterministic_real_run": (
                f"py scripts\\run_real_case.py --case-id {case_id} "
                f"--evidence-path {evidence_arg} --case-workspace {workspace_arg} --json"
            ),
            "real_validation_audit": f"py scripts\\audit_real_validation.py --case-workspace {workspace_arg} --strict",
            "public_trace_refresh": "py scripts\\generate_public_trace_packet.py --json --strict",
            "final_submission_gate": "py scripts\\final_submission_audit.py --demo-video-url VIDEO_URL --devpost-url DEVPOST_URL --strict",
        },
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check and print the live terminal demo rehearsal path.")
    parser.add_argument("--case-id", default="CASE-RD01")
    parser.add_argument("--evidence-path", default=str(DEFAULT_EVIDENCE_PATH))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_demo_rehearsal_report(
        case_id=args.case_id,
        evidence_path=Path(args.evidence_path),
    )
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=True))
    else:
        print(f"Demo rehearsal status: {report['status']}")
        print("gates:")
        for name, gate in report["gates"].items():
            marker = "PASS" if gate["ok"] else "BLOCK"
            print(f"  {marker:5} {name} - {gate['detail']}")
        print("commands:")
        for name, command in report["commands"].items():
            print(f"  {name}: {command}")
    if args.strict and report["status"] != "ready":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
