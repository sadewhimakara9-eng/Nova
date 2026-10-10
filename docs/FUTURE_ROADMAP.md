# NOVA additive roadmap

The [v10 master specification](NOVA_MASTER_SPEC.md) is canonical. The preserved [v8 specification](spec/NOVA_V8_MASTER_SPEC.md) and [Advanced Expansion Pack](spec/NOVA_ADVANCED_EXPANSION.md) remain requirements wherever v10 does not supersede them. Working code is preserved. Real Windows validation, live-model evaluation, vision and speech remain outstanding.

## Current milestone: 0.3

This release adds a searchable feature/status catalog, explicit project decision memory, a local command grammar and an experimental Windows app resolver/launcher. The UI now exposes five primary destinations while retaining internal pages under Settings/Advanced. All 132 expansion sections are registered in `nova/feature_catalog.json`; all 136 v10 sections are registered in `nova/v10_requirements.json`. Generated matrices describe each scope, source, implementation, tests and release. Governance records are not extra working runtime features.

The v10 order supersedes the older broad release-family order below: P0 stabilize → P1 local command routing → P2 general app discovery → P3 secure provider setup → P4 one real provider → P5 authorized vision → P6 real voice → P7 simple UI → P8 durable workers → P9 project continuation → P10 browser → P11 Office → P12 authenticated mesh → P13 second-node validation → later media/communications/Skill Factory/game/3D/education. This release supplies a bounded P1/P2 slice with mocked Windows coverage, not P1–P6 completion. No advanced game/media module is presented as implemented.

Vision is a core required subsystem. It still needs a real provider, capture permissions, private-window exclusions/redaction and image-based acceptance tests. The device mesh still needs node identity, pairing, mutually authenticated encrypted transport, per-device grants, revocation and a controlled second machine. Neither is enabled by a roadmap entry. Live provider acceptance is blocked by the absence of a running owner-selected local model or authorized cloud credentials; keys must be entered securely, never in chat.

- Tools → Feature coverage searches installed tools, agents, provider adapters and future features, with status/type filters. Current mode and emergency stop affect displayed tool availability. Search makes no network calls and never installs or grants permissions.
- Projects → Decision memory records the owner's project label, decision, reason, alternatives and UTC dates. Search, revision-checked edits and confirmed logical deletion work locally. `/decisions <keywords>` retrieves recorded reasons without asking a model. Project labels do not create managed projects or link arbitrary folders.
- `/capabilities <keywords>` reports catalog evidence, including missing features. The executable registry remains derived from actual tool/agent registrations. Roadmap metadata can never authorize a tool.
- Auto-reply remains **OFF**. No send transport exists. All six proposed modes remain planned, including DRAFT_ONLY; no mode is presented as active.

## Shared infrastructure and next dependency order

| Foundation | Existing support | Next complete slice | Enables |
| --- | --- | --- | --- |
| Traceability and truthful discovery | Four installed tools, catalog, evidence references, coverage UI | Runtime provider/dependency checks with timestamps and bounded failures | Capability search, health monitor, repair missions |
| Local project knowledge | Scoped memories and explicit decision records | Project records with explicit folder boundaries and reviewed snapshots | Workspace memory, time machine, contextual help |
| Permissions and audit | Fixed tool/agent scopes, mode gates, metadata events | Per-resource grants with expiry and approval receipts | PC tools, communications, recordings, devices |
| Recovery and secrets | WAL transactions, interrupted-write blocking, durable stop | Verified backup/restore and OS-backed credential storage | Updater, disaster recovery, account connections |
| Workflow execution | Bounded sequential plans, concurrent independent missions | Typed tool-result references and reusable reviewed action templates | Voice macros, learned workflows, scenes |
| External adapters | Ollama/Groq implementations; live connectivity unverified | One owner-selected provider and actual Windows native validation | Benchmarks, fallback, budget routing |
| Communication policy | No transport; auto-reply OFF | Draft-only inbox slice after authorized adapter and recipient identity are ready | Follow-up, priority contacts, optional auto-reply |

Communication enablement must first enforce contact allowlists, cooldown, duplicate prevention, per-conversation/hour/day limits, bot-loop checks, sensitive-content escalation, quiet hours, owner override and emergency disable. No automatic deletes or sends are implied by catalog registration. Remote access stays disabled until paired authentication, encrypted transport and audit are implemented. Workflow learning must observe only with permission, simulate, suggest and obtain owner authorization before enabling a new workflow.

## Broad roadmap from the expansion

Version families describe product direction, not a claim of current completeness. Useful foundations may land early; current runtime is 0.3.0, not NOVA v8 implemented.

| Family | Planned scope |
| --- | --- |
| 0.x | Core, white-glass UI, chat, project status, traceable foundations |
| 1.x | Missions, memory, permissions, bounded PC/file control, browser |
| 1.5 | Sinhala voice, wake word, interruption, workspace restore |
| 2.x | Office, documents, research, presentations and spreadsheets |
| 2.5 | Email, calendar, messaging, optional auto-reply |
| 3.x | Image, video and audio studio |
| 3.5 | Software factory, websites, reviewed deployment, debugging |
| 4.x | Expanded registry, Skill Factory, provider routing, controlled self-improvement |
| 4.5 | Education, personalized practice, target-paper evaluation |
| 5.x | Blender, 3D and architectural visualization |
| 5.5 | Game studio, scoped agent pipeline, game QA |
| 6.x | Authorized smart-home and camera integrations |
| 7.x | Phone companion and secure multi-device workers |
| 8.x | Workflow learning, project prediction, world model, stronger local AI |
| 9.x+ | Mature autonomous personal system within owner policy |

## Maintenance contract

Update the catalog scope and evidence when implementation changes. Run `python scripts/sync_roadmap.py`, then `python scripts/sync_roadmap.py --check` and the regression suite. WORKING needs real implementation plus tests within the stated scope. Missing external credentials/hardware are not evidence of success. New adapters must satisfy core privacy, schema, permission, idempotency and verification contracts before entering the executable tool registry. No source/catalog loading path executes arbitrary plugin code.

Preserve the complete [v8 requirement matrix](REQUIREMENTS_STATUS.md), including PC control, voice, Office, research, calling, purchases, media, education, games, home, vault, backups and security. No new expansion milestone removes those earlier requirements. Continue one tested vertical slice at a time.
