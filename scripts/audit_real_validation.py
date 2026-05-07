from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.real_validation import audit_real_validation_workspace


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit real SIFT run artifacts without accepting synthetic substitutes.")
    parser.add_argument("--case-workspace", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = audit_real_validation_workspace(Path(args.case_workspace))
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=True))
    else:
        print(f"Real validation status: {report.status}")
        for name, ok in report.checks.items():
            print(f"{'PASS' if ok else 'BLOCK':5} {name}")
        for blocker in report.blockers:
            print(f"BLOCKER {blocker}")
    if args.strict and report.status != "ok":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
