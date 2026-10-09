# NOVA project status

Runtime version: **0.2.0 — NOVA Glass**. Primary product specification: **NOVA v8.0** in [NOVA_MASTER_SPEC.md](NOVA_MASTER_SPEC.md). This is a verified vertical slice, not the completed v8 operating system.

## Latest completed work

- Preserved the existing core, memory, tool restrictions, mission engine and all previous tests.
- Built a reusable pearl-white glass theme, original blue/cyan orb, thin outline navigation, translucent composer/cards/dialogs, focus styles, reduced-motion handling and performance mode.
- Added all 13 navigation destinations: Home, Chat, Voice, Missions, Projects, Agents, Memory, Automations, Tools, Integrations, Devices, Privacy and Settings.
- Connected real chat, memory CRUD, plan review/approval, workspace text import, live mission filters, actual agent scopes/reliability, file undo, privacy mode and emergency stop/resume.
- Added isolated voice-state previews with explicit simulated labels. Microphone and missing integrations remain disabled/disconnected.
- Persisted appearance settings locally: glass, transparency, blur, animation, orb effects, scale and performance.
- Added a native Windows pywebview launch path with standard OS window controls, managed loopback child lifecycle and explicit browser fallback.
- Added a capability registry derived from installed tools/authorized agents. Model planning receives real schemas and verification metadata; essential gaps produce a safe report without submitting partial work.
- Saved the v8 primary specification and [requirement/status matrix](REQUIREMENTS_STATUS.md). The earlier v6 and dedicated glass UI prompts remain references.

## Validation

- **60 automated tests passed** on Python 3.12/Linux: core functionality, privacy, filesystem boundaries, recovery, failure isolation, concurrency, provider contracts, capability planning, UI service and dashboard workflow, and launcher lifecycle.
- Model responses and Windows-native APIs are mocked in their unit tests. Live AI inference, natural Sinhala speech and actual Windows window behavior were not verified.
- The real Streamlit application was launched and inspected in Chromium. The original orb was checked visually after fixing SVG sanitization and actual Streamlit 1.65 navigation selectors.
- Browser resize checks cover **1366×768, 1920×1080, 2560×1440 and 760×700**, including visible composer and no horizontal page overflow. Navigation, chat, voice preview, privacy toggles and emergency controls are checked separately in the browser.
- Actual server health and owned-process shutdown/relaunch have integration coverage on Linux. Existing unrelated services are not terminated.
- A real Chromium session saved memory, closed the owned app, relaunched immediately on the same port, and recalled that memory successfully. The launcher now handles POSIX TIME_WAIT sockets while rejecting occupied listeners.

## Important limits

- A local model or owner-supplied cloud key is still needed for general AI conversation and planning. Provider availability is not inferred from its configuration.
- Voice capture, STT/TTS, wake word, Windows PC automation, browser/research tools, Office exports, named project management, messaging, purchases, creative tools and smart-home control are not implemented.
- Local SQLite is not an encrypted vault; forgetting is logical deletion. Full backups, secure erase, per-app privacy zones and system-wide network monitoring remain future work.
- The current capability-gap engine reports gaps; it does not install plugins or rewrite the core. Model generalization and composition have fixture-based tests, not live-model evaluation.
- The optional desktop shell is implemented but must be tested on Windows with WebView2 before native Windows readiness is claimed.
- Native app and browser share the same UI. In browser mode close Nova with Ctrl+C in its console; closing only a browser tab does not stop the local server.

## Next useful milestones

1. Test the native wrapper and one real owner-selected model on Windows, including Sinhala paraphrase evaluation and provider failure recovery.
2. Add a first-launch wizard, OS-backed credential vault and verified backup/restore.
3. Add project records/context, explicit capability permissions and bounded tool-result reasoning, without turning examples into exact-phrase limits.
4. Add carefully scoped Windows app control with observable verification, followed by Sinhala voice on actual audio hardware.
5. Continue the staged v8 roadmap for browser/Office/communication/media features with real acceptance tests.

## Release checkpoint

The update is prepared on the previously authorized `nova-agent-v0.1` GitHub branch. `scripts/package_release.py` builds the new standalone `downloads/Nova-agent-v0.2.zip`; the v0.1 artifact remains available separately. The standalone package excludes legacy `app.py`, credentials and runtime data. The legacy app and `main` are not changed by this release. This is a source release, not a production deployment or the complete NOVA v8 product.
