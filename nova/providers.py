"""Small, fail-closed model clients. No provider connection is made at import time."""

from __future__ import annotations

import json
import os
import re
import ssl
import urllib.error
import urllib.request


class ProviderError(RuntimeError):
    """A provider is unavailable or returned an invalid response."""


class PrivacyError(ProviderError):
    """The selected route is forbidden by NOVA's data policy."""


MODES = frozenset({
    "NORMAL", "LOCAL_ONLY", "OFFLINE", "PRIVATE", "READ_ONLY", "DRY_RUN", "SAFE_MODE",
})
CLASSIFICATIONS = frozenset({
    "PUBLIC", "INTERNAL", "PERSONAL", "PRIVATE", "SECRET", "CREDENTIAL", "SYSTEM_SENSITIVE",
    "SECURITY_SENSITIVE", "THIRD_PARTY_PRIVATE",
})
BLOCKED_CLASSIFICATIONS = CLASSIFICATIONS - {"PUBLIC", "INTERNAL", "PERSONAL", "PRIVATE"}
MAX_INPUT_BYTES = 64 * 1024
MAX_RESPONSE_BYTES = 256 * 1024
MAX_OUTPUT_BYTES = 64 * 1024
TIMEOUT_SECONDS = 25

# A conservative additional guard, not a replacement for explicit classification.
_CREDENTIAL_PATTERNS = (
    re.compile(r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----", re.I),
    re.compile(r"\b(?:gsk_|sk-(?:proj-)?|gh[pousr]_|github_pat_)[A-Za-z0-9_-]{12,}"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{12,}", re.I),
    re.compile(
        r"\b(?:api[_ -]?key|access[_ -]?token|refresh[_ -]?token|auth[_ -]?token|"
        r"password|passwd|secret|token|client[_ -]?secret|private[_ -]?key)"
        r"[\"']?\s*(?:[:=]|\bis\b)\s*[\"']?[^\s\"',;}{]{3,}", re.I,
    ),
    re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s/:@]+:[^\s/@]+@", re.I),
)


def contains_credentials(text: str) -> bool:
    """Detect common credential formats without returning or logging the value."""
    return any(pattern.search(text) is not None for pattern in _CREDENTIAL_PATTERNS)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class ModelProvider:
    """Call fixed Ollama/Groq endpoints after checking mode and data classification.

    Local loopback inference is permitted in OFFLINE mode. Cloud inference requires
    NORMAL mode and PUBLIC/INTERNAL data. Credential detection is a heuristic; users
    must classify data accurately even when no known credential format is detected.
    """

    def __init__(
        self, provider: str = "ollama", model: str = "llama3.2", api_key: str | None = None,
    ):
        if provider not in {"ollama", "groq"}:
            raise ProviderError("Choose the ollama or groq provider.")
        if not isinstance(model, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:/-]{0,127}", model):
            raise ProviderError("The model name is invalid.")
        if contains_credentials(model):
            raise PrivacyError("Credential-like data cannot be used as a model name.")
        self.provider = provider
        self.model = model
        self._api_key = api_key if api_key is not None else os.environ.get("GROQ_API_KEY", "")
        if not isinstance(self._api_key, str) or any(char in self._api_key for char in "\r\n"):
            raise ProviderError("The provider credential configuration is invalid.")

    def status(self) -> dict:
        """Report configuration only; connectivity is deliberately not inferred."""
        return {
            "provider": self.provider,
            "model": self.model,
            "configured": self.provider == "ollama" or bool(self._api_key),
            "connection": "not_checked",
        }

    def complete(
        self, messages: list[dict], mode: str = "LOCAL_ONLY", classification: str = "PERSONAL",
    ) -> str:
        if not isinstance(mode, str) or mode not in MODES:
            raise PrivacyError("Unknown operating mode; model access was blocked.")
        if not isinstance(classification, str) or classification not in CLASSIFICATIONS:
            raise PrivacyError("Unknown data classification; model access was blocked.")
        if classification in BLOCKED_CLASSIFICATIONS:
            raise PrivacyError("This data classification cannot be sent to a model.")
        if self.provider == "groq" and (mode != "NORMAL" or classification not in {"PUBLIC", "INTERNAL"}):
            raise PrivacyError("Cloud inference requires NORMAL mode and PUBLIC or INTERNAL data.")
        if not isinstance(messages, list) or not 1 <= len(messages) <= 128:
            raise ProviderError("Provide between 1 and 128 text messages.")
        clean_messages = []
        size = 0
        for message in messages:
            if not isinstance(message, dict) or set(message) != {"role", "content"}:
                raise ProviderError("Each message must contain only role and content.")
            role, content = message["role"], message["content"]
            if not isinstance(role, str) or role not in {"system", "user", "assistant"} or not isinstance(content, str):
                raise ProviderError("Messages require a supported role and plain text content.")
            try:
                size += len(content.encode("utf-8"))
            except UnicodeError:
                raise ProviderError("Message text is not valid Unicode.") from None
            if size > MAX_INPUT_BYTES:
                raise ProviderError("The conversation exceeds the model input limit.")
            if contains_credentials(content):
                raise PrivacyError("Credential-like data cannot be sent to a model.")
            clean_messages.append({"role": role, "content": content})

        payload = {"model": self.model, "messages": clean_messages, "stream": False}
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.provider == "ollama":
            url = "http://127.0.0.1:11434/api/chat"
            payload["options"] = {"num_predict": 2048}
        else:
            if not self._api_key:
                raise ProviderError("Set GROQ_API_KEY in secure environment settings to use Groq.")
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers["Authorization"] = "Bearer " + self._api_key
            payload["max_tokens"] = 2048
        request = urllib.request.Request(
            url, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers=headers, method="POST",
        )
        # Suppress proxies for loopback. HTTPS cloud requests honor the host proxy
        # configuration but retain certificate/hostname checks and forbid redirects.
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}) if self.provider == "ollama" else urllib.request.ProxyHandler(),
            _NoRedirect(),
            urllib.request.HTTPSHandler(context=ssl.create_default_context()),
        )
        try:
            with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
                if response.geturl() != url or not 200 <= response.status < 300:
                    raise ProviderError("The provider returned an unexpected HTTP response.")
                body = response.read(MAX_RESPONSE_BYTES + 1)
                if len(body) > MAX_RESPONSE_BYTES:
                    raise ProviderError("The provider response exceeds the size limit.")
            result = json.loads(body.decode("utf-8"))
            if self.provider == "ollama":
                answer = result["message"]["content"]
            else:
                answer = result["choices"][0]["message"]["content"]
            if not isinstance(answer, str) or not answer.strip():
                raise ProviderError("The provider returned no text response.")
            if len(answer.encode("utf-8")) > MAX_OUTPUT_BYTES:
                raise ProviderError("The model text exceeds the output limit.")
            if contains_credentials(answer):
                raise PrivacyError("The model response was withheld because it resembles credential data.")
            return answer
        except (urllib.error.URLError, OSError, TimeoutError):
            raise ProviderError("The model service could not be reached or refused the request.") from None
        except (ValueError, UnicodeError, KeyError, IndexError, TypeError, RecursionError):
            raise ProviderError("The model service returned an invalid response.") from None
