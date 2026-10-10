# NOVA 0.3 security model

This is the implemented boundary, not the complete v10 security architecture.

- One local owner, loopback Streamlit, CORS/XSRF enabled, one scheduler lock per data directory. No authenticated multi-user or remote interface exists.
- Models return conversation text or schema-validated plans. Only registered tools with an authorized specialist may run. Catalog and roadmap records never install or grant capabilities. Plan validation precedes submission; NORMAL-only website plans are rejected atomically in other modes.
- Workspace tools reject absolute/parent/hidden paths and stable symlinks; reads reject hardlinks and nonregular files. File creation never overwrites existing data and verifies the resulting hash. Unchanged generated files can move to local trash.
- Windows launch is experimental. It resolves locally registered App Paths, argument-free Start Menu shortcuts, packaged application identities and visible executables. Arbitrary app names are matched against discovered candidates; ambiguous matches are refused. No owner-supplied path, URL, shell command or executable arguments are accepted. A fixed, noninteractive PowerShell discovery script reads shortcut/app metadata. Discovery never executes a shortcut. Common shell/script-host targets and remote UNC paths are excluded. This is not a signed-software inventory or a sandbox for the app being launched; installed applications are trusted at the owner's OS-account level.
- Native app success requires a visible window matching executable path or application identity. Already-visible apps are reported without claiming they were focused. Browser handoff is limited to configured official Gemini/YouTube destinations, requires NORMAL mode, and remains BLOCKED because page loading was not verified. No automatic retry or duplicate browser dispatch follows that result.
- Durable emergency stop pauses new work; an atomic operation already in progress may finish. Restart requeues safe reads but blocks uncertain writes/launches for inspection. Per-request idempotency exists for local missions, not a universal external exactly-once guarantee.
- Decision edits/deletes require the current revision and permitted mode. Audit records omit decision content. Schema migration is additive.
- The Windows GUI entry redirects bootstrap output to local logs and sets hidden child flags. Actual Windows no-terminal/native-window behavior still requires target-machine testing. The diagnostic batch launcher intentionally retains its console.

Not implemented: encrypted vault, per-resource temporary grants, OS sandbox, signed auto-updater, automatic backups, general browser automation, external-send policy engine, remote node agent or device pairing. No network listener for device control is introduced. Vision, audio capture and device mesh remain unavailable; their future adapters must enforce explicit capture/pairing grants, redaction, revocation and verifiable receipts before becoming executable.

Tests use temporary local state and mocked Windows/model APIs. They do not establish Windows readiness or a successful external connection.
