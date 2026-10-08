# NOVA project status

Version: **0.1.0 foundation**, implementing the first working slice of the NOVA v6.0 master specification. The full v6.0 vision is not complete.

## Working and verified

- New standalone Streamlit dashboard and Python core, without modifying the legacy application.
- Sinhala text, Sinhala/Singlish reflex examples, and explicit local chat commands.
- SQLite memory with provenance, confidence, scope, and explicit-over-inferred conflict resolution.
- Mission persistence, three concurrent workers, dependencies, failure isolation, restart recovery, durable emergency stop, and request idempotency.
- File and system specialist registry; exact tool schemas and scoped tool access.
- Bounded workspace listing, UTF-8 read/create, OS information, post-write hashes, and safe rollback retaining files in trash.
- Durable event journal and trusted observer notifications with observer-failure isolation.
- Privacy/read-only/dry-run checks and credential rejection in storage, model boundaries, and chat display.
- Prepared local command plans and validated, reviewed model-plan submission.
- Provider adapters for fixed local Ollama and Groq endpoints. Routing and error handling verified with **mocked HTTP**, not live inference.
- Python bootstrap installs dependencies and starts the real server on Linux; HTTP health/root responses checked. Streamlit AppTest executes real-core workflows.

## Partial or unverified

- Model-based conversation/planning: adapters implemented, needs an installed local model or owner-supplied cloud key for live validation.
- Sinhala support: Unicode and built-in phrases verified; broad language quality and speech are unverified.
- Windows launcher and lock implementation: included, need real Windows execution testing.
- Local data is ordinary SQLite/files, not an encrypted vault. No automatic backup/restore or secure erasure.
- No auto-retry of uncertain writes. A crash during creation intentionally produces a BLOCKED mission for inspection.

## Tests and acceptance traceability

Run `python -m unittest discover -s tests -v`.

Latest validation: **36 tests passed, zero failures or skips**, on Python 3.12/Linux using the launcher's isolated environment. Dependency consistency and the real launched server's health/root endpoints also passed. No live AI-provider inference or Windows execution was included.

| Master acceptance requirement | Evidence / status |
| --- | --- |
| A: concurrent independent jobs | Core test uses a finite worker barrier |
| B: one failure does not stop others | Core independent/dependent failure tests |
| C: recovery after restart | Persisted state tests; interrupted reads requeued, writes blocked |
| D: secret boundary | Provider and database credential-rejection tests |
| G: prompt injection | Unknown tool/traversal plan rejection tests; no web ingestion exists |
| H: emergency stop | Core durable stop/resume plus dashboard tests |
| K/L: accurate memory and precedence | SQLite memory persistence/conflict tests |
| M: file deletion protection | No permanent deletion tool; undo preserves changed files |
| O: offline local work | Core offline file workflow test |
| E/F/N: email, purchases, duplicate sends | Not implemented; mission idempotency is not proof of send idempotency |
| I/J/P: self-update, security targets, education | Not implemented |

## Next milestones, in order

1. Connect an owner-approved model; evaluate real Sinhala conversation and reviewed planning. Add selective local memory retrieval and bounded tool-result reasoning.
2. Validate Windows launch/locking, package a desktop installer, and add an OS-backed credential vault and verified backup/restore.
3. Add approved-folder permissions, more reversible file operations, and tightly scoped Windows app launching with process verification.
4. Implement push-to-talk Sinhala speech, device selection, interruption and emergency-stop testing on actual audio hardware.
5. Add browser/research, Office exports, project namespaces, and long-running scheduled missions, each with live verification and permission tests.
6. Expand to email/calendar, study, creative tools, games and smart home through the staged roadmap in the master specification.

## Checkpoint

All implementation is in new repository files. The owner authorized publishing this release on the separate `nova-agent-v0.1` branch, with a standalone archive at `downloads/Nova-agent-v0.1.zip`. This is a source release, not a production deployment or a merge into `main`. Existing `app.py`, `requirements.txt`, and devcontainer configuration are unchanged. Use `Start Nova.bat`, `start-nova.sh`, or `nova_app.py` for the new agent.
