# Runtime And Adapter Language Audit

Date: 2026-05-06

Purpose: keep public runtime language truthful. The project must distinguish
implemented, smoke-tested, and candidate provider paths.

## Canonical Language

Use this wording:

- implemented runtime: Anthropic, OpenRouter, and Groq through `src/agent.py`;
- smoke-tested runtime: OpenRouter, verified with a short real-evidence agent
  run on 2026-05-06;
- degraded implemented runtime: Groq, implemented but locally returning HTTP
  403 during live smoke testing;
- candidate provider: a configured external provider that is not used by the
  current autonomous agent until an adapter is built and tested;
- future adapter: a possible runtime path that is outside current release
  readiness;
- provider readiness check: a safe local check that reports configuration
  state without printing secrets.

Avoid this wording:

- "all providers are equally ready";
- "Groq is locally usable" until the HTTP 403 condition is resolved;
- "any configured key can run the current agent";
- "provider fallback works" unless an actual fallback adapter and test exist.

## Audited Surfaces

| Surface | Required truth |
|---|---|
| `README.md` | Setup names OpenRouter as the preferred free/low-cost path and preserves Groq/Anthropic caveats. |
| `docs/STATE.md` | Current state keeps final submission blocked while noting OpenRouter smoke success. |
| `docs/freshness_dependency_register_2026-05-06.md` | Provider limits and Groq HTTP 403 are treated as volatile. |
| `docs/local_vs_sift_readiness_report.md` | Local checks are separated from real SIFT readiness. |
| `docs/submission_readiness_audit.md` | Submission remains blocked by real validation and public submission materials. |
| `src/agent.py` | `build_api_readiness_report()` selects the first ready implemented provider without printing secrets. |
| `scripts/check_env.py` | Environment check lists provider variables without exposing values. |

## Public Claim Boundary

The release can claim:

- the current implemented runtimes can be checked without printing secrets;
- OpenRouter has passed a short local smoke run;
- Groq adapter code exists but local account/API status currently blocks live use.

The release cannot claim:

- stable Groq execution from the current local key;
- Gemini/OpenAI execution;
- model-provider independence;
- real SIFT validation from API readiness alone.
