# Provider Readiness Check

Purpose: provide a local provider-readiness surface without exposing secrets or
claiming unimplemented providers as production runtime support.

## Current Implemented Runtimes

The current implemented autonomous agent runtimes are Anthropic, OpenRouter,
and Groq through `src/agent.py`. `auto` currently prefers OpenRouter, then
Groq, then Anthropic when a matching key is configured and syntactically safe.

Readiness command:

```powershell
py -m src.agent --check-api
```

Expected safe behavior:

- prints provider names and environment variable names;
- reports whether each variable is configured;
- prints the selected model name;
- marks Anthropic, OpenRouter, and Groq as implemented runtimes;
- keeps unimplemented provider entries as candidate adapters only;
- does not print secret values.

## Environment And SIFT Readiness

Full real-run readiness requires both API readiness and SIFT forensic tool
readiness.

Command:

```powershell
py scripts\check_env.py --json
```

Expected safe behavior:

- reports missing or found SIFT commands;
- reports provider variables as configured or missing;
- includes `secrets_redacted: true`;
- blocks real SIFT readiness when required forensic tools are missing;
- does not promote unimplemented candidate providers to implemented runtime.

## Verified Local Status On 2026-05-07

- API readiness command completed without printing secret values.
- OpenRouter is the current selected free/low-cost runtime path.
- Groq is implemented and currently passes API readiness.
- SIFT readiness passes through WSL forensic commands.
- Real bounded CASE-RD01 validation exists; full long-run autonomous
  investigation is still not claimed.

## Release Language Rule

Public docs may say that Anthropic, OpenRouter, and Groq are implemented
provider paths. Public docs must not claim Gemini or OpenAI support until
adapters are implemented, tested, and documented.
