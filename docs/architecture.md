# Architecture and decision record

## ADR 001: modular Python core with a local Streamlit dashboard

The master prompt recommends a modular monolith first. This repository already has Streamlit, so the first usable release keeps that UI technology and adds a separate, testable standard-library core. This avoids requiring a frontend build toolchain or many services before the agent can do useful work. A native desktop shell and OS integrations can be added later.

```text
nova_app.py (owner input, settings, review)
    → NovaCore (director, mode/privacy checks, commands, planning)
    → SQLite Store (missions, memory, event journal, persistent stop)
    → bounded scheduler (three workers; dependency checkpoints)
    → AgentRegistry (file-agent or system-agent tool scope)
    → ToolRegistry (validated arguments and dedicated workspace)
    → actual result verification → persisted receipt

Chat/planning → ModelProvider → privacy gate → fixed Ollama/Groq endpoint
Model text → no direct execution
Prepared plan → schema validation → owner review → mission submission
```

The two specialist workers are scoped Python agents, not a simulated fleet of independent LLMs. The director/planner/verifier responsibilities are core functions. No role is advertised as an installed voice, browser, game, or email agent.

## Modules

| Module | Responsibility |
| --- | --- |
| `config.py` | Platform-aware data directory, resource limits |
| `storage.py` | SQLite transactions, event journal, isolated observer notifications |
| `agents.py` | Agent protocol and per-specialist tool allowlists |
| `tools.py` | Tool definitions, path checks, bounded file I/O, content hashes |
| `core.py` | Reflex routing, persistent memory, planning, mission lifecycle, recovery, rollback |
| `providers.py` | Provider interface, privacy classification, bounded HTTP, safe errors |
| `nova_app.py` | Dashboard, owner settings, plan review, explicit memory controls |

SQLite uses WAL and serialized short transactions. Each mission records a UUID trace ID, goal, tool, validated inputs, optional dependency, state, timestamps, result/error, and optional idempotency key. Events include lifecycle and tool/agent metadata, not raw prompts or file contents. Event observers are trusted internal code; exceptions cannot invalidate an already-persisted event. This is an in-process event bus, not a distributed message broker.

## ADR 002: bounded, verifiable tools before desktop automation

Only `files.list`, `files.read`, `files.create`, and `system.info` can execute. Creation is exclusive, with a post-write SHA-256 check. Files are limited to a dedicated workspace and reads are bounded to 1 MB. Hidden/absolute/parent paths, stable symlinks, and hardlinked reads are rejected. Listing is bounded to 500 files/directories. The worker verifies the tool's receipt before marking a mission complete. No shell, arbitrary URL tool, external sends, account actions, payments, or deletion API exists.

## ADR 003: conservative recovery and explicit idempotency

One cross-process lock protects each data folder. A mission is claimed transactionally before dispatch. Duplicate request IDs reuse the same mission only when the tool and inputs match. Automatic crash recovery requeues reads and marks interrupted writes BLOCKED because an external side effect may have happened before the database receipt committed. This is at-most-once retry policy for writes, not an exactly-once guarantee.

Stop persists in SQLite and prevents new work. An already-running atomic tool call can finish. Explicit resume queues paused work. Independent missions may run concurrently; each prepared plan is a sequence. Failure blocks dependents while unrelated missions continue.

## ADR 004: no implicit model access to local memory

The current chat sends only the latest input and fixed instructions to the selected provider. Conversation history is displayed in browser session state but is not yet included in inference. Memory is explicitly managed and retrieved through local commands, not automatically supplied to cloud models. This limits accidental disclosure at the cost of richer conversational context. Selective, provenance-aware context retrieval is a later milestone.

## Known constraints

- UTF-8 text only; no PDFs, Office exports, image understanding, browser, microphone or PC control.
- No recurring scheduler, resource monitor, budgets, vector memory, knowledge graph, encrypted vault, or complete privacy-policy language.
- Generated plans have at most eight steps. They cannot substitute the output of one tool into another or run an iterative agent reasoning loop yet.
- Sidebar provider settings persist only for the browser session. Data/missions/preferences persist on disk.
- Live provider latency, Sinhala model quality, Windows batch execution and native Windows locking require testing on the target machine.
