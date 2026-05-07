# Architecture

This project uses a narrow Custom MCP Server instead of broad shell access. The
agent can request forensic facts through typed, read-only tools, while evidence
mutation and generic command execution are outside the MCP surface.

Visual rule for public diagrams: forensic clarity, evidence-first structure,
and no decorative dashboard framing.

```mermaid
flowchart LR
    Evidence["SANS SIFT Workstation<br/>Evidence: Windows disk image"] --> Server["Custom MCP Server<br/>src/server.py"]

    subgraph Wrappers["Read-only SIFT wrappers"]
        MMLS["mmls<br/>partition table"]
        FLS["fls<br/>filesystem inventory"]
        PSORT["log2timeline.py + psort.py<br/>JSON Lines timeline"]
        RIP["rip.pl<br/>registry persistence"]
    end

    Server --> MMLS
    Server --> FLS
    Server --> PSORT
    Server --> RIP

    Server <-->|"MCP stdio boundary"| Agent["AI Agent<br/>src/agent.py<br/>Anthropic + OpenAI-compatible provider loop"]

    Agent --> Verifier["Claim verifier<br/>verify_claim"]
    Agent --> Audit["Audit logging<br/>write_execution_log"]

    Verifier --> Outputs["Outputs"]
    Audit --> Outputs

    Outputs --> Report["report.md"]
    Outputs --> Logs["agent_execution_log.jsonl"]
    Outputs --> Accuracy["docs/accuracy_report.md"]
```

## Security Boundary

- The original evidence image is an input source only.
- Output files are written under the case workspace.
- The server exposes fixed MCP tools, not a generic shell.
- Backend command execution uses argument lists and allowlisted tool families.
- Destructive actions such as `rm`, overwrite, delete, or raw command execution
  are not routable through the MCP server.
- Findings must pass through `verify_claim` before being reported as confirmed.

## Judge-Readable Trust Boundary

For judging purposes, the architecture has one simple trust claim:

> The agent can ask for forensic facts, but it cannot ask the product to mutate
> the original evidence or run arbitrary shell commands.

This matters because the FIND EVIL! submission is evaluated on constraint
implementation and audit trail quality, not only on whether the final report
looks plausible.

Reviewer-facing guarantees:

- the evidence file is registered as read-only case input;
- the public MCP surface is limited to eight named forensic actions;
- generated reports, logs, indexes, and derived artifacts are separated from
  the original evidence path;
- parser failures become visible uncertainty instead of silent success;
- candidate findings are checked against collected evidence before becoming
  confirmed findings;
- unsupported or conflicted claims must be downgraded, dropped, or routed to
  human review;
- execution logs let reviewers trace a finding back to the tool action that
  produced the supporting evidence.

Current limitation:

- local API readiness does not equal full autonomous investigation completion;
  the real bounded CASE-RD01 pass exists through a SIFT-compatible WSL command
  surface and includes bounded SOFTWARE Run-key/SYSTEM service parsing,
  bounded EVTX event parsing, and bounded registry/event correlation, but full
  Plaso timeline and deeper process/account corroboration remain open.

## Judge-Readable Trust Boundary Diagram

```mermaid
flowchart LR
    Evidence["Original Evidence<br/>input-only disk image"] --> Open["case_open_readonly"]
    Open --> Server["Custom MCP Server<br/>eight fixed tools"]
    Agent["AI Agent<br/>bounded loop"] <-->|"MCP stdio"| Server
    Server --> Tools["Read-only forensic tools<br/>mmls, fls, timeline, registry, events"]
    Tools --> Workspace["Generated case workspace<br/>reports, logs, derived artifacts"]
    Workspace --> Outputs["Final outputs<br/>report, evidence book, correction ledger, accuracy report, logs"]
    Unsafe["Unsafe mutation request<br/>delete, overwrite, raw shell"] -. "not routable" .-> Boundary["Safety boundary"]
    Evidence -. "never written by product" .-> Boundary
```

## Evidence Chain Diagram

```mermaid
flowchart LR
    Finding["Final Finding"] --> Claim["Candidate Claim"]
    Claim --> Evidence["Evidence Record"]
    Evidence --> Action["Execution Action"]
    Action --> Source["Source Reference"]
    Source --> Review["Reviewer can replay or inspect"]
```

## Correction Loop Diagram

```mermaid
flowchart LR
    Unsupported["Unsupported Candidate Claim"] --> Challenge["Verifier Challenge"]
    Challenge --> Followup["Targeted Follow-up"]
    Followup --> Corrected["Corrected"]
    Followup --> Downgraded["Downgraded"]
    Followup --> Dropped["Dropped"]
    Followup --> Human["Needs Human Review"]
```

## Runtime Flow

1. `src/agent.py` starts `src.server` over MCP stdio.
2. The agent opens the case with `case_open_readonly`.
3. The agent gathers partition, filesystem, timeline, registry, and event
   evidence through typed MCP calls.
4. Candidate findings are verified with `verify_claim`.
5. Agent actions and corrections are written through `write_execution_log`.
6. The final analyst report is written to `report.md`.

## Current Eval Status

`docs/accuracy_report.md` now separates the real bounded CASE-RD01 evidence pass
from the historical synthetic fixture. The real pass demonstrates read-only
evidence access, volume boundary handling, high-signal artifact discovery,
self-correction for an unsupported compromise claim, and replayable execution
logs. It is not a full incident reconstruction.
