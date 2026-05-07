# Visual QA Checklist

Date: 2026-05-06

Purpose: close the Phase 6 visual QA gate without using visual polish to hide
real validation gaps.

## Required Checks

| Check | Required result |
|---|---|
| No clipped text | Repository-rendered headings, tables, diagrams, paths, and status labels must wrap safely. |
| Diagrams readable in repository view | Mermaid diagrams must have clear labels and simple left-to-right flow. |
| No decorative clutter | Public docs must avoid decorative dashboard language and threat-map theater. |
| No misleading green status | Blocked validation states must remain blocked, not success-colored. |
| Evidence-first hierarchy | README and diagrams must lead with promise, quick status, real validation status, how to run, artifacts, limitations, and contribution path. |
| No visual masking | Visual polish cannot close, hide, or soften real SIFT validation blockers. |

## Current Gate Result

Current visual QA status is controlled by:

- `py scripts\audit_visual_package.py --json --strict`
- `py scripts\audit_design_quality.py --json --strict`

These checks block missing diagram surfaces, missing degraded-state language,
unfinished public-copy markers, decorative dashboard framing, and weak design
package coverage.
