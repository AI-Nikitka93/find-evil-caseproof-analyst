# Demo Host Selection Criteria

Date: 2026-05-06

Purpose: define how to choose the best host/image inside the starter dataset for the live demo.

## Selection Goal

Choose the host that best supports a short, credible live terminal demo:

- real case data;
- visible evidence-backed findings;
- at least one self-correction sequence;
- no unsupported final claims;
- understandable story for judges.

## Candidate Priority

Current recommended first candidate:

```text
SRL-2018-Compromised Enterprise Network / base-rd-01-cdrive.E01
```

Fallback candidates:

```text
base-wkstn-01-c-drive.E01
base-file-cdrive.E01
base-dc-cdrive.E01
```

## Selection Criteria

| Criterion | Pass condition |
|---|---|
| Evidence availability | File can be obtained and stored locally without corrupt download. |
| SIFT readability | Required forensic tools can read the image and produce useful output. |
| Artifact richness | Partition, filesystem, timeline, registry, and event paths produce enough data for a meaningful story. |
| Correction potential | The case naturally allows an unsupported or incomplete initial claim to be corrected through targeted follow-up. |
| Demo time fit | The selected workflow can run or be prepared within the live video constraints without hiding the important traceability story. |
| Judge clarity | A non-specialist judge can understand what was found, what was rejected, and why the final report is safer than a generic AI answer. |
| Evidence safety | Original evidence remains input-only; outputs are written only to the case workspace. |
| Reproducibility | The README can explain how a judge can repeat the same run or inspect the same outputs. |

## Disqualification Criteria

Do not use a host/image for the primary demo if:

- the image cannot be read reliably;
- it produces only empty or trivial outputs;
- the story depends on speculation rather than evidence;
- the self-correction moment has to be staged;
- output volume makes the demo impossible to explain;
- the run requires manual hidden fixes;
- evidence safety cannot be shown clearly.

## Demo Story Requirements

The selected host must support:

- opening the case through the controlled tool surface;
- gathering at least two different artifact families;
- proposing or evaluating candidate claims;
- rejecting, downgrading, or correcting at least one claim;
- writing a final report;
- preserving an execution log that links findings to tool calls.

## Current Decision

`base-rd-01-cdrive.E01` remains the first candidate, but the final demo host is not locked until:

- the file exists locally;
- SIFT readability is confirmed;
- at least one correction-worthy artifact path is observed;
- runtime is acceptable for the final demo workflow.
