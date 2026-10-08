# Security and privacy boundaries

This release is for one owner on a trusted local machine. It is not a hostile-code sandbox or a remotely authenticated control service.

## Enforced controls

- Localhost-only launch; Streamlit CORS and XSRF protection stay enabled.
- Only four registered tools, with exact argument fields and per-agent tool scope. Model-generated tool names or arguments cannot add capabilities.
- No external action is inferred from model prose. Plans are validated and reviewed before submission.
- Relative dedicated-workspace paths; no overwrites; no permanent deletion tool. Undo requires the recorded content hash to match and retains the artifact in local trash.
- LOCAL_ONLY, PRIVATE, OFFLINE, READ_ONLY, DRY_RUN, and SAFE_MODE disable cloud calls. Only NORMAL plus PUBLIC/INTERNAL permits Groq. READ_ONLY/SAFE_MODE deny workspace/memory mutation; DRY_RUN permits planning but no queued execution.
- SECRET, CREDENTIAL, SYSTEM_SENSITIVE, SECURITY_SENSITIVE, and THIRD_PARTY_PRIVATE are rejected for model calls. PERSONAL and PRIVATE may use local inference only.
- Credential pattern checks run independently of classification. Keys are never ordinary memory. The new app does not import the legacy app or its embedded credential.
- Model endpoints are fixed; redirects are disabled; Groq uses verified HTTPS and honors configured system proxies. Local Ollama bypasses proxies so loopback prompts stay local.
- Provider failures return sanitized messages. Events log safe metadata; mission and memory tables intentionally store owner-approved local content.
- Request/response limits, model timeout, three workers, and bounded file traversal prevent unbounded work in implemented paths.

## Limits and threat model

Credential detection cannot recognize every secret; owner classification remains necessary. PRIVATE memory is not encrypted at rest. An OS user or process with access to the data directory can read or alter it. Forgetting a memory is logical deletion, not guaranteed forensic erasure.

Path checks defend against submitted traversal and existing links. They do **not** establish an OS-level isolation boundary against a malicious same-user process racing parent-directory changes. Do not grant hostile processes write access to the workspace or run unknown plugins in-process. The event observer interface accepts trusted code only.

The UI's cloud setting authorizes the current request's transmission to the selected provider; it does not establish legal terms, retention, or provider availability. There is no platform-wide egress monitor. Nova does not claim all network activity on the PC is blocked by LOCAL_ONLY.

Emergency stop prevents new tool dispatch. It cannot retract completed writes or abort a blocking model HTTP call already sent; that call is limited by its timeout. Automation resumes only through the owner control. Interrupted writes require inspection rather than silent replay.

No secret vault, admin broker, sandboxed plugins, self-update pipeline, messaging, payments, or security scanning tools are installed. These must gain explicit permission models and tests before being made executable.

The legacy `app.py` contains an embedded credential. Rotate it with the provider; replacing that legacy integration is separate work. The new entry point does not use it.
