# NOVA development instructions

- Read `docs/PROJECT_STATUS.md`, `docs/architecture.md`, and relevant sections of `docs/spec/NOVA_MASTER_PROMPT.md` before extending the agent.
- Use the existing isolated checkout. Do not create a Git worktree unless the user explicitly asks for one.
- The new entry point is `nova_app.py`; `app.py` is a legacy application. Never print or reuse embedded credentials from legacy source. Do not modify legacy source as an incidental cleanup.
- Implement working vertical slices and maintain truthful feature status. Do not portray mocked integrations, configured providers, or untested Windows behavior as verified.
- Core code belongs in `nova/`; tests in `tests/`; user launch scripts at the root and `scripts/`. Prefer the standard library and existing Streamlit dependency.
- Keep memory, missions, provider credentials, and logs out of source control. Use temporary `NOVA_DATA_DIR` values for tests. No secret values in docs, fixtures, or logs.
- All model-generated plans pass the fixed tool schema and mode gates. Models cannot execute Python, shell commands, or change owner policy. Add explicit permissions and actual verification before adding side effects.
- Preserve local-only defaults, fixed model destinations, verified TLS, redirect protection, emergency stop, no-overwrite file behavior, and safe interrupted-write recovery.
- Test new capabilities using `python -m unittest discover -s tests -v`. Include regression tests for policy or persistence changes. Use mocked external services for deterministic tests and label them as mocked.
- The Windows launcher and Windows locking path need real Windows validation before claiming Windows readiness. The current runtime is a single-user local dashboard; do not expose it to a network.
- Update `docs/PROJECT_STATUS.md` after each meaningful implementation milestone. Do not commit or push user work unless requested.
