# Runtime And Adapter Language Audit

Date: 2026-05-06

Purpose: keep public runtime language truthful. The project must distinguish
implemented, smoke-tested, and candidate provider paths.

## Canonical Language

Use this wording:

- implemented runtime: Anthropic, OpenRouter, and Groq through `src/agent.py`;
- selected demo runtime: OpenRouter, verified with a short real-evidence agent
  run and selected by `--check-api` on 2026-05-07;
- alternate implemented runtime: Groq, currently passing API readiness;
- candidate provider: a configured external provider that is not used by the
  current autonomous agent until an adapter is built and tested;
- future adapter: a possible runtime path that is outside current release
  readiness;
- provider readiness check: a safe local check that reports configuration
  state without printing secrets.

Avoid this wording:

- "all providers are equally ready";
- a specific provider is used in the final demo unless the recorded run proves it;
- "any configured key can run the current agent";
- "provider fallback works" unless an actual fallback adapter and test exist.

## Audited Surfaces

| Surface | Required truth |
|---|---|
| `README.md` | Setup names OpenRouter as the preferred free/low-cost path and preserves Groq/Anthropic caveats. |
| `docs/STATE.md` | Current state keeps final submission blocked while noting OpenRouter smoke success. |
| `docs/freshness_dependency_register_2026-05-06.md` | Provider limits are treated as volatile and must be refreshed before final submission. |
| `docs/local_vs_sift_readiness_report.md` | Local checks are separated from real SIFT readiness. |
| `docs/submission_readiness_audit.md` | Submission remains blocked by real validation and public submission materials. |
| `src/agent.py` | `build_api_readiness_report()` selects the first ready implemented provider without printing secrets. |
| `scripts/check_env.py` | Environment check lists provider variables without exposing values. |

## Public Claim Boundary

The release can claim:

- the current implemented runtimes can be checked without printing secrets;
- OpenRouter has passed a short local smoke run;
- Groq adapter code exists and currently passes API readiness.

The release cannot claim:

- stable execution from a specific provider without a fresh recorded run;
- Gemini/OpenAI execution;
- model-provider independence;
- real SIFT validation from API readiness alone.
