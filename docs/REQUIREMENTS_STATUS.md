# Preserved NOVA v8 requirement/status matrix

Historical source: [v8 specification](spec/NOVA_V8_MASTER_SPEC.md). This matrix records the **0.2.0** milestone. The current canonical specification is v10; see [current requirement matrix](REQUIREMENT_MATRIX.md) and [project status](PROJECT_STATUS.md) for 0.3 changes. Earlier requirements remain active unless explicitly superseded by v10.

**WORKING** means implemented and verified within the stated scope. **PARTIAL** names precisely what exists and what does not. **NOT_STARTED** means no executable feature is offered. **GUIDANCE** is an engineering constraint rather than a separate runtime feature. Model HTTP fixtures and Windows mocks never establish a live connection or real Windows readiness.

| v8 sections | Requirement | Status and scope | Evidence |
| --- | --- | --- | --- |
| 0–2, 7, 20–21, 227–228, 281–292 | Product direction, owner control, staged delivery | GUIDANCE: existing modular core preserved; this release follows priority 262 | Architecture ADRs; unchanged legacy app |
| 3–6, 15–19 | Generalized intent, capability composition/gaps | PARTIAL: installed registry feeds the model planner; bounded validated sequential plans; missing essential capabilities block submission. No automatic skill building, deep plan comparison or uncertainty engine | `test_capabilities.py`; model responses are mocked |
| 6 | Executable capability metadata | WORKING for the four installed tools; permissions, input schemas, verification, actual specialist scope, unmeasured fields explicitly marked | Registry tests; Tools UI |
| 8 | Personality settings | NOT_STARTED; no pretend active presets | Settings notice |
| 9 | Sinhala-first intelligence | PARTIAL: Unicode, built-in conversational examples and model language preference; live-model generalization quality not evaluated | Core tests; real-browser Sinhala display |
| 10–13 | Speech, pronunciation, correction, night voice | NOT_STARTED for audio; UI preview is simulated and isolated | Voice screen and UI tests |
| 14 | Cognitive stack | PARTIAL: director, planner, scoped workers and result verifier; no independent fleet of reasoning models | Core, agents, tools |
| 22–26 | Providers, routing, fallback, integration hub | PARTIAL: Ollama/Groq adapters, fixed destinations, privacy routing; no OpenAI/Gemini adapters or automatic fallback yet | Provider mocked-HTTP tests |
| 27–29 | Secrets, vault, release scanning | PARTIAL: credential rejection, masked provider field, high-confidence release scanner. No encrypted vault; legacy source still requires provider-side key rotation | Privacy/provider tests; packaging guard |
| 30–33 | Privacy classification, routing, protected zones | PARTIAL: modes/classifications and workspace restrictions; no per-app zones or system-wide egress monitor | Core/provider tests; Privacy UI |
| 34–44 | Memory and world model | PARTIAL: explicit SQLite memories, provenance, scopes, precedence and deletion. No vector graph, TTL, application snapshots or context restoration | Memory persistence/conflict tests |
| 45–58 | Missions, dependencies, workers, budgets | PARTIAL: persistent missions, sequential dependencies, independent concurrent jobs, failure isolation and scoped agents. No long-term goal scheduler, budgets or overnight reports | Core concurrency/recovery tests |
| 59–64 | Windows PC control | NOT_STARTED. The native UI shell grants no PC-control capabilities | Disabled future specialists |
| 65–69 | File intelligence/artifacts | PARTIAL: bounded list/read/create, hashes, no overwrite, reversible creation. No semantic file search or full lineage registry | Filesystem and rollback tests |
| 70–90 | Office, browser, research, communications, calendar, purchases | NOT_STARTED | Disconnected integration cards; no sends or payments |
| 91–122 | Media, coding factory, self-improvement, games, 3D, home/cameras | NOT_STARTED | No executable plugins or generated-code runner |
| 123–132 | Authorized security and education | NOT_STARTED | No security-target or exam-generation tool |
| 133–145 | Automations, workflow learning, simulations, trust/policy | PARTIAL: read-only/dry-run gates and measured recent tool results; no rule automation, learning or policy language | Mode tests; Automations disabled |
| 146–159 | Permissions, receipts, undo, capability truth | PARTIAL: tool/agent/workspace scopes, no permanent delete, verified receipts, safe undo and truthful capability status. External side effects are not implemented | Security tests and plan review |
| 160–168 | Recovery, backups, incidents | PARTIAL: read recovery, durable stop, blocked interrupted writes. No automated backup/restore, circuit breaker or incident engine | Restart and recovery tests |
| 169–188 | Observability, costs, project management, updates | PARTIAL: durable metadata events and mission trace IDs; no cost ledger, updater or named-project database | Event tests; local workspace view |
| 189–200 | White glass, orb, shell, Home/Chat/composer | WORKING: reusable local artwork/tokens, 10 visual states, all navigation, text composer and reviewed text import | Actual Chromium screenshots; UI tests |
| 201–202 | Voice UI and honest status | WORKING UI only: disconnected microphone plus labelled preview. No real STT/TTS | UI integration and browser workflow |
| 203 | Mission UI | WORKING for core states, filters, live polling, dependency/verification details. Priority/deadline fields absent from core are not invented | Real-core AppTest |
| 204 | Projects UI | PARTIAL: actual local workspace and recent artifacts/project notes; named projects/milestones coming soon | Navigation test |
| 205–206 | Agents and memory UI | WORKING for actual two specialists and existing memory scopes; other roles/collections are not falsely populated | Agent view-model and UI tests |
| 207–208 | Automations/integrations UI | WORKING presentation: disabled missing backends and unverified model connectivity shown accurately | Full navigation test |
| 209–210 | Privacy and approval UI | WORKING within core scope: local-only switch, limited cloud-response history, inspect/cancel/approve local mission modal | Browser toggles and AppTest approval |
| 211–214 | Settings, appearance, responsiveness/accessibility | WORKING controls for appearance/model setup, reduced motion and performance mode. Unsupported voice/personality/update settings are clearly identified | Preference tests; four browser sizes; Sinhala screenshots |
| 215–216 | Global overlay/system tray | NOT_STARTED | Explicit Settings notice |
| 217–218 | UI service/events | WORKING: core-backed view models; 3-second mission/status refresh; concise completion notices | Controller and event tests |
| 219 | Streaming chat | NOT_STARTED; waiting indicator for existing non-streaming providers | No simulated token stream |
| 220 | Functional/disabled controls | WORKING in the implemented views | UI/browser workflows |
| 221–222 | Setup and credentials | PARTIAL: one-command dependency setup and password field; no dedicated first-launch wizard or OS vault | Launcher and masked-key tests |
| 223–225 | Phone, multi-device and remote access | NOT_STARTED; app binds only loopback | Launcher flags/tests |
| 226, 229–235 | Engineering structure and validation | GUIDANCE: primary spec, this matrix, status, architecture and tests maintained | Repository files |
| 236–245, 257–258 | Core acceptance | PARTIAL: concurrent/failure/recovery/privacy/stop/memory/offline tests pass. No payments, external duplicate-send guarantee or live provider failure evaluation | Existing core/provider suites |
| 246–251, 255–256 | PC/Office/media/education/generalization acceptance | NOT PASSED for real integrations. Registry composition tested with model fixtures only | Honest capability limits |
| 252–254 | UI, resizing, Sinhala acceptance | WORKING in real Linux Chromium; native Windows still unverified | Browser evidence and screenshots |
| 259–260 | Installer and natural operations | PARTIAL: self-bootstrapping launcher, native webview path, local help/status/stop/resume. No compiled Setup.exe | Launcher tests including real Linux child lifecycle |
| 261–280 | Examples, current priority, phased roadmap | GUIDANCE: UI priority addressed in this release; later stages remain roadmap work | Project status and next milestones |

All capabilities not explicitly implemented above remain **NOT_STARTED**. A visible page or a configured provider is never proof of an active integration. Full v8 acceptance is not claimed.
