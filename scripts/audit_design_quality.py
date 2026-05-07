from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.design_quality import audit_design_package


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit the Phase 6 design package.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = audit_design_package(PROJECT_ROOT)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=True))
    else:
        print(f"Design quality status: {report.status}")
        for check in report.checks:
            marker = "PASS" if check.ok else "BLOCK"
            print(f"{marker:5} {check.name} - {check.detail}")
    if args.strict and report.status != "ok":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
