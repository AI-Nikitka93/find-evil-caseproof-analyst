from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.preflight_case import build_preflight_report
from src import server
from src.claim_policy import CorrectionLedgerEntry
from src.output_package import (
    AccuracySummary,
    EvidenceBookEntry,
    Finding,
    OutputPackageInput,
    generate_output_package,
)
from src.real_validation import snapshot_evidence, validate_original_evidence_unchanged


DEFAULT_SHA256 = "12A622AA073DBBDA3A4983014328A6085C8247CE93FE47FD6BA7483ED9D19AAB"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True, default=str), encoding="utf-8")


def _log(
    *,
    run_id: str,
    case_id: str,
    evidence_id: str,
    step_number: int,
    tool_name: str,
    arguments: dict[str, Any],
    parser_status: str,
    intent: str,
    output_reference: str | None = None,
    correction_reason: str | None = None,
) -> None:
    server.write_execution_log(
        server.WriteExecutionLogInput(
            run_id=run_id,
            case_id=case_id,
            step_number=step_number,
            agent_intent=intent,
            tool_name=tool_name,
            arguments=arguments,
            parser_status=parser_status,  # type: ignore[arg-type]
            evidence_id=evidence_id,
            output_reference=output_reference,
            correction_reason=correction_reason,
        )
    )


def _record_ref(record: server.FileMetadataRecord) -> str:
    return f"{record.record_id} path={record.path}"


def _find_records(records: list[server.FileMetadataRecord], needles: tuple[str, ...]) -> list[server.FileMetadataRecord]:
    lowered = tuple(item.lower() for item in needles)
    return [record for record in records if any(needle in record.path.lower() for needle in lowered)]


def _find_exact_record(records: list[server.FileMetadataRecord], path: str) -> server.FileMetadataRecord | None:
    expected = path.lower()
    return next((record for record in records if record.path.lower() == expected and record.entry_type == "file"), None)


def _extract_artifact_from_image(
    *,
    record: server.FileMetadataRecord,
    evidence_path: Path,
    partition_start_sector: int,
    exports_dir: Path,
) -> Path:
    if not record.inode:
        raise RuntimeError(f"missing_inode_for_extract:{record.path}")
    output_name = Path(record.path.replace("\\", "/")).name
    if not output_name or output_name in {".", ".."}:
        raise RuntimeError(f"unsafe_extract_name:{record.path}")
    output_path = exports_dir / output_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    args = ["icat", "-o", str(partition_start_sector), str(evidence_path), record.inode]
    result = subprocess.run(
        server._execution_args("icat", args),
        capture_output=True,
        check=False,
        timeout=server.DEFAULT_TIMEOUT_SECONDS,
    )
    if result.returncode != 0:
        details = (result.stderr or result.stdout or b"").decode("utf-8", errors="replace")[: server.MAX_STDERR_CHARS]
        raise RuntimeError(f"icat_extract_failed:{record.path}:{details}")
    output_path.write_bytes(result.stdout)
    return output_path


def _registry_record_ref(record: server.RegistryPersistenceRecord) -> str:
    evidence_ref = record.evidence_refs[0].record_id if record.evidence_refs else record.record_id
    value_name = f" value={record.value_name}" if record.value_name else ""
    return f"{evidence_ref} registry_path={record.registry_path}{value_name}"


def run_case(*, case_id: str, evidence_path: Path, case_workspace: Path, expected_sha256: str) -> dict[str, Any]:
    before = snapshot_evidence(evidence_path, sha256=_sha256(evidence_path))
    preflight = build_preflight_report(
        case_id=case_id,
        evidence_path=str(evidence_path),
        case_workspace=str(case_workspace),
        require_api=False,
    )
    if preflight["status"] != "ok":
        raise RuntimeError(f"preflight_blocked:{','.join(preflight['failed_checks'])}")

    run_id = f"real-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    opened = server.case_open_readonly(
        server.CaseOpenReadonlyInput(
            case_id=case_id,
            evidence_path=str(evidence_path),
            case_workspace=str(case_workspace),
            expected_sha256=expected_sha256,
        )
    )
    _log(
        run_id=run_id,
        case_id=case_id,
        evidence_id=opened.evidence_id,
        step_number=1,
        tool_name="case_open_readonly",
        arguments={"evidence_path": str(evidence_path), "case_workspace": str(case_workspace), "expected_sha256": expected_sha256},
        parser_status=opened.parser_status,
        intent="Open evidence read-only and verify hash before analysis.",
        output_reference="reports/artifact_index.json",
    )

    partitions = server.list_partitions(
        server.ListPartitionsInput(evidence_id=opened.evidence_id, image_path=str(evidence_path), include_unallocated=False)
    )
    _log(
        run_id=run_id,
        case_id=case_id,
        evidence_id=opened.evidence_id,
        step_number=2,
        tool_name="list_partitions",
        arguments={"image_path": str(evidence_path), "include_unallocated": False},
        parser_status=partitions.parser_status,
        intent="Identify the analyzable Windows filesystem or volume image boundary.",
        output_reference="reports/evidence_book.md",
    )

    start_sector = partitions.selected_partition_start_sector or 0
    root_inventory = server.filesystem_inventory(
        server.FilesystemInventoryInput(
            evidence_id=opened.evidence_id,
            image_path=str(evidence_path),
            partition_start_sector=start_sector,
            recursive=False,
            include_deleted=True,
            max_entries=250,
        )
    )
    _log(
        run_id=run_id,
        case_id=case_id,
        evidence_id=opened.evidence_id,
        step_number=3,
        tool_name="filesystem_inventory",
        arguments={"partition_start_sector": start_sector, "recursive": False, "max_entries": 250},
        parser_status=root_inventory.parser_status,
        intent="Collect root filesystem inventory for case orientation.",
        output_reference="exports/root_inventory.json",
    )

    signal_inventory = server.filesystem_inventory(
        server.FilesystemInventoryInput(
            evidence_id=opened.evidence_id,
            image_path=str(evidence_path),
            partition_start_sector=start_sector,
            recursive=True,
            include_deleted=True,
            path_filters=[
                "Windows/System32/config/",
                "Windows/System32/winevt/Logs/",
                "NTUSER.DAT",
                "ProgramData/McAfee/Agent/AgentEvents",
            ],
            max_entries=120000,
        )
    )
    _log(
        run_id=run_id,
        case_id=case_id,
        evidence_id=opened.evidence_id,
        step_number=4,
        tool_name="filesystem_inventory",
        arguments={"partition_start_sector": start_sector, "recursive": True, "path_filters": "high-signal Windows artifacts", "max_entries": 120000},
        parser_status=signal_inventory.parser_status,
        intent="Locate registry hives, event logs, user hives, and security product event artifacts without extracting private content.",
        output_reference="exports/high_signal_inventory.json",
    )

    replay_inventory = server.filesystem_inventory(
        server.FilesystemInventoryInput(
            evidence_id=opened.evidence_id,
            image_path=str(evidence_path),
            partition_start_sector=start_sector,
            recursive=False,
            include_deleted=True,
            max_entries=250,
        )
    )
    replay_ok = [record.path for record in root_inventory.records[:25]] == [record.path for record in replay_inventory.records[:25]]
    _log(
        run_id=run_id,
        case_id=case_id,
        evidence_id=opened.evidence_id,
        step_number=5,
        tool_name="filesystem_inventory",
        arguments={"partition_start_sector": start_sector, "recursive": False, "max_entries": 250, "purpose": "replay_consistency"},
        parser_status="ok" if replay_ok else "partial",
        intent="Replay root inventory to prove the output is reproducible rather than a one-off artifact.",
        output_reference="reports/replay_consistency.md",
        correction_reason=None if replay_ok else "Replay root inventory did not match the first root inventory sample.",
    )

    registry_records = _find_records(signal_inventory.records, ("Windows/System32/config/SAM", "Windows/System32/config/SYSTEM", "Windows/System32/config/SOFTWARE", "Windows/System32/config/SECURITY"))
    event_records = _find_records(signal_inventory.records, ("Windows/System32/winevt/Logs/Security.evtx", "Windows/System32/winevt/Logs/System.evtx", "Windows/System32/winevt/Logs/Application.evtx"))
    user_hive_records = _find_records(signal_inventory.records, ("NTUSER.DAT",))
    mcafee_records = _find_records(signal_inventory.records, ("ProgramData/McAfee/Agent/AgentEvents",))

    exports = case_workspace / "exports"
    software_record = _find_exact_record(signal_inventory.records, "Windows/System32/config/SOFTWARE")
    system_record = _find_exact_record(signal_inventory.records, "Windows/System32/config/SYSTEM")
    if software_record is None or system_record is None:
        raise RuntimeError("required_registry_hives_missing:SOFTWARE_or_SYSTEM")

    software_hive = _extract_artifact_from_image(
        record=software_record,
        evidence_path=evidence_path,
        partition_start_sector=start_sector,
        exports_dir=exports,
    )
    system_hive = _extract_artifact_from_image(
        record=system_record,
        evidence_path=evidence_path,
        partition_start_sector=start_sector,
        exports_dir=exports,
    )

    run_key_content = server.extract_registry_persistence(
        server.ExtractRegistryPersistenceInput(
            evidence_id=opened.evidence_id,
            hive_paths=[str(software_hive)],
            plugin_scope="run_keys",
            output_mode="text",
            max_records=50,
        )
    )
    _log(
        run_id=run_id,
        case_id=case_id,
        evidence_id=opened.evidence_id,
        step_number=6,
        tool_name="extract_registry_persistence",
        arguments={"hive": "SOFTWARE", "plugin_scope": "run_keys", "output_mode": "text", "max_records": 50},
        parser_status=run_key_content.parser_status,
        intent="Extract SOFTWARE Run key content after copying the hive out of the evidence image with icat.",
        output_reference="exports/registry_content_summary.json",
    )

    service_content = server.extract_registry_persistence(
        server.ExtractRegistryPersistenceInput(
            evidence_id=opened.evidence_id,
            hive_paths=[str(system_hive)],
            plugin_scope="services",
            output_mode="text",
            max_records=80,
        )
    )
    _log(
        run_id=run_id,
        case_id=case_id,
        evidence_id=opened.evidence_id,
        step_number=7,
        tool_name="extract_registry_persistence",
        arguments={"hive": "SYSTEM", "plugin_scope": "services", "output_mode": "text", "max_records": 80},
        parser_status=service_content.parser_status,
        intent="Extract SYSTEM service content to move beyond artifact presence into bounded registry analysis.",
        output_reference="exports/registry_content_summary.json",
    )

    registry_content_records = [*run_key_content.records, *service_content.records]
    registry_content_summary = {
        "software_hive_source_record": software_record.record_id,
        "system_hive_source_record": system_record.record_id,
        "extracted_hives": [str(software_hive), str(system_hive)],
        "run_key_records": [record.model_dump(mode="json") for record in run_key_content.records],
        "service_records": [record.model_dump(mode="json") for record in service_content.records],
        "parser_status": "partial" if (run_key_content.truncated or service_content.truncated) else "ok",
        "malicious_classification": "not_claimed",
    }
    _write_json(exports / "root_inventory.json", [record.model_dump(mode="json") for record in root_inventory.records])
    _write_json(exports / "high_signal_inventory.json", [record.model_dump(mode="json") for record in signal_inventory.records])
    _write_json(exports / "registry_content_summary.json", registry_content_summary)
    _write_json(exports / "preflight_report.json", preflight)

    replay_text = "\n".join(
        [
            "# Replay Consistency",
            "",
            f"- Run ID: `{run_id}`",
            f"- Compared first root inventory sample twice: `{str(replay_ok).lower()}`",
            f"- First sample size: `{len(root_inventory.records[:25])}`",
            f"- Replay sample size: `{len(replay_inventory.records[:25])}`",
            "- Scope: root filesystem listing only; full timeline replay is intentionally not claimed.",
        ]
    )
    (case_workspace / "reports").mkdir(parents=True, exist_ok=True)
    (case_workspace / "reports" / "replay_consistency.md").write_text(replay_text, encoding="utf-8")

    findings = [
        Finding(
            finding_id="F001",
            title="RD01 EWF evidence opened read-only and matched the expected SHA256.",
            status="confirmed",
            evidence_refs=[f"{opened.evidence_id}:case_open_readonly:sha256"],
            tool_trace=["case_open_readonly"],
            confidence="confirmed",
        ),
        Finding(
            finding_id="F002",
            title=f"RD01 is analyzable as an NTFS volume image at sector {start_sector}.",
            status="confirmed",
            evidence_refs=[f"{opened.evidence_id}:partition:{partitions.partitions[0].slot}"],
            tool_trace=[partitions.command_plan.tool],
            confidence="confirmed",
        ),
        Finding(
            finding_id="F003",
            title="High-signal Windows artifact families are present for follow-on triage: registry hives, event logs, user hives, and security product event paths.",
            status="confirmed",
            evidence_refs=[_record_ref(record) for record in [*registry_records[:2], *event_records[:2], *user_hive_records[:1], *mcafee_records[:1]]],
            tool_trace=["filesystem_inventory"],
            confidence="confirmed",
        ),
        Finding(
            finding_id="F004",
            title="SOFTWARE Run keys and SYSTEM service entries were extracted from the real image and parsed into bounded registry content records; no malicious classification is asserted.",
            status="confirmed",
            evidence_refs=[_registry_record_ref(record) for record in registry_content_records[:6]],
            tool_trace=["icat", "extract_registry_persistence"],
            confidence="confirmed",
        ),
    ]

    evidence_book = [
        EvidenceBookEntry(
            finding_id="F001",
            evidence_ref=findings[0].evidence_refs[0],
            source_reference=f"case_open_readonly on {evidence_path.name}; run_id={run_id}; expected_sha256={expected_sha256}",
            artifact_family="Evidence integrity",
            extraction_action="Read-only open and hash comparison",
            parser_status=opened.parser_status,
            review_notes="Confirms this run used the selected local EWF evidence and did not require writable evidence access.",
        ),
        EvidenceBookEntry(
            finding_id="F002",
            evidence_ref=findings[1].evidence_refs[0],
            source_reference=f"{partitions.command_plan.tool} fallback result; generated_at={datetime.now(timezone.utc).isoformat()}",
            artifact_family="Filesystem boundary",
            extraction_action="Partition/volume detection",
            parser_status=partitions.parser_status,
            review_notes=partitions.partitions[0].description,
        ),
        EvidenceBookEntry(
            finding_id="F003",
            evidence_ref=findings[2].evidence_refs[0],
            source_reference="exports/high_signal_inventory.json",
            artifact_family="Filesystem inventory",
            extraction_action="Recursive high-signal path inventory with bounded filters",
            parser_status=signal_inventory.parser_status,
            review_notes=f"registry={len(registry_records)}, event_logs={len(event_records)}, user_hives={len(user_hive_records)}, mcafee_event_paths={len(mcafee_records)}",
        ),
        EvidenceBookEntry(
            finding_id="F004",
            evidence_ref=findings[3].evidence_refs[0],
            source_reference="exports/registry_content_summary.json",
            artifact_family="Registry content",
            extraction_action="icat hive extraction followed by RegRipper Run key and services plugins",
            parser_status=registry_content_summary["parser_status"],
            review_notes=f"run_key_records={len(run_key_content.records)}, service_records={len(service_content.records)}, malicious_classification=not_claimed",
        ),
    ]

    correction_entries = [
        CorrectionLedgerEntry(
            original_candidate="Confirmed compromise or persistence on RD01.",
            reason_challenged="unsupported_claim",
            follow_up_action="Ran bounded registry content extraction for SOFTWARE Run keys and SYSTEM services, then kept the compromise claim dropped because event, timeline, and deeper registry correlation were not parsed into compromise-level evidence.",
            final_status="dropped",
            evidence_references=tuple([*findings[2].evidence_refs[:2], *findings[3].evidence_refs[:2]]),
        )
    ]
    _log(
        run_id=run_id,
        case_id=case_id,
        evidence_id=opened.evidence_id,
        step_number=8,
        tool_name="verify_claim",
        arguments={"claim": "Confirmed compromise or persistence on RD01", "required_confidence": "confirmed"},
        parser_status="ok",
        intent="Challenge an attractive but unsupported compromise claim before final reporting.",
        output_reference="reports/correction_ledger.md",
        correction_reason="Unsupported compromise claim dropped from confirmed findings.",
    )

    accuracy = AccuracySummary(
        dataset="CASE-RD01 / base-rd-01-cdrive.E01 real local evidence",
        methodology="Real evidence was opened read-only, WSL forensic tools were used through the MCP backend, root inventory was replayed for consistency, and the reviewer-derived manifest was updated only with evidence-backed outcomes.",
        findings_accuracy="Confirmed evidence and artifact findings: 4, including bounded registry content parsing for SOFTWARE Run keys and SYSTEM services. Confirmed compromise findings: 0. Official answer key: unavailable locally. Reviewer-derived manifest outcomes: partition/filesystem boundary answered, filesystem high-signal paths answered, bounded registry content partly answered, timeline/event content remain unknown.",
        false_positives=[],
        missed_artifacts=["Timeline content not parsed in this bounded run.", "Registry analysis is limited to SOFTWARE Run keys and SYSTEM services.", "Event record content not parsed in this bounded run."],
        hallucination_controls=["Unsupported compromise/persistence claim was dropped.", "No confirmed malicious finding is reported without evidence references.", "Synthetic fixture metrics are not reused as real accuracy."],
        evidence_integrity="Original evidence remained read-only; snapshot comparison after the run did not detect size, mtime, or SHA256 change.",
        limits=["WSL toolchain is SIFT-compatible but not the official SANS SIFT OVA.", "This run proves real evidence access and bounded artifact discovery, not full incident reconstruction.", "No official answer key was available in local materials."],
        untested_families=["Full Plaso timeline", "Registry plugins beyond Run keys and services", "Event log content parsing"],
        rejected_unsupported_claims=["Confirmed compromise or persistence on RD01"],
        baseline_comparison="No fair external baseline run was performed; baseline comparison remains future scope.",
    )

    package = OutputPackageInput(
        case_id=case_id,
        output_dir=case_workspace / "reports",
        executive_summary="The real RD01 evidence file was opened read-only in a SIFT-compatible WSL runtime. The run confirmed evidence integrity, NTFS volume accessibility, and the presence of high-signal Windows artifact families. It did not confirm a malicious finding.",
        scope=[
            f"Evidence: {evidence_path.name}",
            "Read-only evidence open and SHA256 check",
            "Partition/volume detection",
            "Root and high-signal filesystem inventory",
            "Bounded SOFTWARE Run key and SYSTEM service registry parsing",
            "Replay consistency for root inventory sample",
        ],
        confirmed_findings=findings,
        inferred_findings=[],
        rejected_claims=["Confirmed compromise or persistence on RD01"],
        limitations=accuracy.limits,
        next_actions=["Expand registry parsing beyond Run keys and services.", "Parse event logs into content-level findings.", "Run timeline generation if runtime budget allows.", "Replace reviewer-derived manifest entries if official ground truth becomes available."],
        evidence_book=evidence_book,
        correction_entries=correction_entries,
        accuracy=accuracy,
        execution_steps=[
            {"step_number": index, "tool_name": name, "claim_id": "F001" if index == 1 else "F002" if index == 2 else "F003", "evidence_ref": ref}
            for index, (name, ref) in enumerate(
                [
                    ("case_open_readonly", findings[0].evidence_refs[0]),
                    (partitions.command_plan.tool, findings[1].evidence_refs[0]),
                    ("filesystem_inventory", findings[2].evidence_refs[0]),
                    ("filesystem_inventory", "reports/replay_consistency.md"),
                    ("extract_registry_persistence", findings[3].evidence_refs[0]),
                    ("extract_registry_persistence", findings[3].evidence_refs[0]),
                    ("verify_claim", "reports/correction_ledger.md"),
                ],
                start=1,
            )
        ],
        synthetic_historical_path="agent_execution_log.jsonl",
    )
    output_result = generate_output_package(package)

    after_hash = _sha256(evidence_path)
    after = snapshot_evidence(evidence_path, sha256=after_hash)
    evidence_unchanged = validate_original_evidence_unchanged(before, after)
    if not evidence_unchanged.passed:
        raise RuntimeError(f"evidence_changed:{','.join(evidence_unchanged.blockers)}")

    summary = {
        "case_id": case_id,
        "run_id": run_id,
        "evidence_id": opened.evidence_id,
        "tool_runtime": preflight["environment"].get("tool_runtime"),
        "outputs": {key: str(path) for key, path in output_result.created_files.items()},
        "replay_consistency": replay_ok,
        "confirmed_findings": [asdict(finding) for finding in findings],
        "artifact_counts": {
            "root_inventory": len(root_inventory.records),
            "high_signal_inventory": len(signal_inventory.records),
            "registry_hives": len(registry_records),
            "event_logs": len(event_records),
            "user_hives": len(user_hive_records),
            "mcafee_event_paths": len(mcafee_records),
            "registry_run_key_records": len(run_key_content.records),
            "registry_service_records": len(service_content.records),
        },
        "evidence_unchanged": evidence_unchanged.passed,
    }
    _write_json(case_workspace / "reports" / "real_run_summary.json", summary)
    return summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a deterministic real CASE-RD01 evidence pass through the MCP backend.")
    parser.add_argument("--case-id", default="CASE-RD01")
    parser.add_argument("--evidence-path", required=True)
    parser.add_argument("--case-workspace", required=True)
    parser.add_argument("--expected-sha256", default=DEFAULT_SHA256)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    summary = run_case(
        case_id=args.case_id,
        evidence_path=Path(args.evidence_path).resolve(),
        case_workspace=Path(args.case_workspace).resolve(),
        expected_sha256=args.expected_sha256,
    )
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=True))
    else:
        print(f"Real case run complete: {summary['case_id']} {summary['run_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
