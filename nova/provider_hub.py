"""Owner-configured text providers and honest measured health, without secret metadata."""
from __future__ import annotations

from datetime import datetime, timezone
import json
import time

from nova.providers import ModelProvider, ProviderError, PrivacyError
from nova.vault import SecretVault, VaultError

DEFAULT_MODELS = {"openai": "gpt-4.1-mini", "gemini": "gemini-2.5-flash",
                  "ollama": "llama3.2", "groq": "llama-3.3-70b-versatile"}
STATES = frozenset({"DISCONNECTED", "CONNECTED", "DEGRADED", "AUTH_EXPIRED", "RATE_LIMITED"})


class _ObservedClient:
    """Text-only adapter whose outcomes update the hub's sanitized measurements."""
    def __init__(self, hub, adapter):
        self._hub = hub
        self._adapter = adapter
        self.provider = adapter.provider
        self.model = adapter.model

    def status(self):
        return self._adapter.status()

    def complete(self, messages, mode="LOCAL_ONLY", classification="PERSONAL", *, max_output_tokens=2048):
        started = time.monotonic()
        try:
            result = self._adapter.complete(messages, mode, classification,
                                            max_output_tokens=max_output_tokens)
        except PrivacyError:
            # Refused data/routes are not evidence of provider unavailability.
            raise
        except ProviderError as error:
            state = error.status if error.status in STATES else "DEGRADED"
            self._hub._save_health(self.provider, state,
                "Text request failed; review credentials, model or service availability.",
                round((time.monotonic() - started) * 1000), measured=True)
            raise
        self._hub._save_health(self.provider, "CONNECTED", "Text request succeeded at the recorded time.",
                              round((time.monotonic() - started) * 1000), measured=True)
        return result


class ProviderHub:
    def __init__(self, store, data_dir):
        self.store = store
        self.vault = SecretVault(data_dir)

    @property
    def vault_available(self):
        return self.vault.available

    def _name(self, provider):
        if not isinstance(provider, str) or provider not in DEFAULT_MODELS:
            raise ProviderError("Choose a supported provider.")
        return provider

    def _model(self, provider):
        self._name(provider)
        return self.store.setting("providers." + provider + ".model", DEFAULT_MODELS[provider])

    def providers(self):
        return [{"provider": name, "model": self._model(name), "local": name == "ollama",
                 "capabilities": ["text"], "cost_class": "local" if name == "ollama" else "metered",
                 "health": self.status(name)} for name in DEFAULT_MODELS]

    def configure(self, provider, model, key=None):
        self._name(provider)
        ModelProvider(provider, model, api_key="")  # Validate before any persistence.
        if key is not None:
            try:
                self.vault.put(provider, key)
            except VaultError:
                raise ProviderError("Secure credential storage is unavailable or could not save the key.") from None
        self.store.set_setting("providers." + provider + ".model", model)
        self._save_health(provider, "DISCONNECTED", "Configuration saved; connection not checked.", None)

    def client(self, provider):
        self._name(provider)
        key = ""
        if provider != "ollama":
            try:
                key = self.vault.get(provider) or ""
            except VaultError:
                self._save_health(provider, "DISCONNECTED", "Secure provider credentials are unavailable.", None)
                raise ProviderError("Unlock Windows secure storage to use this provider.", "DISCONNECTED") from None
            if not key:
                self._save_health(provider, "DISCONNECTED", "Secure provider credentials are unavailable.", None)
                raise ProviderError("Add a provider credential in local secure settings.", "DISCONNECTED")
        # Explicit empty key for local provider; never inherit old environment secrets.
        return _ObservedClient(self, ModelProvider(provider, self._model(provider), api_key=key))

    def status(self, provider):
        self._name(provider)
        try:
            value = json.loads(self.store.setting("providers." + provider + ".health", "{}"))
        except (ValueError, TypeError):
            value = {}
        if not isinstance(value, dict) or value.get("status") not in STATES:
            return {"status": "DISCONNECTED", "detail": "Connection not checked.", "checked_at": None,
                    "latency_ms": None, "attempts": 0, "failures": 0, "error_rate": None}
        # Persisted values are our fixed messages, never external exception bodies.
        return value

    def _save_health(self, provider, state, detail, latency, measured=False):
        old = self.status(provider)
        attempts = old.get("attempts", 0) + int(measured)
        failures = old.get("failures", 0) + int(measured and state != "CONNECTED")
        result = {"status": state, "detail": detail,
                  "checked_at": datetime.now(timezone.utc).isoformat() if measured else None,
                  "latency_ms": latency, "attempts": attempts, "failures": failures,
                  "error_rate": failures / attempts if attempts else None}
        self.store.set_setting("providers." + provider + ".health", json.dumps(result))
        return result

    def check(self, provider, *, mode="LOCAL_ONLY"):
        """Explicit owner test: sends only a fixed short probe; cloud requires NORMAL."""
        self._name(provider)
        if provider != "ollama" and mode != "NORMAL":
            raise PrivacyError("Cloud connection checks require NORMAL mode.")
        try:
            client = self.client(provider)
        except ProviderError:
            return self._save_health(provider, "DISCONNECTED", "Secure provider credentials are unavailable.", None)
        try:
            client.complete([{"role": "user", "content": "Reply OK."}], mode, "PUBLIC", max_output_tokens=32)
        except PrivacyError:
            raise
        except ProviderError:
            pass  # The observed client already recorded this failed attempt once.
        return self.status(provider)

    def forget(self, provider):
        self._name(provider)
        try:
            self.vault.forget(provider)
        except VaultError:
            raise ProviderError("Could not remove the encrypted provider credential.") from None
        self.store.set_setting("providers." + provider + ".health", "{}")

    def complete(self, provider, messages, mode="LOCAL_ONLY", classification="PERSONAL", *,
                 fallback=None, fallback_approved=False):
        """Text inference only, at most one approved fallback. No tool execution/retry."""
        self._name(provider)
        if fallback is not None:
            self._name(fallback)
            if fallback == provider or fallback_approved is not True:
                raise ProviderError("A distinct fallback requires explicit owner approval.")
        try:
            return self.client(provider).complete(messages, mode, classification)
        except PrivacyError:
            raise
        except ProviderError:
            if fallback is None:
                raise
        # The destination independently applies the same privacy and credential gates.
        return self.client(fallback).complete(messages, mode, classification)
