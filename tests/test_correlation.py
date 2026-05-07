from src.correlation import build_correlation_summary


def test_correlation_summary_flags_event_log_clear_without_confirming_compromise() -> None:
    registry_summary = {
        "run_key_records": [
            {
                "record_id": "ev:registry:1",
                "registry_path": "Microsoft\\Windows\\CurrentVersion\\Run",
                "value_name": "SecurityHealth",
                "value_data": "%ProgramFiles%\\Windows Defender\\MSASCuiL.exe",
            }
        ],
        "service_records": [
            {
                "record_id": "ev:registry:2",
                "registry_path": "ControlSet001\\Services\\ExampleSvc",
                "value_name": "ExampleSvc",
                "value_data": "C:\\Windows\\System32\\svchost.exe -k netsvcs",
            }
        ],
    }
    event_summary = {
        "event_records": [
            {
                "record_id": "ev:event:1",
                "event_id": 1102,
                "channel": "security",
                "timestamp_utc": "2018-05-04T22:14:29.130575Z",
                "provider": "Microsoft-Windows-Eventlog",
                "rendered_message": "The audit log was cleared by Administrator.",
            },
            {
                "record_id": "ev:event:2",
                "event_id": 4624,
                "channel": "security",
                "timestamp_utc": "2018-05-04T22:14:31.319296Z",
                "provider": "Microsoft-Windows-Security-Auditing",
                "rendered_message": "An account was successfully logged on.",
            },
        ],
    }

    summary = build_correlation_summary(registry_summary, event_summary)

    assert summary["status"] == "review_required"
    assert summary["confirmed_compromise"] is False
    assert summary["event_watchlist"]["1102"]["count"] == 1
    assert summary["registry_watchlist"]["run_key_records"] == 1
    assert summary["correlation_findings"][0]["disposition"] == "needs_human_review"
    assert "Confirmed compromise on RD01" in summary["rejected_claims"]


def test_correlation_summary_records_no_confirmed_compromise_when_inputs_are_empty() -> None:
    summary = build_correlation_summary({"run_key_records": [], "service_records": []}, {"event_records": []})

    assert summary["status"] == "insufficient_evidence"
    assert summary["confirmed_compromise"] is False
    assert summary["correlation_findings"] == []
    assert "No malicious activity found on RD01" in summary["rejected_claims"]
