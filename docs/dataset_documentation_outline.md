# Dataset Documentation Outline

Date: 2026-05-06

Purpose: define the final dataset documentation structure before real analysis starts.

## Required Final Sections

The final dataset documentation must include:

1. Dataset identity.
2. Source and access notes.
3. Evidence inventory.
4. Scope of analysis.
5. Expected artifact families.
6. What was tested.
7. What was not tested.
8. Ground-truth or reviewer-derived method.
9. Findings summary.
10. Known limitations.
11. Reproducibility notes.
12. Safety and evidence-integrity notes.

## Dataset Identity

Required content:

- case name;
- evidence filename;
- evidence type;
- expected host role;
- expected operating-system family;
- local evidence path;
- case workspace path;
- date obtained;
- analyst/reviewer attribution.

## Source And Access Notes

Required content:

- source category;
- direct source location where appropriate;
- date source was checked;
- whether access was public, contest-provided, or otherwise restricted;
- whether the file might disappear before judging;
- fallback source or fallback dataset plan.

## Evidence Inventory

Required content after local file exists:

- exact filename;
- exact byte size;
- hash/check value if generated or provided;
- image format;
- partition overview;
- filesystem overview;
- read-only storage location;
- confirmation that generated outputs are separate.

## Scope Of Analysis

Required content:

- Windows disk triage lane;
- included artifact families;
- excluded artifact families;
- reason for exclusions;
- depth-over-breadth statement aligned with FIND EVIL judging.

## What Was Tested

Required content:

- partition listing;
- filesystem inventory;
- timeline generation;
- registry persistence review;
- event record extraction;
- claim verification;
- correction flow;
- execution log traceability.

## What Was Not Tested

Required content:

- memory analysis if not run;
- network packet analysis if not run;
- live endpoint/SIEM analysis if not run;
- full enterprise-wide correlation if not run;
- any SIFT tools not exposed through the controlled MCP surface.

## Ground Truth Method

Required content:

- official answer key status;
- expected answer source;
- reviewer-derived manifest status if needed;
- labels for confirmed fact, inference, unknown, unsupported, and contradicted;
- limitations of any non-official expected answers.

## Findings Summary

Required content after real run:

- confirmed findings;
- inferred findings;
- unsupported claims dropped;
- corrected claims;
- unknowns;
- artifact families with no useful output.

## Reproducibility Notes

Required content:

- exact command used to run the agent;
- case workspace location;
- relevant environment readiness result;
- output files generated;
- execution log location;
- known local-vs-SIFT differences.

## Current Status

The outline is ready. It becomes a completed real dataset document only after:

- selected `.E01` file exists locally;
- evidence inventory is filled from the actual file;
- SIFT-compatible run produces real outputs;
- synthetic-only language is replaced where real evidence results exist.
