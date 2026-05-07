# Pre-Release Freshness Checklist

Date: 2026-05-07

Purpose: list external facts that must be rechecked before submission because they can change before judging.

## Sources To Recheck

| Fact | Current source | Current status |
|---|---|---|
| Contest deadline | FIND EVIL Devpost overview | Deadline shown as Jun 15, 2026 at 11:45pm EDT. |
| Required submission components | FIND EVIL Devpost overview | Eight required components listed; missing any one means elimination. |
| Demo video rule | FIND EVIL Devpost overview | Demo video max is 5 minutes and must show live terminal execution against real case data. |
| Starter evidence access | FIND EVIL Devpost resources | Starter case data link is still listed on the resources page. |
| SIFT download path | SANS SIFT Workstation page | SIFT Workstation remains the official workstation download page. |
| Protocol SIFT install command | FIND EVIL Devpost resources | Resources page still references the Protocol SIFT package install command. |
| Public repo license requirement | FIND EVIL Devpost overview | Public GitHub repository with MIT or Apache 2.0 license is required. |
| AI runtime/provider constraints | Current local environment and provider docs | Must be rechecked before final demo to avoid surprise model or account changes. |
| MCP Python SDK version | PyPI and local `py -m pip show mcp` | `mcp 1.27.0` is current for this project and installed locally; use a virtual environment to avoid unrelated package conflicts. |
| Selected evidence presence | Local ignored `evidence/` folder and dataset docs | `base-rd-01-cdrive.E01` is present locally and remains excluded from the public repository. |
| SIFT-compatible command surface | `py scripts\check_env.py --strict` | SIFT-compatible commands are available through WSL for current local validation. |

## Required Recheck Moments

Recheck these facts:

- before downloading final evidence;
- before recording the demo video;
- before publishing or updating the public repository;
- before submitting Devpost materials;
- after any major change to SIFT, Protocol SIFT, or model runtime assumptions.

## What To Record

Each freshness update must record:

- date checked;
- source URL or local command;
- fact checked;
- result;
- whether any project document needs updating;
- whether the change blocks release.

## Fast-Changing Facts

The fastest-changing project facts are:

- starter evidence link and file availability;
- participant/resource page content;
- SIFT download/version notes;
- Protocol SIFT setup instructions;
- model/API availability and local key readiness;
- public submission rules;
- demo and repository requirements.

## Current Live Sources

Checked on 2026-05-06:

- FIND EVIL overview: `https://findevil.devpost.com/`
- FIND EVIL resources: `https://findevil.devpost.com/resources`
- SIFT Workstation: `https://www.sans.org/tools/sift-workstation/`

Refreshed on 2026-05-07:

- FIND EVIL overview: `https://findevil.devpost.com/`
- FIND EVIL rules: `https://findevil.devpost.com/rules`
- Protocol SIFT repository HEAD: `40bed7a96bfd986ea048c3b2aeb9d788b2f3400c`
- MCP Python SDK / PyPI: `mcp 1.27.0`

## No-Go Conditions

Stop release if:

- Devpost requirements changed and local artifacts no longer match;
- starter evidence is no longer accessible and no fallback evidence is validated;
- SIFT setup path changed enough to break judge instructions;
- public repository/license requirement is not satisfied;
- demo video does not show real case data and visible self-correction.
