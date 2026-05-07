from __future__ import annotations

from collections import Counter
from typing import Any


WATCHLIST_EVENT_IDS: dict[int, str] = {
    1102: "security_log_cleared",
    4624: "successful_logon",
    4672: "special_privileges_assigned",
    4688: "process_created",
    4697: "service_installed",
    4720: "user_account_created",
    4732: "member_added_to_local_group",
    7045: "service_installed",
}


def _records(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    values = payload.get(key, [])
    return [item for item in values if isinstance(item, dict)] if isinstance(values, list) else []


def _event_id(record: dict[str, Any]) -> int:
    try:
        return int(record.get("event_id", 0) or 0)
    except (TypeError, ValueError):
        return 0


def _event_ref(record: dict[str, Any]) -> str:
    event_id = record.get("event_id", "unknown")
    channel = record.get("channel", "unknown")
    timestamp = record.get("timestamp_utc") or "no_timestamp"
    return f"{record.get('record_id', 'event:unknown')} event_id={event_id} channel={channel} timestamp={timestamp}"


def _registry_ref(record: dict[str, Any]) -> str:
    path = record.get("registry_path") or "unknown_registry_path"
    value = record.get("value_name") or record.get("value_data") or "unknown_value"
    return f"{record.get('record_id', 'registry:unknown')} registry_path={path} value={value}"


def _watchlist_events(event_records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    counts = Counter(_event_id(record) for record in event_records)
    summary: dict[str, dict[str, Any]] = {}
    for event_id, label in WATCHLIST_EVENT_IDS.items():
        matching = [record for record in event_records if _event_id(record) == event_id]
        summary[str(event_id)] = {
            "label": label,
            "count": counts.get(event_id, 0),
            "sample_refs": [_event_ref(record) for record in matching[:3]],
        }
    return summary


def _timeline_anchors(event_records: list[dict[str, Any]]) -> list[dict[str, str]]:
    anchors: list[dict[str, str]] = []
    for record in event_records:
        timestamp = record.get("timestamp_utc")
        if not timestamp:
            continue
        event_id = _event_id(record)
        if event_id not in WATCHLIST_EVENT_IDS:
            continue
        anchors.append(
            {
                "timestamp_utc": str(timestamp),
                "record_ref": _event_ref(record),
                "meaning": WATCHLIST_EVENT_IDS[event_id],
            }
        )
    return sorted(anchors, key=lambda item: item["timestamp_utc"])[:25]


def build_correlation_summary(registry_summary: dict[str, Any], event_summary: dict[str, Any]) -> dict[str, Any]:
    """Build a conservative cross-artifact summary without upgrading suspicion into compromise."""

    run_key_records = _records(registry_summary, "run_key_records")
    service_records = _records(registry_summary, "service_records")
    event_records = _records(event_summary, "event_records")
    event_watchlist = _watchlist_events(event_records)
    findings: list[dict[str, Any]] = []

    if event_watchlist["1102"]["count"]:
        findings.append(
            {
                "finding_id": "C001",
                "title": "Security log clear activity is present in the bounded EVTX sample.",
                "disposition": "needs_human_review",
                "evidence_refs": event_watchlist["1102"]["sample_refs"],
                "reason": "Event ID 1102 is high-signal, but this bounded run does not prove malicious intent by itself.",
            }
        )

    if run_key_records or service_records:
        registry_refs = [_registry_ref(record) for record in [*run_key_records[:3], *service_records[:3]]]
        findings.append(
            {
                "finding_id": "C002",
                "title": "Registry persistence surfaces were parsed and are available for reviewer correlation.",
                "disposition": "confirmed_artifact_presence",
                "evidence_refs": registry_refs,
                "reason": "Run keys and services are content-level artifacts; no malicious classification is asserted without corroboration.",
            }
        )

    has_high_signal_events = any(event_watchlist[str(event_id)]["count"] for event_id in (1102, 4697, 4720, 4732, 7045))
    status = "review_required" if findings and (has_high_signal_events or run_key_records or service_records) else "insufficient_evidence"

    return {
        "status": status,
        "confirmed_compromise": False,
        "registry_watchlist": {
            "run_key_records": len(run_key_records),
            "service_records": len(service_records),
            "sample_run_key_refs": [_registry_ref(record) for record in run_key_records[:3]],
            "sample_service_refs": [_registry_ref(record) for record in service_records[:3]],
        },
        "event_watchlist": event_watchlist,
        "timeline_anchors": _timeline_anchors(event_records),
        "correlation_findings": findings,
        "rejected_claims": [
            "Confirmed compromise on RD01",
            "No malicious activity found on RD01",
        ],
        "analyst_narrative": (
            "The bounded correlation layer found high-signal event and registry surfaces, "
            "including any security-log-clear or persistence records present in the sample. "
            "It deliberately keeps compromise status unconfirmed until cross-artifact timing, "
            "process, account, and persistence evidence all support the same story."
        ),
    }
