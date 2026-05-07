from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.claim_policy import CorrectionLedgerEntry
from src.output_package import (
    AccuracySummary,
    EvidenceBookEntry,
    Finding,
    OutputPackageInput,
    generate_output_package,
)


def build_package_from_json(payload: dict[str, Any]) -> OutputPackageInput:
    return OutputPackageInput(
        case_id=payload["case_id"],
        output_dir=Path(payload["output_dir"]),
        executive_summary=payload["executive_summary"],
        scope=list(payload.get("scope", [])),
        confirmed_findings=[Finding(**item) for item in payload.get("confirmed_findings", [])],
        inferred_findings=[Finding(**item) for item in payload.get("inferred_findings", [])],
        rejected_claims=list(payload.get("rejected_claims", [])),
        limitations=list(payload.get("limitations", [])),
        next_actions=list(payload.get("next_actions", [])),
        evidence_book=[EvidenceBookEntry(**item) for item in payload.get("evidence_book", [])],
        correction_entries=[
            CorrectionLedgerEntry(
                original_candidate=item["original_candidate"],
                reason_challenged=item["reason_challenged"],
                follow_up_action=item["follow_up_action"],
                final_status=item["final_status"],
                evidence_references=tuple(item.get("evidence_references", [])),
            )
            for item in payload.get("correction_entries", [])
        ],
        accuracy=AccuracySummary(**payload["accuracy"]),
        execution_steps=list(payload.get("execution_steps", [])),
        synthetic_historical_path=payload.get("synthetic_historical_path"),
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate judge-facing FIND EVIL output package from JSON input.")
    parser.add_argument("--input-json", required=True, help="Path to package input JSON.")
    parser.add_argument("--json", action="store_true", help="Print created files as JSON.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    result = generate_output_package(build_package_from_json(payload))
    created = {key: str(path) for key, path in result.created_files.items()}
    if args.json:
        print(json.dumps({"created_files": created}, indent=2, ensure_ascii=True))
    else:
        for key, path in created.items():
            print(f"{key}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
