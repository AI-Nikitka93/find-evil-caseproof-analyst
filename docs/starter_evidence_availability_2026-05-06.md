# Starter Evidence Availability

Checked: 2026-05-06  
Purpose: support Phase 2 dataset selection without pretending that a local real evidence image exists.

## Current Public Resource Status

The live FIND EVIL resources page confirms that starter case data is provided through:

```text
https://sansorg.egnyte.com/fl/HhH7crTYT4JK
```

The same page describes the resource as:

```text
Sample disk images and memory captures provided at launch.
```

## Current Browser Limitation

The Egnyte shared-folder page opens, but the file listing is rendered dynamically and the current text fetch only returns a loading shell.

This means the current run confirms the starter evidence link exists, but it does not independently refresh the full folder listing through the static text fetch.

## Last Known File Listing From Project Research

The project research file `docs/research_sift_mcp.md` recorded the following visible disk-image candidates from the same Egnyte share on 2026-05-04:

```text
SRL-2018-Compromised Enterprise Network/
  base-dc-cdrive.E01
  base-file-cdrive.E01
  base-rd-01-cdrive.E01
  base-rd-02-cdrive.E01
  base-wkstn-01-c-drive.E01
  base-wkstn-05-cdrive.E01
  dmz-ftp-cdrive.E01
```

## Availability Decision

Current usable decision:

- the official starter evidence resource still exists on the live Devpost resources page;
- the strongest known candidate remains `base-rd-01-cdrive.E01`;
- the file must still be downloaded or otherwise provided locally before inventory, chain-of-custody notes, and real validation can be completed.

## What Must Be Rechecked After Download

After the file is available locally:

- exact filename;
- exact byte size;
- evidence hash if available or generated locally;
- whether SIFT tools can read it;
- partition structure;
- whether it contains enough artifacts for the intended demo story.
