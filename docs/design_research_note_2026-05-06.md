# Design Research Note

Date: 2026-05-06

Purpose: close the first Phase 6 design slice with concrete design evidence,
without turning the project into a decorative dashboard or copying third-party
assets, text, or layouts.

## Visual Reference Brief

Target visual category:

- serious forensic and audit documentation;
- security operations readability;
- evidence review surfaces;
- traceability diagrams;
- generated case dossiers.

Reference direction:

- use dense but calm information hierarchy;
- separate confirmed, inferred, unsupported, blocked, and human-review states;
- make evidence chains readable before any decoration;
- make readiness blockers visible and not greenwashed;
- keep original evidence and generated workspace visually separate.

Non-copying rule:

- references are used only as evidence of design patterns and anti-patterns;
- no third-party layouts, icons, screenshots, brand language, or visual assets
  are copied into the project.

## Lazyweb Status And Stop Condition

Checked candidate workflow: aboul3ata/lazyweb-skill.

Current product decision:

- Lazyweb is useful when screenshot-based visual evidence is required for a UI,
  pricing page, dashboard, or onboarding comparison.
- This project currently needs documentation visuals and generated evidence
  dossier hierarchy more than a full UI screen benchmark.
- Therefore screenshot-based Lazyweb research is not required for this slice.

Lazyweb stop condition if used later:

- enough references exist to cover report, evidence book, correction ledger,
  readiness state, and architecture diagram surfaces;
- anti-patterns are identified;
- findings are translated into project-specific design changes;
- no direct copying of another product's assets, text, layout, or brand occurs.

## Design-To-Code Repository Review

Reviewed candidates:

- google-labs-code/design.md
- VoltAgent/awesome-design-md
- kzhrknt/awesome-design-md-jp
- bergside/awesome-design-skills
- shaom/brand-to-design-md-skill
- hasi98/designpull

Findings applied:

- DESIGN.md should be a durable contract, not a vague moodboard.
- The file must describe product goal, users, surfaces, states, components,
  visual language, accessibility, and non-goals.
- The design contract must be specific enough for Google Stitch or an AI design
  agent to generate consistent screens without inventing a new product shape.
- Design-to-code artifacts must preserve constraints: no secret values, no
  copied brands, no hidden fake readiness, no implied dashboard-first pivot.
- The design file must encode reusable components and states, because those are
  easier to audit than a one-off visual description.

## Anti-Patterns Rejected

- plastic AI dashboard;
- threat-map theater;
- purple-blue AI gradient surface;
- green status labels for incomplete validation;
- generic chatbot layout;
- polished screenshot that hides missing real SIFT validation;
- single large card pretending to be an investigation interface.

## Concrete Design Implications

- `DESIGN.md` must keep forensic clarity as the first rule.
- Report surfaces must privilege evidence IDs, source references, parser status,
  correction outcomes, and limitations.
- Architecture diagrams must show input-only evidence and generated output
  boundaries.
- README and generated outputs should share the same status language.
- Visual identity should be sober: paper, ink, boundary lines, restrained status
  colors, and compact typography.

## Source Links

- https://github.com/google-labs-code/design.md
- https://github.com/VoltAgent/awesome-design-md
- https://github.com/kzhrknt/awesome-design-md-jp
- https://github.com/bergside/awesome-design-skills
- https://github.com/shaom/brand-to-design-md-skill
- https://github.com/hasi98/designpull
- https://github.com/aboul3ata/lazyweb-skill
