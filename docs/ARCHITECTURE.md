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

Chat/planning → ModelProvider → privacy gate → ProviderHub health/vault → fixed Ollama/Groq/OpenAI/Gemini endpoint
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


## ADR 005: preserve the core; use a glass UI service layer and native webview shell

The v8 specification makes the unfinished UI the current priority. `nova/ui/controller.py` supplies validated display preferences, real mission/agent view models and a limited successful-cloud-response history. `glass.py`/`glass.css` provide reusable local artwork and appearance tokens. Inline SVG is sanitized by Streamlit, so original SVG artwork is encoded as local image data, with no external assets. Animations honor reduced-motion and performance settings.

The UI uses existing core methods for memory, missions, tools, stop/resume and plans. Voice preview uses session state only and is labelled simulated. Unimplemented integrations have disabled controls. Mission status is refreshed every three seconds; model replies are still non-streaming.

On Windows, `scripts/desktop.py` opens the same local app in a standard framed pywebview window. It exposes no Python/JavaScript bridge. It starts and stops only its own loopback server and falls back visibly to the browser when native components are unavailable. Native Windows behavior remains unverified on real hardware.

## ADR 006: installed capabilities, not example-phrase limits

`nova/capabilities.py` derives executable capability records from actual registered tools and authorized specialist scopes. The model planner receives input schema, permissions, verification methods and recent measured reliability. It may compose arbitrary supported tool steps for the owner's outcome. Unsupported essential capabilities produce a structured gap report with no mission submission. This is a working registry and bounded planning extension; automatic skill creation, sandboxed installation and live-model generalization evaluations are later milestones. Existing explicit slash commands are convenience shortcuts, not a claim of general language understanding.

## ADR 007: discovery metadata cannot authorize execution

`nova/catalog.py` combines the existing runtime registry with installed agent/provider descriptors and `feature_catalog.json`, which tracks all 132 additive requirements. Runtime tool availability reflects mode and stop state. Provider connections remain NOT_VERIFIED; no search triggers a network probe. Expansion records retain explicit implementation scope and REFERENCE_ONLY availability unless a corresponding local UI feature exists. The planner still receives only `core.capabilities()`, never roadmap features as executable tools. No plugin loader or arbitrary-code adapter installation is introduced.

Coverage counts exclude governance sections 129–132. `scripts/sync_roadmap.py` generates the Markdown traceability matrix from the same records and supports a drift check. Status describes implementation scope, not a claim of current external availability. Future adapter registration must still meet tool schemas and authorized specialist scope.

## ADR 008: explicit project decisions with optimistic revision checks

The existing SQLite database gains an additive `decisions` table. Existing missions, settings and memories are preserved. `nova/decisions.py` stores owner-supplied project labels, decision, reason, alternatives, timestamps and revision. Core write methods apply mode and emergency-stop gates; updates/deletes match the expected revision so stale requests cannot overwrite later edits. Audit events contain fixed labels/counts only. Search is Unicode-aware and returns at most 100 records; results are local and never automatically included in a provider request.

Project labels are not managed project IDs or inferred relationships. Edits preserve creation time but replace the current record; a full historical decision journal, semantic retrieval and named-project management remain future work. Logical deletion is not secure erasure of backups or SQLite pages.

## ADR 009: deterministic local intent before provider setup

The v10 canonical architecture prioritizes local Windows control. `local_commands.py` extracts arbitrary application names from English and Sinhala/Singlish launch grammar before any model selection or credential check. `windows_apps.py` discovers local App Paths, argument-free Start Menu shortcuts, packaged application identities and visible executables. It uses exact or clearly separated fuzzy matches and refuses ambiguity. The fixed PowerShell discovery script contains no interpolated owner input; launch uses argument arrays without a shell. A visible-window executable/AUMID match verifies native launch. Full PC control, focus/close, file/folder opening and unrestricted web navigation remain missing.

Windows builds add a scoped desktop worker and two experimental tools. Website handoff only targets configured official Gemini/YouTube destinations in NORMAL mode. Installed exact application identities are preferred; OS browser dispatch alone leaves a BLOCKED mission with an unverified receipt. It is never reported as a loaded website or retried automatically. Interrupted launches are treated as uncertain writes. Tests mock Windows APIs; a real target-device run is still required.

## ADR 010: five daily pages and optional GUI bootstrap

Chat, Voice, Projects, Memory and Settings are the only primary sidebar pages. All existing Home/Missions/Agents/Tools/Integrations/Devices/Automations/Privacy workspaces remain reachable through Settings → Advanced and the internal quick finder. Six validated accent choices affect small selection/action accents rather than recoloring the workspace. Greeting uses host local time.

`Start Nova.pyw` runs the existing bootstrap with hidden Windows child flags and local log redirection. Native window close still stops only its owned server. If GUI mode falls back to a browser, a visible session dialog owns shutdown; closing only the browser tab does not terminate the service. The diagnostic batch entry remains available. No tray service or global overlay is claimed. Full native/no-flash behavior is unverified on this Linux host.

## Omega provider and image boundaries

ProviderHub owns secure configuration, observed text requests and explicit probes. SecretVault uses Windows DPAPI with no unsupported-platform fallback. VisionGateway separately performs bounded local OCR on explicitly uploaded images; its output never becomes model context automatically. See PROVIDER_SYSTEM.md and VISION_SYSTEM.md for limits.
