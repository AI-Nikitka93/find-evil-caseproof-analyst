from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TOOLS = (
    "case_open_readonly",
    "list_partitions",
    "filesystem_inventory",
    "build_timeline",
    "extract_registry_persistence",
    "extract_event_records",
    "verify_claim",
    "write_execution_log",
)
REQUIRED_IGNORE_PATTERNS = (
    ".env",
    ".env.*",
    "!.env.example",
    "docs/*.local.md",
    "cases/",
    "fixtures/",
    "evidence/",
)
REQUIRED_DOCS = (
    "docs/local_only_notes_audit.md",
    "docs/trust_boundary_contract.md",
    "docs/public_tool_name_stability_check.md",
    "docs/schema_product_entity_mapping.md",
    "docs/public_tool_safety_acceptance.md",
    "docs/secret_handling_policy.md",
    "docs/provider_readiness_check.md",
    "docs/runtime_adapter_language_audit.md",
    "docs/future_agent_project_instructions.md",
    "docs/no_revert_workspace_discipline.md",
    "DESIGN.md",
    "docs/design_research_note_2026-05-06.md",
    "docs/visual_asset_policy.md",
    "docs/demo_narration_notes.md",
    "docs/visual_qa_checklist.md",
    "docs/phase6_anchor_review.md",
    "docs/phase6_end_review.md",
    "docs/reviewer_traceability_walkthrough.md",
    "docs/final_quality_gate_matrix.md",
    "docs/final_submission_package.md",
    "docs/demo_video_script.md",
    "docs/judge_try_it_out.md",
    "docs/public_release_manifest.md",
    "docs/public_real_execution_log_sample.jsonl",
    "docs/public_real_traceability_packet.md",
    "docs/final_release_go_no_go_2026-05-07.md",
)
REQUIRED_SCHEMA_MARKERS = (
    "CaseOpenReadonlyInput",
    "CaseOpenReadonlyOutput",
    "EvidenceReference",
    "VerifyClaimInput",
    "ClaimVerificationResult",
    "ExecutionLogRecord",
)
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
)
SCAN_EXTENSIONS = {".md", ".py", ".txt", ".json", ".jsonl", ".example"}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "cases", "fixtures", "evidence"}
SKIP_FILES = {".env.local"}


@dataclass(slots=True)
class AuditCheck:
    name: str
    ok: bool
    detail: str


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _public_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.name in SKIP_FILES:
            continue
        if path.suffix.lower() in SCAN_EXTENSIONS or path.name == ".gitignore":
            files.append(path)
    return files


def build_release_controls_report(root: Path = PROJECT_ROOT) -> dict[str, Any]:
    checks: list[AuditCheck] = []

    gitignore_path = root / ".gitignore"
    gitignore = _read(gitignore_path) if gitignore_path.exists() else ""
    missing_ignores = [pattern for pattern in REQUIRED_IGNORE_PATTERNS if pattern not in gitignore.splitlines()]
    checks.append(
        AuditCheck(
            name="local_only_ignore_patterns",
            ok=not missing_ignores,
            detail="missing: " + ", ".join(missing_ignores) if missing_ignores else "all required local-only patterns are ignored",
        )
    )

    missing_docs = [path for path in REQUIRED_DOCS if not (root / path).is_file()]
    checks.append(
        AuditCheck(
            name="boundary_docs_exist",
            ok=not missing_docs,
            detail="missing: " + ", ".join(missing_docs) if missing_docs else "all release-control docs exist",
        )
    )

    public_log_path = root / "docs" / "public_real_execution_log_sample.jsonl"
    public_log_records: list[dict[str, Any]] = []
    public_log_blockers: list[str] = []
    if public_log_path.is_file():
        for index, line in enumerate(_read(public_log_path).splitlines(), start=1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                public_log_blockers.append(f"invalid_jsonl_line:{index}")
                continue
            if not isinstance(payload, dict):
                public_log_blockers.append(f"non_object_line:{index}")
                continue
            public_log_records.append(payload)
        public_log_tools = {str(record.get("tool_name", "")) for record in public_log_records}
        for required in ("case_open_readonly", "list_partitions", "filesystem_inventory", "extract_registry_persistence", "verify_claim"):
            if required not in public_log_tools:
                public_log_blockers.append(f"missing_tool:{required}")
        if not any(record.get("correction_reason") for record in public_log_records):
            public_log_blockers.append("missing_visible_correction_reason")
        public_log_text = _read(public_log_path)
        if re.search(r"(?i)(?:[A-Z]:\\|/home/|/Users/|C:\\Users\\)", public_log_text):
            public_log_blockers.append("local_path_leak")
    else:
        public_log_blockers.append("missing_public_real_execution_log_sample")
    checks.append(
        AuditCheck(
            name="public_real_execution_log_sample",
            ok=not public_log_blockers,
            detail="blockers: " + ", ".join(sorted(set(public_log_blockers))) if public_log_blockers else f"{len(public_log_records)} public-safe real log records",
        )
    )

    server_path = root / "src" / "server.py"
    server_source = _read(server_path)
    missing_tools = [tool for tool in EXPECTED_TOOLS if f"def {tool}(" not in server_source]
    tool_decorator_count = server_source.count("@mcp.tool()")
    checks.append(
        AuditCheck(
            name="public_tool_names_stable",
            ok=not missing_tools and tool_decorator_count == len(EXPECTED_TOOLS),
            detail=(
                f"missing={missing_tools}, decorators={tool_decorator_count}"
                if missing_tools or tool_decorator_count != len(EXPECTED_TOOLS)
                else "expected eight public MCP tools are present"
            ),
        )
    )

    forbidden_server_markers = [marker for marker in ("shell=True", "NotImplementedError") if marker in server_source]
    checks.append(
        AuditCheck(
            name="no_generic_shell_or_stubs",
            ok=not forbidden_server_markers and "subprocess.run(" in server_source and "check=False" in server_source,
            detail=(
                "forbidden markers: " + ", ".join(forbidden_server_markers)
                if forbidden_server_markers
                else "no generic shell/stub marker found; fixed subprocess path is present"
            ),
        )
    )

    missing_schema_markers = [marker for marker in REQUIRED_SCHEMA_MARKERS if marker not in server_source]
    checks.append(
        AuditCheck(
            name="schema_product_markers_present",
            ok=not missing_schema_markers,
            detail=(
                "missing: " + ", ".join(missing_schema_markers)
                if missing_schema_markers
                else "core schema/product markers are present"
            ),
        )
    )

    secret_hits: list[str] = []
    for path in _public_files(root):
        text = _read(path)
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                secret_hits.append(str(path.relative_to(root)))
                break
    checks.append(
        AuditCheck(
            name="no_obvious_public_secret_values",
            ok=not secret_hits,
            detail="hits: " + ", ".join(secret_hits) if secret_hits else "no obvious public token values found",
        )
    )

    failed = [check.name for check in checks if not check.ok]
    return {
        "status": "ok" if not failed else "blocked",
        "checks": [asdict(check) for check in checks],
        "failed_checks": failed,
        "expected_tools": list(EXPECTED_TOOLS),
        "secrets_redacted": True,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit release-control contracts for local-only data and MCP safety.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_release_controls_report()
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=True))
    else:
        print(f"Release controls status: {report['status']}")
        for check in report["checks"]:
            marker = "PASS" if check["ok"] else "BLOCK"
            print(f"{marker:5} {check['name']} - {check['detail']}")
    if args.strict and report["status"] != "ok":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
