# NOVA 0.3 privacy model

LOCAL_ONLY remains the default for model traffic. Groq requires explicit NORMAL mode and PUBLIC/INTERNAL classification; private/protected requests cannot use that cloud route. Ollama is restricted to the local endpoint. TLS, redirect and response-size checks remain in place.

Ordinary chat sends only the current request, fixed instructions and installed tool names. Saved memories, decision records, files and mission history are not automatically transmitted. `/decisions` and `/capabilities` are local lookups and do not call a provider. The owner must enter any key into the masked provider field or a secure process environment. Session-entered keys are not written to SQLite. The current app does not provide an encrypted credential vault; the old legacy source is excluded from downloadable packages.

Memories, decisions, missions and settings are local unencrypted SQLite data. Decision search is bounded and Unicode-aware; records contain only owner-entered project labels/reasons and timestamps. A project label grants no filesystem access. Forgetting is logical deletion, not secure erasure of database pages or backups. Decision/model metadata events omit prompts, reasons, file contents and keys.

Windows discovery reads local application registrations, shortcut targets and visible-window process identities. The launch receipt omits window titles and executable paths. A fixed discovery script contains no owner input. NOVA does not upload screen contents or perform background OCR, microphone capture, camera recording or device discovery. Provider configuration is not a connectivity result.

Opening an installed app can trigger that app's own network behavior, restored tabs or account session; NOVA does not monitor or constrain another application's traffic. Official website handoff requires NORMAL mode and may use the browser's existing cookies/session. It sends no NOVA memory or decision contents. Browser page loading is explicitly unverified.

The GUI bootstrap keeps a local startup log; no credentials are passed as command arguments. Inspect logs before sharing because paths/runtime diagnostics may be present. There is no system-wide egress monitor. Voice, vision, device mesh and auto-reply remain disabled/unimplemented. The v10 capture exclusions NO_CAPTURE/NO_OCR/LOCAL_VISION_ONLY/NO_CLOUD are future required controls, not active protection for a nonexistent capture pipeline.
