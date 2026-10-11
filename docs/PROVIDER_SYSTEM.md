# Provider system

Settings → AI offers OpenAI, Gemini, Ollama and Groq. Save a model and, on Windows, a key; then press Check connection. Cloud probes require NORMAL and send only a fixed short PUBLIC probe capped at32 output tokens. Chat additionally requires PUBLIC/INTERNAL. LOCAL_ONLY/PRIVATE/OFFLINE prevent cloud inference. Local commands route before provider construction.

Keys are protected with current-user Windows DPAPI and atomically stored under the local data folder. No plaintext fallback exists. The Hub never inherits environment keys. The password field clears on save; Python cannot guarantee zeroization of every temporary string. Linux/macOS cannot configure cloud keys through this vault. Forget removes ciphertext and resets health.

OpenAI/Gemini use fixed HTTPS destinations, verified TLS and no redirects. Each attempted request records sanitized status, latency and cumulative failure rate; health is a historical observation, not a permanent availability guarantee. No provider response body or key is persisted as diagnostic metadata.

The backend accepts one distinct fallback only with explicit approval and repeats privacy gates. No privacy failure triggers fallback. This does not retry tool actions. Automatic cost/quality routing, budgets, circuit breakers, image/voice interfaces and fallback selection UI remain outstanding. Live cloud requests and Windows DPAPI are unverified; tests use mocked HTTP/DPAPI.
