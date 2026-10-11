# NOVA development instructions

- Read `docs/NOVA_MASTER_SPEC.md` (Omega 12 is canonical), `docs/PROJECT_STATUS.md`, `docs/REQUIREMENT_MATRIX.md`, and `docs/ARCHITECTURE.md` before extending the agent. The v8, v6, glass UI and expansion requirements remain preserved reference material.
- Earlier prompts are historical references; Omega 12 supersedes their requirements. Preserve verified working code; maintain `docs/FUTURE_ROADMAP.md` and generate `docs/EXPANSION_TRACEABILITY.md` from `nova/feature_catalog.json` with `scripts/sync_roadmap.py`. Roadmap records never grant tool permissions.
- Decision records are owner-entered local data, not implicit model context. Preserve revision checks, mode gates and content-free audit metadata. Auto-reply remains OFF until its transport and policy protections actually exist.
- Keep only Chat, Voice, Projects, Memory and Settings in primary navigation. Preserve internal pages under Settings/Advanced. Windows launch tools are experimental until tested on Windows; never treat OS browser handoff as verified page loading. No owner input may enter the fixed discovery script or shell arguments.
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
- Keep glass UI state previews isolated from core actions. Every integration must show its actual connection state. Do not render raw diagnostic JSON outside the Advanced settings panel.
- Inspect the UI in a real browser after visual changes. Streamlit sanitizes inline SVG in `st.html`; use the escaped image-based components in `nova/ui/glass.py`.
- Run `python scripts/package_release.py` before distributing a release. It checks high-confidence secret formats and deliberately excludes legacy `app.py`, environment data, virtual environments and previous archives.
