# Freshness Dependency Register

Checked: 2026-05-07
Purpose: keep volatile contest, runtime, dependency, and evidence assumptions
current for the final FIND EVIL submission package.

## Freshness-Sensitive Dependencies

| Dependency | Why it can change | Current verified state | Recheck point |
|---|---|---|---|
| FIND EVIL Devpost rules | Deadline, submission wording, resources, and participant count can change. | Live overview/rules still require a working Protocol SIFT/SIFT agentic project, public GitHub repo, live terminal video, architecture diagram, dataset docs, accuracy report, try-it-out instructions, and execution logs. Deadline remains Jun 15, 2026 @ 11:45pm EDT. | Before demo recording and before final submission. |
| SIFT Workstation download | OVA version, hash values, install instructions, and supported paths can change. | SANS page shows SIFT Workstation download updated Apr 24, 2026, OVA size 8.81GB, Protocol SIFT install command, and Ubuntu 22.04 install path. | Before real environment setup and before try-it-out instructions are finalized. |
| Protocol SIFT repository | Install files, Claude Code guidance, allowed tools, and case templates can change. | `git ls-remote https://github.com/teamdfir/protocol-sift.git HEAD` returns `40bed7a96bfd986ea048c3b2aeb9d788b2f3400c`, matching prior research. | Before final integration instructions and before public README finalization. |
| SIFT repository / install path | Cast install guidance and repository ownership can change. | GitHub redirects to `teamdfir/sift`; install section says Cast replaced SIFT CLI and uses `sudo cast install teamdfir/sift-saltstack`. | Before SIFT install docs are published. |
| Starter evidence availability | Shared case files may move, expire, or require access. | Selected `base-rd-01-cdrive.E01` is present locally under ignored `evidence/`; public docs must still avoid publishing evidence bytes or raw case outputs. | Before video and before any public artifact refresh. |
| Forensic tool behavior | Installed versions and output fields can differ inside the target SIFT environment. | SIFT-compatible commands are available through WSL for the current validation path; official clean SANS SIFT OVA validation remains a separate pre-submission check if time allows. | Before final video and before judge-machine claims. |
| AI runtime availability | Models, rate limits, spend limits, request limits, and availability can change. | OpenRouter is the current selected free/low-cost implemented runtime path; Groq is implemented and currently passes API readiness; Anthropic remains implemented if a valid key is available. | Before final demo and before public runtime claims. |
| Public repository requirements | License visibility and public-hosting behavior can change. | Contest requires public repository and MIT or Apache 2.0 license. | Before repository publication and final submission. |
| MCP Python SDK | Official SDK release and structured-output behavior can change. | PyPI shows `mcp 1.27.0`; active local runtime now has `mcp 1.27.0` installed, matching `requirements.txt`. | Before final local gates and clean-machine setup. |

## Current SIFT / Protocol SIFT Picture

Verified on 2026-05-07:

- FIND EVIL directs participants to SANS SIFT Workstation and Protocol SIFT.
- SANS SIFT page describes Protocol SIFT as experimental and separate from core SIFT Workstation.
- SANS SIFT page states Protocol SIFT can be installed after launching SIFT by running the Protocol SIFT install command.
- SANS SIFT page warns Protocol SIFT has not been validated for forensic soundness or evidentiary reliability and remains in initial research stage.
- SIFT Workstation supports forensic investigation workflows and evidence image support including raw and E01-style evidence handling paths.
- Protocol SIFT repository describes a Claude Code + SANS SIFT Workstation configuration, not a replacement for the custom CaseProof MCP boundary.
- SIFT repository install guidance currently points to Cast and `teamdfir/sift-saltstack`.
- Current CaseProof validation uses a WSL SIFT-compatible command surface, not a claim that the official SANS SIFT OVA has been clean-machine validated.

Product implication:

- Public copy must not imply that Protocol SIFT itself is court-admissible or production-proven.
- CaseProof must keep its own accuracy/trust package honest.
- Real validation inside the target environment remains mandatory.

## Current AI Runtime Constraints

Verified on 2026-05-07:

- The implemented runtimes in this repository are Anthropic, OpenRouter, and
  Groq through `src.agent`.
- Local readiness check selects OpenRouter without printing secret values.
- Anthropic API requires an account and API key or configured federation; it enforces request, rate, and spend limits that vary by account and usage tier.
- Groq is available as an OpenAI-compatible external API surface and documents rate limits, spend limits, model permissions, service tiers, production checklist, and security onboarding.
- OpenRouter provides an external model-routing surface and has its own key/account behavior and model availability constraints.
- In this project, OpenRouter and Groq adapters are implemented; OpenRouter is
  the selected demo path and Groq currently passes API readiness.
- Active Python dependency alignment was refreshed with `py -m pip install -r requirements.txt`; `mcp 1.27.0` is installed for this project run. A non-project package may still require a different MCP version, so judges should use an isolated virtual environment.

Public-claim rule:

- Do not claim a final provider path unless the public demo records that
  provider successfully.
- Do not print, copy, or store API keys in docs or logs.
- Do not promise stable cost, latency, limits, or model availability without a final pre-release check.

## Assumptions That Must Be Rechecked Before Demo And Submission

- Devpost deadline and required artifacts.
- Video length and visibility requirements.
- Public repository license requirements.
- SIFT Workstation download/install instructions.
- Protocol SIFT install instructions.
- Starter evidence availability and access requirements.
- Selected evidence file integrity and usability.
- Required forensic tool availability inside SIFT.
- AI runtime account limits and model availability.
- Public README claims about supported runtimes and real validation.

## Update Cycle

Before demo recording:

- re-open Devpost;
- re-open SANS SIFT page;
- re-open Protocol SIFT repository;
- re-run API readiness without printing secrets;
- re-run SIFT readiness in the actual analysis environment.

Before final submission:

- repeat the same checks;
- update this register with the final check date;
- remove or downgrade any public claim that no longer matches live sources.
