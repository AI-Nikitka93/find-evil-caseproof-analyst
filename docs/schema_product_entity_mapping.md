# Schema To Product Entity Mapping

Date: 2026-05-06

Purpose: verify that current contract schemas still match the product entities CaseProof Analyst needs.

## Product Entities

| Product entity | Contract/schema surface | Current status |
|---|---|---|
| Case | `case_id`, `CaseWorkspace`, `CaseState` | Present |
| Evidence source | `evidence_path`, `evidence_id`, `CaseOpenReadonlyInput`, `CaseOpenReadonlyOutput` | Present |
| Evidence record | `EvidenceReference`, `PartitionInfo`, `FileMetadataRecord`, `TimelineRecord`, `RegistryPersistenceRecord`, `EventRecord` | Present |
| Candidate claim | `VerifyClaimInput.claim_id`, `VerifyClaimInput.claim_text` | Present |
| Verified finding | `ClaimVerificationResult`, `VerifyClaimOutput` | Present |
| Correction event | `WriteExecutionLogInput.correction_reason`, parser status, verifier status | Present |
| Execution log | `WriteExecutionLogInput`, `ExecutionLogRecord`, `WriteExecutionLogOutput` | Present |

## Tool Coverage

| Tool | Product entity covered |
|---|---|
| `case_open_readonly` | Case, evidence source, workspace boundary |
| `list_partitions` | Evidence records for partition context |
| `filesystem_inventory` | Evidence records for filesystem context |
| `build_timeline` | Evidence records for event/time sequence |
| `extract_registry_persistence` | Evidence records for persistence context |
| `extract_event_records` | Evidence records for Windows event context |
| `verify_claim` | Candidate claim to verified finding |
| `write_execution_log` | Execution log and correction event |

## Gaps Noted

No schema gap blocks the current first-release product shape.

Still open for later release depth:

- final real evidence book format;
- correction ledger presentation;
- real accuracy report replacement after `.E01` validation;
- reviewer-derived manifest promotion after actual evidence review.

These are output/reporting depth gaps, not public MCP contract gaps.

## Acceptance

The mapping is acceptable because:

- every core product entity has a schema surface;
- every public tool contributes to a product entity;
- no extra product entity depends on a hidden generic shell;
- correction and uncertainty can be represented without fake success;
- `scripts/audit_release_controls.py` checks the current schema/product markers.
