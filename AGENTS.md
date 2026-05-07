# Find Evil Project Agent Guide

Project: Evidence-Locked Self-Correcting Disk Triage MCP for the FIND EVIL!
hackathon.

Current stack:

- Python MCP server using official `mcp` package and FastMCP.
- Contract-first Pydantic schemas in `src/server.py`.
- Autonomous Anthropic + MCP stdio client in `src/agent.py`.
- Project memory under `docs/`.

Important commands:

```bash
python -m src.server
python -m src.agent --case-id CASE --evidence-path PATH --case-workspace cases/CASE
python -m src.agent --check-api
python scripts/check_env.py --strict
python scripts/sync_state.py
pytest tests/test_server_contracts.py
pytest tests/test_agent_contracts.py
py tests/mock_eval_fixture.py
```

Read first:

1. `docs/STATE.md`
2. `docs/EXEC_PLAN.md`
3. `docs/DECISIONS.md`
4. `docs/hackathon_strategy.md`
5. `docs/research_sift_mcp.md`
6. `docs/future_agent_project_instructions.md`

Active boundary:

- Do not implement DFIR subprocess calls in the MCP bootstrap step.
- Preserve the eight public tool names unless a decision is recorded.
- Keep the original evidence path read-only by architecture.
- Agent runs must keep `MAX_ITERATIONS`, global timeout, tool-call budget, and claim verification before final reporting.
- `docs/accuracy_report.md` is currently an initial synthetic benchmark report, not a real SIFT image accuracy claim.
- Public repository packaging lives in `README.md`, `LICENSE`, and `docs/architecture.md`.
- Current readiness status lives in `docs/submission_readiness_audit.md`; final submission is not ready until video, Devpost text, public repo, and real SIFT validation are complete.
- Secret handling policy lives in `docs/secret_handling_policy.md`; never print or copy credential values into logs, reports, docs, screenshots, or task text.
- Runtime language policy lives in `docs/runtime_adapter_language_audit.md`; Anthropic is the implemented runtime, while other configured provider keys are candidate adapter inputs only.
- Workspace discipline lives in `docs/no_revert_workspace_discipline.md`; do not revert, delete, or clean up user/evidence/case files without explicit approval and verification.
