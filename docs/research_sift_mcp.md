# P-18 Research: SIFT Custom MCP Technical Evidence

Checked on: 2026-05-04 19:24 +03:00  
Research slug: `sift-mcp-dfir-tools`  
Query type: Type B / Type C hybrid: new build under technical uncertainty plus SDK/CLI verification.  
Depth: Standard.  
Project context: FIND EVIL! Custom MCP Server for the selected "Evidence-Locked Self-Correcting Disk Triage MCP" strategy.

## 1. Scope Boundary

This document only records verified technical facts needed by the next MCP design agent.

In scope:

- current Python MCP SDK path;
- Protocol SIFT repository structure and current integration model;
- SIFT Workstation tool availability evidence from SIFT/Protocol SIFT repos;
- machine-readable or parser-friendly CLI output for Sleuth Kit, Plaso, and RegRipper;
- starter dataset access and visible folder/file structure.

Out of scope:

- designing the MCP server schema;
- writing wrapper code;
- choosing final Python package layout;
- implementing parsers.

## 2. Plan Artifact

### Questions

- How should a Python MCP server be written using the current official SDK?
- Does Protocol SIFT already define a custom MCP server interface, or is it a Claude Code configuration layer?
- Which SIFT CLI tools can return JSON/CSV/bodyfile directly?
- Which tools require custom text/regex parsers?
- What starter datasets are visible and suitable for Windows disk-image triage?

### Evidence Needed

- Official MCP documentation and official Python SDK repository.
- `teamdfir/protocol-sift` repository files.
- `sans-dfir/sift`, `teamdfir/sift-saltstack`, and tool package evidence.
- Official Sleuth Kit manuals and Plaso docs/source.
- RegRipper GitHub source.
- Browser check of the Egnyte dataset link.

### Stop Condition

Stop when P-MCP can proceed without guessing:

- package name and stable MCP server API;
- Protocol SIFT integration surface;
- exact first-pass CLI commands and output formats;
- known parser gaps;
- dataset options and access constraints.

## 3. Confirmed Facts

### 3.1 MCP Python SDK

| Fact | Verification state | Evidence |
|---|---:|---|
| The official Python SDK package is `mcp`; latest PyPI version observed is `1.27.0`; it requires Python `>=3.10`. | verified | PyPI JSON live check: `https://pypi.org/pypi/mcp/json`; repo: `https://github.com/modelcontextprotocol/python-sdk` |
| The stable SDK documentation path for current implementation is the `v1.x` branch, not `main`. | verified | `python-sdk` README on `main` says v1.x is current stable and v2 docs on main are pre-alpha; local `v1.x` clone commit `73d458baac207cecf77d17e64c7ce3902f4bce04` dated 2026-04-13. |
| Use `FastMCP` from `mcp.server.fastmcp`, not the `MCPServer` examples from `main`, for this 2026 stable build. | verified | `v1.x` README and `docs/server.md`; `main` examples showed v2/pre-alpha imports, so they are rejected for current implementation. |
| Install command from official SDK docs is `uv add "mcp[cli]"` or `pip install "mcp[cli]"`. | verified | `https://github.com/modelcontextprotocol/python-sdk/tree/v1.x` README. |
| FastMCP tools are registered with `@mcp.tool()` and type hints/docstrings are used to derive tool metadata. | verified | `v1.x` `docs/server.md` and README quickstart. |
| FastMCP supports resources with `@mcp.resource(...)`, prompts with `@mcp.prompt()`, and tools with `@mcp.tool()`. | verified | `v1.x` README quickstart. |
| `mcp.run(transport="streamable-http")` is documented; `mcp.run()` direct execution defaults are available. | verified | `v1.x` README and examples. |
| MCP standard transports include `stdio` and Streamable HTTP; for stdio, server stdout must contain only valid MCP messages, and logging belongs on stderr. | verified | MCP transport spec: `https://modelcontextprotocol.io/specification/2025-11-25/basic/transports`. |
| Tool results can include `structuredContent`, and tool-originated errors should be returned with `isError: true` rather than as protocol errors where the LLM needs to see and self-correct. | verified | MCP tools/spec schema: `https://modelcontextprotocol.io/specification/2025-06-18/server/tools` and schema page. |
| FastMCP supports structured outputs from compatible return type annotations and Pydantic models. | verified | `v1.x` `docs/server.md` structured output section. |
| FastMCP error handling supports `ToolError`; unhandled exceptions become `isError=True`; direct `CallToolResult` can be returned for full control. | verified | `v1.x` `docs/server.md` error handling section. |
| FastMCP `Context` can be injected into tools and used for logging/progress reporting via methods such as `ctx.info`, `ctx.error`, `ctx.report_progress`. | verified | `v1.x` `docs/server.md` context section. |
| SDK has in-memory testing helper `create_connected_server_and_client_session` for MCP server tests. | verified | `v1.x` `docs/testing.md`. |

### 3.2 Protocol SIFT Repository Structure

Protocol SIFT repository checked at:

- Repo: `https://github.com/teamdfir/protocol-sift`
- Commit observed locally: `40bed7a96bfd986ea048c3b2aeb9d788b2f3400c`

Current file structure:

```text
README.md
install.sh
global/CLAUDE.md
global/settings.json
global/settings.local.json
case-templates/CLAUDE.md
analysis-scripts/generate_pdf_report.py
skills/memory-analysis/SKILL.md
skills/plaso-timeline/SKILL.md
skills/sleuthkit/SKILL.md
skills/windows-artifacts/SKILL.md
skills/yara-hunting/SKILL.md
```

Confirmed integration model:

- Protocol SIFT is currently a **Claude Code + SANS SIFT Workstation configuration kit**, not a standalone MCP server framework.
- `install.sh` installs files into `~/.claude/`: global prompt/config, local settings, skills, case template, and report generator.
- `global/settings.json` pre-approves many forensic CLI tools and denies dangerous commands such as `rm -rf`, `dd`, `wget`, `curl`, `ssh`, and `WebFetch`.
- The write/edit allow-list is scoped to `./analysis/*`, `./reports/*`, and `./exports/*`.
- A Claude Code `Stop` hook appends an audit entry to `./analysis/forensic_audit.log`.
- No `mcpServers` config, MCP server source code, or custom MCP server registration file was present in the repository at the checked commit.

Implication for P-MCP:

- A Custom MCP Server will be a new adjacent component.
- Protocol SIFT can provide forensic operating rules, tool allow/deny policy, and skill examples.
- The custom MCP server must still be explicitly registered with the client runtime. The MCP SDK README shows `claude mcp add --transport http my-server http://localhost:8000/mcp` as an example, but P-MCP must verify the final Claude Code MCP config path before implementation.

### 3.3 SIFT Workstation Tool Availability Evidence

SIFT repository status:

- `https://github.com/sans-dfir/sift` is a metadata/issue repository.
- It points to `teamdfir/sift-saltstack` as the states that do the actual work, and `teamdfir/sift-packer` as image builder.
- Commit observed for `sans-dfir/sift`: `fbca61139d1574ac8a59b239f97d524960b9f5cc`, dated 2024-02-14.
- `sans-dfir/sift` README says supported distros include Ubuntu 20.04 Focal and 22.04 Jammy and installation uses `sudo cast install teamdfir/sift-saltstack`.

SIFT SaltStack evidence:

- Repo: `https://github.com/teamdfir/sift-saltstack`
- Commit observed locally: `96b7d9898bc55264679b9ea50949ddc919f76f59`, dated 2026-04-13.
- Package states include `sift/packages/sleuthkit.sls`, `sift/packages/plaso-tools.sls`, `sift/packages/python3-plaso.sls`, and `sift/scripts/regripper.sls`.
- `sift/scripts/regripper.sls` installs RegRipper under `/usr/share/regripper`, adjusts plugin path to `/usr/share/regripper/plugins/`, and symlinks `/usr/local/bin/rip.pl` to `/usr/share/regripper/rip.pl`.
- `sift/config/symlinks.sls` includes `/usr/local/bin/rip.pl` symlink.

Protocol SIFT evidence for tool paths:

- `global/CLAUDE.md` lists Sleuth Kit tools (`fls`, `icat`, `ils`, `blkls`, `mactime`, `tsk_recover`) as system PATH tools.
- It lists Plaso tools (`log2timeline.py`, `psort.py`, `pinfo.py`) from GIFT PPA version `20240308`.
- It lists EZ Tools under `/opt/zimmermantools/`, with .NET invocation. These are not in the requested baseline utility set, but useful for later Windows artifact expansion.

## 4. CLI Tool Output Verification

### 4.1 Sleuth Kit: `mmls`

Official source:

- `https://sleuthkit.org/sleuthkit/man/mmls.html`
- Source clone: `https://github.com/sleuthkit/sleuthkit`, commit `63655c153750ea93344e85c2f46fcd7d9149b040`, dated 2026-04-27.

Purpose:

- Displays partition layout of a volume system.

Relevant documented syntax:

```bash
mmls [-t mmtype] [-o offset] [-i imgtype] [-b dev_sector_size] [-BrvV] [-aAmM] image [images]
```

Useful flags for MCP wrapper:

| Flag | Use | Machine-readable status |
|---|---|---|
| `-B` | include partition size in bytes | text table only |
| `-i imgtype` | set image type, or use `-i list` | text only |
| `-b dev_sector_size` | set device sector size | text only |
| `-o offset` | offset where the volume system starts | text only |
| `-a`, `-A`, `-m`, `-M` | allocated/unallocated/metadata filtering | text only |
| `-r` | recurse into DOS partitions | text only |
| `-v`, `-V` | verbose/version | text only |

Confirmed parser reality:

- No official JSON or CSV output flag found for `mmls`.
- P-MCP should parse the fixed-width/text table into structured records.
- Recommended MCP behavior: run `mmls -B <image>` first, parse `Slot`, `Start`, `End`, `Length`, `Size`, `Description`; reject unsupported layouts with a tool error instead of guessing.

### 4.2 Sleuth Kit: `fls`

Official source:

- `https://sleuthkit.org/sleuthkit/man/fls.html`
- Source clone: `https://github.com/sleuthkit/sleuthkit`, commit `63655c153750ea93344e85c2f46fcd7d9149b040`, dated 2026-04-27.

Purpose:

- Lists file and directory names in a disk image.

Relevant documented syntax:

```bash
fls [-adDFlpruvV] [-m mnt] [-z zone] [-f fstype] [-s seconds] [-i imgtype] [-o imgoffset] [-b dev_sector_size] image [images] [inode]
```

Useful flags for MCP wrapper:

| Flag | Use | Machine-readable status |
|---|---|---|
| `-r` | recursive directory listing | text only |
| `-p` | full path per entry | parser-friendly text |
| `-l` | long format: file type, inode, name, modified/access/changed/created times, size, uid, gid | parser-friendly text |
| `-m /` | bodyfile/time-machine format for `mactime` or Plaso bodyfile parser | machine-ingestable bodyfile, not JSON |
| `-o <sectors>` | filesystem partition offset in sectors | input control |
| `-f <type>` | force filesystem type; `-f list` lists supported types | input control |
| `-i <imgtype>` | image type; `-i list` lists supported types | input control |
| `-b <dev_sector_size>` | device sector size | input control |
| `-d`, `-D`, `-F`, `-u` | deleted/directories/files/undeleted filters | text/bodyfile depending on mode |
| `-z <zone>` | timezone for `-l` or `-m` | useful for normalized UTC handling |

Confirmed parser reality:

- No official JSON output flag found for `fls`.
- `fls -m / -o <offset> <image>` is the strongest machine-ingestable path because Plaso supports bodyfile parsing.
- `fls -r -p -o <offset> <image>` and `fls -l -o <offset> <image>` require custom parsers.
- `fls -m` output should be treated as bodyfile evidence, not directly as final normalized JSON.

Recommended commands for P-MCP to test:

```bash
mmls -B <image.E01_or_raw>
fls -r -p -o <partition_start_sector> <image>
fls -l -r -o <partition_start_sector> <image>
fls -m / -r -o <partition_start_sector> <image> > ./analysis/bodyfile.txt
```

### 4.3 Plaso: `log2timeline.py`, `psort.py`, `pinfo.py`, `psteal.py`

Official sources:

- `https://plaso.readthedocs.io/en/latest/sources/user/Using-log2timeline.html`
- `https://plaso.readthedocs.io/en/latest/sources/user/Using-psort.html`
- `https://plaso.readthedocs.io/en/latest/sources/user/Output-and-formatting.html`
- `https://plaso.readthedocs.io/en/latest/sources/user/Creating-a-timeline.html`
- Source clone: `https://github.com/log2timeline/plaso`, commit `e84736bae14793f5fe038f7ea12b704d917faf9e`, dated 2026-05-04.

Purpose:

- `log2timeline.py` extracts events from files, directories, storage media images, or devices into a `.plaso` storage file.
- `psort.py` post-processes `.plaso` storage files into output formats.
- `pinfo.py` inspects storage metadata and parser/event counts.
- `psteal.py` is a one-step parse + export frontend.

Important CLI facts:

- `log2timeline.py --storage-file OUTPUT INPUT` is official basic usage.
- `log2timeline.py` can prompt for partitions/VSS/credentials unless controlled.
- Official docs list options to avoid prompts: `--partitions`, `--vss_stores`, and `--unattended`.
- Preprocessing can determine the OS and parser preset; `--parsers` overrides this.
- `psort.py` no longer writes output to stdout as of Plaso 1.5.0; use `-w OUTPUTFILE`.
- `psort.py -o list` lists output modules.
- Official output modules include `dynamic`, `json`, `json_line`, `l2tcsv`, `tln`, `xlsx`, and others depending on optional dependencies.
- `dynamic` output supports selected fields via `--fields`.
- JSON output fields include `display_name`, `filename`, `inode`, `message`, `pathspec`, `parser`, `tag`, and `timestamp_desc`.
- `l2tcsv` is a legacy CSV format with 17 fixed fields.

Recommended parse/export commands to verify on SIFT:

```bash
log2timeline.py --storage-file ./analysis/<case>.plaso --parsers win_gen --timezone UTC <image_or_mount>
pinfo.py ./analysis/<case>.plaso
psort.py -o json_line -w ./exports/<case>_timeline.jsonl ./analysis/<case>.plaso
psort.py -o json -w ./exports/<case>_timeline.json ./analysis/<case>.plaso
psort.py -o dynamic --fields datetime,timestamp_desc,source,source_long,message,parser,display_name,tag,filename,inode -w ./exports/<case>_timeline.csv ./analysis/<case>.plaso
psort.py -o l2tcsv -w ./exports/<case>_timeline_l2tcsv.csv ./analysis/<case>.plaso
psteal.py --source <image_or_mount> -o dynamic -w ./exports/<case>_psteal.csv
```

Preferred MCP output route:

- Use `json_line` for large timelines because it is stream-friendly.
- Use `dynamic` CSV for analyst-readable exports and pivoting.
- Use `pinfo.py` after every `log2timeline.py` run to confirm parser counts and catch zero-hit failures.

### 4.4 RegRipper: `rip.pl`

Official/source evidence:

- Repo: `https://github.com/keydet89/RegRipper3.0`
- Commit observed locally: `d43d740688ca44b67ccbe91881d3f29db49cf934`, dated 2026-04-30.
- SIFT SaltStack installs/symlinks `rip.pl` under `/usr/local/bin/rip.pl`.

Relevant syntax from `rip.pl`:

```bash
Rip [-r Reg hive file] [-f profile] [-p plugin] [options]
```

Useful flags:

| Flag | Use | Machine-readable status |
|---|---|---|
| `-r <hive>` | registry hive file to parse | input control |
| `-f <profile>` | run profile such as system/software/ntuser where available | text output |
| `-p <plugin>` | run a single plugin | text output |
| `-a` | automatically run hive-specific plugins | text output |
| `-aT` | automatically run hive-specific TLN plugins | TLN-style text, better for timeline ingestion than normal prose |
| `-l` | list plugins | text output |
| `-c` with `-l` | output plugin list in CSV | only plugin list is CSV, not analysis result |

Confirmed parser reality:

- RegRipper analysis output goes to stdout and is normally human-readable text.
- No confirmed JSON output for analysis results.
- `-c` is only documented for plugin list CSV with `-l`, not for registry analysis output.
- `-aT` is the best structured-ish option because it runs hive-specific TLN plugins, but P-MCP must inspect each plugin output before treating it as structured.
- For registry artifacts, Protocol SIFT also references Eric Zimmerman `RECmd` CSV workflows. That is outside the required baseline utilities for this step but may be a lower-parser-risk fallback for Windows registry CSV in a later architecture decision.

Recommended commands to verify on SIFT:

```bash
rip.pl -l
rip.pl -l -c
rip.pl -r <SYSTEM_hive> -p compname > ./exports/regripper_compname.txt
rip.pl -r <SOFTWARE_hive> -p run > ./exports/regripper_run.txt
rip.pl -r <SYSTEM_hive> -aT > ./exports/regripper_system_tln.txt
```

Tools requiring custom parsers:

- `mmls`: text table parser.
- `fls` normal/long path listing: text parser.
- `RegRipper` normal plugin output: custom parser per plugin or conservative evidence block storage.
- `RegRipper -aT`: TLN parser likely feasible, but still must be validated plugin by plugin.

Tools with usable machine-readable output:

- `fls -m`: bodyfile/time-machine format, accepted by timeline tooling.
- `psort.py`: `json`, `json_line`, `dynamic`, `l2tcsv`.
- `pinfo.py`: Plaso source includes JSON output support; P-MCP should verify exact command syntax on installed SIFT (`pinfo.py --help`) because public user docs emphasize text usage but source has `--output-format`.
- `RegRipper -l -c`: CSV for plugin listing only.

## 5. Starter Dataset Access

Dataset URL:

- `https://sansorg.egnyte.com/fl/HhH7crTYT4JK`

Browser verification:

- Page opened successfully on 2026-05-04.
- Page title: `HACKATHON-2026`.
- Shared by Rob Lee.
- Page indicated availability until Jun 17, 2026.
- Public page rendered folder/file listings, but raw directory API was not extracted. Large downloads were not attempted.

Visible root folders:

```text
HACKATHON-2026/
  Compromised APT Attack Scenarios/
  Standard Forensic Case/
```

Visible `Compromised APT Attack Scenarios/`:

```text
SRL-2015-Compromised Enterprise Network/
SRL-2018-Compromised Enterprise Network/
```

Visible `SRL-2015-Compromised Enterprise Network/` files:

```text
win7-32-nromanoff-10.3.58.5.zip              14.8 GB
win7-64-nfury-10.3.58.6.zip                  13.3 GB
win2008R2-controller-10.3.58.4.zip           16.3 GB
xp-tdungan-10.3.58.7.zip                     11.2 GB
```

Visible `SRL-2018-Compromised Enterprise Network/` files/folders:

```text
SRL-2018/                                    folder
base-dc-cdrive.E01                           11.5 GB
base-file-cdrive.E01                         15.3 GB
base-rd-01-cdrive.E01                        16.6 GB
base-rd-02-cdrive.E01                        16 GB
base-wkstn-01-c-drive.E01                    15.8 GB
base-wkstn-05-cdrive.E01                     13.8 GB
dmz-ftp-cdrive.E01                           11.9 GB
```

Visible `Standard Forensic Case/` files:

```text
ROCBA-BACKGROUND.pptx                         38.3 MB
Rocba-Memory.zip                              5.3 GB
```

Dataset recommendation for next step:

- For the disk-image MCP MVP, use `SRL-2018-Compromised Enterprise Network` first because the visible files are `.E01` Windows disk images, which match the selected Windows disk triage lane.
- Avoid starting with `Standard Forensic Case` for this specific MVP because the visible evidence is memory-oriented (`Rocba-Memory.zip`) plus a background presentation, not a first-pass Windows disk image.

Blocked/unknown:

- Exact internal contents of ZIP/E01 files were not inspected because the files are very large and downloading was not necessary for this research step.
- No ground-truth answer key was visible from the browser listing.

## 6. Working Hypotheses

| Hypothesis | Why it is plausible | Verification needed |
|---|---|---|
| `SRL-2018/base-rd-01-cdrive.E01` is the best first MVP target. | Protocol SIFT case template mentions `rd01` as a primary compromise host in an SRL scenario; Egnyte exposes `base-rd-01-cdrive.E01`. | Download or mount enough metadata to confirm OS, partition offsets, and expected artifacts. |
| `psort.py -o json_line` should be the default timeline export for MCP ingestion. | Plaso docs list JSON Lines output; JSONL is safer for large timelines than one giant JSON file. | Run on SIFT with installed Plaso version and inspect output size/schema. |
| `RegRipper -aT` can feed a simple TLN parser for registry timeline facts. | `rip.pl` documents `-aT` as hive-specific TLN plugins. | Run against real hives and validate field separators/timestamps across plugins. |
| Protocol SIFT can consume a custom MCP server through Claude Code MCP registration. | MCP SDK README shows `claude mcp add` example. | Verify exact Claude Code config behavior in the target SIFT VM. |

## 7. Contradictions And Resolution

### MCP SDK `main` vs `v1.x`

Contradiction:

- `main` branch contained v2/pre-alpha documentation/examples using `MCPServer`.
- The README states v1.x is current stable.
- PyPI live check shows stable `mcp 1.27.0`.

Resolution:

- Use package `mcp` from PyPI and SDK `v1.x` docs for implementation.
- Reject `main` examples that import `mcp.server.mcpserver.MCPServer` for the current build.

Confidence: 92/100 because this is confirmed by official SDK README, PyPI, and branch inspection.

### SIFT repo vs actual SIFT package source

Contradiction:

- `sans-dfir/sift` is expected to describe SIFT, but it is a metadata repository.
- Actual package states live in `teamdfir/sift-saltstack`.

Resolution:

- Use `sans-dfir/sift` for installation/metadata and `teamdfir/sift-saltstack` for package/tool presence.

Confidence: 88/100 because source repos agree, but exact installed VM versions still need runtime confirmation.

### RegRipper CSV expectations

Contradiction:

- Some users may expect `-c` to mean CSV output generally.
- `rip.pl` syntax indicates `-c` outputs plugin list in CSV when used with `-l`.

Resolution:

- Do not claim RegRipper analysis output is CSV/JSON.
- Treat analysis output as text/TLN depending on plugin mode.

Confidence: 90/100 because confirmed from current source code and SIFT install state.

## 8. Negative Results

- No JSON output flag found for `mmls`.
- No JSON output flag found for `fls`.
- No CSV analysis-output mode confirmed for RegRipper plugin results.
- No custom MCP server implementation found inside `teamdfir/protocol-sift`.
- No visible answer key/ground truth file found in Egnyte listing via browser.
- No safe need to download multi-GB datasets during this research step.

## 9. Sources

| Source | Type | Date/commit observed | Used for |
|---|---|---:|---|
| `https://github.com/modelcontextprotocol/python-sdk/tree/v1.x` | official SDK GitHub | commit `73d458b`, 2026-04-13 | Python SDK stable API, FastMCP patterns |
| `https://pypi.org/pypi/mcp/json` | package registry | live 2026-05-04 | `mcp` version `1.27.0`, Python requirement |
| `https://modelcontextprotocol.io/specification/2025-11-25/basic/transports` | official spec | published/crawled current | stdio and Streamable HTTP transport rules |
| `https://modelcontextprotocol.io/specification/2025-06-18/server/tools` | official spec | current spec page | `structuredContent`, `isError`, tool error semantics |
| `https://github.com/teamdfir/protocol-sift` | GitHub source | commit `40bed7a`, checked 2026-05-04 | Protocol SIFT repository structure and Claude config model |
| `https://github.com/sans-dfir/sift` | GitHub source | commit `fbca611`, 2024-02-14 | SIFT metadata repo and install references |
| `https://github.com/teamdfir/sift-saltstack` | GitHub source | commit `96b7d98`, 2026-04-13 | SIFT package/tool presence |
| `https://sleuthkit.org/sleuthkit/man/mmls.html` | official manual | page checked 2026-05-04 | `mmls` syntax and flags |
| `https://sleuthkit.org/sleuthkit/man/fls.html` | official manual | page checked 2026-05-04 | `fls` syntax, `-m`, `-l`, `-o`, bodyfile path |
| `https://github.com/sleuthkit/sleuthkit` | GitHub source | commit `63655c1`, 2026-04-27 | Sleuth Kit current source/manpage confirmation |
| `https://plaso.readthedocs.io/en/latest/sources/user/Using-log2timeline.html` | official docs | 20260427 docs | `log2timeline.py` source/storage behavior |
| `https://plaso.readthedocs.io/en/latest/sources/user/Using-psort.html` | official docs | 20260427 docs | `psort.py` output formats and `-w` requirement |
| `https://plaso.readthedocs.io/en/latest/sources/user/Output-and-formatting.html` | official docs | 20260427 docs | JSON/JSONL/dynamic/l2tcsv fields |
| `https://github.com/log2timeline/plaso` | GitHub source | commit `e84736b`, 2026-05-04 | latest Plaso source confirmation |
| `https://github.com/keydet89/RegRipper3.0` | GitHub source | commit `d43d740`, 2026-04-30 | RegRipper flags and output limits |
| `https://sansorg.egnyte.com/fl/HhH7crTYT4JK` | browser-verified dataset listing | checked 2026-05-04 | starter dataset folder/file structure |

## 10. Handoff For P-MCP

P-MCP should start from these decisions:

- Use official `mcp` package, stable `v1.x`, `FastMCP`.
- Design tools with typed inputs/outputs and structured return models.
- Use `ToolError` / `isError=True` for expected forensic failures so the agent can self-correct.
- For stdio transport, never print logs to stdout.
- Prefer Streamable HTTP locally if Claude Code setup allows it; otherwise stdio is spec-supported.
- Treat Protocol SIFT as Claude Code configuration + skill baseline, not as an existing MCP framework.
- Expose wrapper functions around proven CLI commands, but do not expose generic shell.
- For first disk MVP, prefer:
  - `mmls -B` text parser for partitions;
  - `fls -m` bodyfile for timeline ingestion;
  - `fls -r -p` and `fls -l` custom parsers for file inventory;
  - `log2timeline.py` + `psort.py -o json_line` for normalized timeline records;
  - RegRipper text/TLN output only if parser confidence is bounded and documented.

## 11. Research Snapshot

### Research Slug

- Slug: `sift-mcp-dfir-tools`

### Query Type

- Type: new/technical
- Depth: Standard
- Evidence quality: high for MCP SDK, Protocol SIFT structure, Sleuth Kit/Plaso flags; medium-high for SIFT installed versions because VM runtime confirmation remains.

### Query Log

| Query/check | Found | Used |
|---|---|---|
| MCP Python SDK official docs / GitHub | Official SDK repo, PyPI package, v1.x branch | yes |
| Protocol SIFT GitHub | Installer, global settings, skills, case template | yes |
| SIFT GitHub | Metadata repo pointing to saltstack/packer | yes |
| SIFT SaltStack packages | Sleuth Kit, Plaso, RegRipper install states | yes |
| Sleuth Kit `mmls`/`fls` docs | Official manpages and source man files | yes |
| Plaso output docs/source | Official docs and current source | yes |
| RegRipper source | GitHub `rip.pl` syntax | yes |
| Egnyte dataset link | Browser-rendered public listing | yes |

### Freshness

- Checked on: 2026-05-04 19:24 +03:00.
- Current enough: MCP SDK/PyPI, Plaso source, Sleuth Kit source, RegRipper source, SIFT SaltStack.
- Stale or unresolved: `sans-dfir/sift` metadata repo is older; exact installed SIFT VM versions must be checked in runtime.

### Main Contradictions

- MCP SDK `main` vs stable `v1.x`: resolved in favor of `v1.x`.
- SIFT metadata repo vs SaltStack package source: resolved by using SaltStack for package evidence.
- RegRipper `-c` expectation: resolved as plugin-list CSV only.

### What Is Still Unknown

- Exact Claude Code MCP server registration behavior in the SIFT VM.
- Exact versions installed in the downloaded SIFT OVA.
- Whether `pinfo.py --output-format json` is available in the SIFT Plaso version.
- Internal contents and ground truth of the large Egnyte datasets.

### Confidence

- Overall: 86/100.
- MCP SDK stable path: 92/100.
- Protocol SIFT structure: 95/100.
- Sleuth Kit output facts: 90/100.
- Plaso output facts: 91/100.
- RegRipper output facts: 90/100.
- Dataset structure: 78/100 because listing was browser-verified but large files were not downloaded.

### Provenance Block

Sources reviewed:

- Official MCP docs/spec, MCP Python SDK repo/PyPI, Protocol SIFT repo, SIFT metadata/saltstack/packer repos, Sleuth Kit manual/source, Plaso docs/source, RegRipper source, Egnyte dataset page.

Sources used:

- Listed in section 9.

Sources rejected:

- Blog/tutorial pages about RegRipper because current GitHub source was stronger.
- MCP SDK `main` examples using v2/pre-alpha `MCPServer` API for implementation guidance.
- Generic SIFT package assumptions not backed by `sift-saltstack` or Protocol SIFT files.

Major verified claims:

- `mcp` stable package path and FastMCP v1.x API.
- Protocol SIFT current repo does not contain a custom MCP server.
- Sleuth Kit `mmls`/`fls` do not expose documented JSON output.
- Plaso `psort.py` supports `json`, `json_line`, `dynamic`, and `l2tcsv`.
- RegRipper analysis output is stdout text/TLN; CSV is only confirmed for plugin list.
- Egnyte page exposes large `.E01` and ZIP starter evidence.

Major inferred claims:

- `json_line` should be preferred for large Plaso timeline MCP ingestion.
- `SRL-2018` is the best first disk-image MVP dataset.
- RegRipper normal plugin output should be handled conservatively as text evidence unless parser coverage is explicitly tested.

Open gaps:

- Runtime command availability and exact versions inside the SIFT VM.
- Ground truth/answer key availability.
- Final Claude Code MCP registration method.

[P-18 V2 COMPLETE: 2026-05-04 19:24 | Type: new/technical | Depth: Standard | Check: Critical 5/5 | Important 5/5 | Recommended 4/4 | Confidence: 86/100]
