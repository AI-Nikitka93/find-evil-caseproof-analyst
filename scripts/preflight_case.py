from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.check_env import build_environment_report


DEFAULT_MIN_EVIDENCE_BYTES = 1_048_576


@dataclass(slots=True)
class PathCheck:
    name: str
    path: str
    ok: bool
    detail: str


def _resolve(path: str) -> Path:
    return Path(path).expanduser().resolve()


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def build_preflight_report(
    *,
    case_id: str,
    evidence_path: str,
    case_workspace: str,
    min_evidence_bytes: int = DEFAULT_MIN_EVIDENCE_BYTES,
    require_sift: bool = True,
    require_api: bool = True,
) -> dict[str, Any]:
    evidence = _resolve(evidence_path)
    workspace = _resolve(case_workspace)
    project_root = Path.cwd().resolve()
    evidence_dir = (project_root / "evidence").resolve()
    cases_dir = (project_root / "cases").resolve()

    checks: list[PathCheck] = []

    checks.append(
        PathCheck(
            name="case_id",
            path=case_id,
            ok=bool(case_id.strip()) and not any(sep in case_id for sep in ("/", "\\", "..")),
            detail="case_id must be non-empty and must not contain path separators",
        )
    )

    evidence_exists = evidence.is_file()
    evidence_size = evidence.stat().st_size if evidence_exists else 0
    checks.append(
        PathCheck(
            name="evidence_exists",
            path=str(evidence),
            ok=evidence_exists,
            detail="selected evidence file must exist",
        )
    )
    checks.append(
        PathCheck(
            name="evidence_size",
            path=str(evidence),
            ok=evidence_exists and evidence_size >= min_evidence_bytes,
            detail=f"evidence file must be at least {min_evidence_bytes} bytes to reject tiny fixtures",
        )
    )
    checks.append(
        PathCheck(
            name="evidence_local_only",
            path=str(evidence),
            ok=_is_relative_to(evidence, evidence_dir),
            detail="evidence must be under the local ignored evidence directory",
        )
    )
    checks.append(
        PathCheck(
            name="workspace_not_evidence",
            path=str(workspace),
            ok=workspace != evidence and not _is_relative_to(workspace, evidence_dir),
            detail="case workspace must not be the evidence file or inside the evidence directory",
        )
    )
    checks.append(
        PathCheck(
            name="workspace_under_cases",
            path=str(workspace),
            ok=_is_relative_to(workspace, cases_dir),
            detail="case workspace must be under the cases directory",
        )
    )

    env_report = build_environment_report()
    implemented_agent_keys = {"GROQ_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY"}
    api_ready = not require_api or any(
        item["name"] in implemented_agent_keys and item["configured"] and item.get("valid", False)
        for item in env_report["api_environment"]
    )
    sift_ready = not env_report["missing_required_sift_binaries"] if require_sift else True

    checks.append(
        PathCheck(
            name="api_ready",
            path="GROQ_API_KEY or OPENROUTER_API_KEY or ANTHROPIC_API_KEY",
            ok=api_ready,
            detail=(
                "AI provider key is not required for this deterministic MCP/backend evidence check"
                if not require_api
                else "implemented agent runtime API key must be configured and syntactically safe without exposing the value"
            ),
        )
    )
    checks.append(
        PathCheck(
            name="sift_ready",
            path="required SIFT commands",
            ok=sift_ready,
            detail="required SIFT commands must resolve and current runtime must be usable",
        )
    )

    failed = [check for check in checks if not check.ok]
    return {
        "case_id": case_id,
        "evidence_path": str(evidence),
        "case_workspace": str(workspace),
        "evidence_size": evidence_size,
        "status": "ok" if not failed else "blocked",
        "checks": [asdict(check) for check in checks],
        "failed_checks": [check.name for check in failed],
        "environment": env_report,
        "secrets_redacted": True,
    }


def _print_text_report(report: dict[str, Any]) -> None:
    print(f"Preflight status: {report['status']}")
    for check in report["checks"]:
        marker = "PASS" if check["ok"] else "BLOCK"
        print(f"{marker:5} {check['name']} - {check['detail']}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check case-specific evidence-run prerequisites.")
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--evidence-path", required=True)
    parser.add_argument("--case-workspace", required=True)
    parser.add_argument("--min-evidence-bytes", type=int, default=DEFAULT_MIN_EVIDENCE_BYTES)
    parser.add_argument("--no-api-required", action="store_true", help="Allow deterministic MCP/backend evidence checks without an AI provider key.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_preflight_report(
        case_id=args.case_id,
        evidence_path=args.evidence_path,
        case_workspace=args.case_workspace,
        min_evidence_bytes=args.min_evidence_bytes,
        require_api=not args.no_api_required,
    )
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=True))
    else:
        _print_text_report(report)
    if args.strict and report["status"] != "ok":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
