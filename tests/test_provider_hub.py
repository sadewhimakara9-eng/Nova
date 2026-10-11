"""Mocked transport/vault tests; no real cloud connectivity claims."""
import io
import json
from pathlib import Path
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

from nova.provider_hub import ProviderHub
from nova.providers import ModelProvider, ProviderError, PrivacyError
from nova.storage import Store


class Response(io.BytesIO):
    status = 200

    def __init__(self, body, url):
        super().__init__(json.dumps(body).encode())
        self.url = url

    def geturl(self):
        return self.url


class ProviderHubTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Store(Path(self.tmp.name) / "state.db")
        self.hub = ProviderHub(self.store, self.tmp.name)
        self.messages = [{"role": "user", "content": "Hello"}]

    @patch("nova.providers.urllib.request.build_opener")
    def test_openai_and_gemini_fixed_destinations(self, opener):
        for name, url, body in [
            ("openai", "https://api.openai.com/v1/chat/completions", {"choices": [{"message": {"content": "OK"}}]}),
            ("gemini", "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
             {"candidates": [{"content": {"parts": [{"text": "OK"}]}}]}),
        ]:
            with self.subTest(name=name):
                opener.return_value.open.return_value = Response(body, url)
                model = "gpt-4.1-mini" if name == "openai" else "gemini-2.5-flash"
                result = ModelProvider(name, model, "synthetic-auth").complete(
                    [{"role": "system", "content": "Be brief"}] + self.messages, "NORMAL", "PUBLIC", max_output_tokens=32)
                self.assertEqual(result, "OK")
                request = opener.return_value.open.call_args.args[0]
                self.assertEqual(request.full_url, url)
                self.assertNotIn("synthetic-auth", request.full_url)
                data = json.loads(request.data)
                if name == "gemini":
                    self.assertIsNone(request.get_header("Authorization"))
                    self.assertEqual(data["systemInstruction"]["parts"][0]["text"], "Be brief")
                    self.assertEqual(data["generationConfig"]["maxOutputTokens"], 32)
                else:
                    self.assertEqual(data["max_tokens"], 32)

    @patch("nova.providers.urllib.request.build_opener")
    def test_new_cloud_adapters_block_private_and_secret_before_network(self, opener):
        for name in ("openai", "gemini"):
            client = ModelProvider(name, "test-model", "synthetic-auth")
            for mode, classification in [("LOCAL_ONLY", "PUBLIC"), ("NORMAL", "PERSONAL"), ("NORMAL", "SECRET")]:
                with self.assertRaises(PrivacyError):
                    client.complete(self.messages, mode, classification)
        opener.assert_not_called()
        for model in ("../other", "foo/bar", "x?key=y", "x:generateContent"):
            with self.assertRaises(ProviderError):
                ModelProvider("gemini", model)

    @patch("nova.providers.urllib.request.build_opener")
    def test_error_status_is_sanitized(self, opener):
        for code, expected in [(401, "AUTH_EXPIRED"), (403, "AUTH_EXPIRED"), (429, "RATE_LIMITED"), (500, "DEGRADED")]:
            opener.return_value.open.side_effect = urllib.error.HTTPError("https://private.invalid", code, "sensitive exception detail", {}, None)
            with self.assertRaises(ProviderError) as error:
                ModelProvider("openai", api_key="synthetic-auth").complete(self.messages, "NORMAL", "PUBLIC")
            self.assertEqual(error.exception.status, expected)
            self.assertNotIn("sensitive", str(error.exception))
            self.assertNotIn("private.invalid", str(error.exception))

    @patch("nova.provider_hub.SecretVault")
    def test_only_model_and_safe_health_in_database(self, vault):
        hub = ProviderHub(self.store, self.tmp.name)
        hub.configure("openai", "gpt-4.1-mini", "synthetic-auth")
        vault.return_value.put.assert_called_once_with("openai", "synthetic-auth")
        self.assertEqual(hub.status("openai")["status"], "DISCONNECTED")
        with self.store.connect() as db:
            self.assertNotIn("synthetic-auth", str(db.execute("SELECT * FROM settings").fetchall()))
        self.assertNotIn("synthetic-auth", str(hub.providers()))
        with self.assertRaises(ProviderError):
            hub.configure("openai", "invalid model", "synthetic-auth")
        self.assertEqual(vault.return_value.put.call_count, 1)

    @patch("nova.provider_hub.ModelProvider.complete", return_value="OK")
    @patch("nova.provider_hub.SecretVault.get", return_value="synthetic-auth")
    def test_explicit_connection_check_and_forget(self, get, complete):
        with self.assertRaises(PrivacyError):
            self.hub.check("openai")
        complete.assert_not_called()
        result = self.hub.check("openai", mode="NORMAL")
        self.assertEqual(result["status"], "CONNECTED")
        self.assertIsNotNone(result["checked_at"])
        self.assertEqual(result["attempts"], 1)
        self.assertEqual(complete.call_args.kwargs["max_output_tokens"], 32)
        complete.side_effect = ProviderError("private error must not persist", "RATE_LIMITED")
        result = self.hub.check("openai", mode="NORMAL")
        self.assertEqual(result["status"], "RATE_LIMITED")
        self.assertEqual(result["error_rate"], .5)
        self.assertNotIn("private error", str(result))
        self.hub.forget("openai")
        self.assertEqual(self.hub.status("openai")["status"], "DISCONNECTED")

    @patch("nova.provider_hub.SecretVault.get", return_value="synthetic-auth")
    @patch("nova.providers.urllib.request.build_opener")
    def test_fallback_needs_approval_and_rechecks_destination_privacy(self, opener, get):
        opener.return_value.open.side_effect = urllib.error.URLError("offline")
        with self.assertRaises(ProviderError):
            self.hub.complete("ollama", self.messages, fallback="openai")
        opener.assert_not_called()
        with self.assertRaises(PrivacyError):
            self.hub.complete("ollama", self.messages, fallback="openai", fallback_approved=True)
        self.assertEqual(opener.return_value.open.call_count, 1)  # local attempt only
        opener.reset_mock()
        with self.assertRaises(PrivacyError):
            self.hub.complete("openai", self.messages, fallback="gemini", fallback_approved=True)
        opener.assert_not_called()

    @patch("nova.provider_hub.SecretVault.get", return_value="synthetic-auth")
    @patch("nova.providers.urllib.request.build_opener")
    def test_approved_fallback_is_single_text_call(self, opener, get):
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        opener.return_value.open.side_effect = [urllib.error.URLError("unavailable"),
            Response({"candidates": [{"content": {"parts": [{"text": "Fallback reply"}]}}]}, url)]
        reply = self.hub.complete("openai", self.messages, "NORMAL", "PUBLIC", fallback="gemini", fallback_approved=True)
        self.assertEqual(reply, "Fallback reply")
        self.assertEqual(opener.return_value.open.call_count, 2)

    @patch.dict("os.environ", {"OPENAI_API_KEY": "synthetic-env-auth"})
    @patch("nova.provider_hub.SecretVault.get", return_value=None)
    def test_hub_does_not_reuse_environment_credentials(self, get):
        with self.assertRaises(ProviderError):
            self.hub.client("openai")

    @patch("nova.provider_hub.SecretVault.get", return_value="synthetic-auth")
    @patch("nova.providers.urllib.request.build_opener")
    def test_chat_client_records_real_transport_outcomes_and_preserves_interface(self, opener, get):
        client = self.hub.client("openai")
        self.assertEqual(client.provider, "openai")
        self.assertEqual(client.model, "gpt-4.1-mini")
        self.assertEqual(self.hub.status("openai")["attempts"], 0)
        opener.return_value.open.return_value = Response(
            {"choices": [{"message": {"content": "Hello"}}]}, "https://api.openai.com/v1/chat/completions")
        self.assertEqual(client.complete(self.messages, "NORMAL", "PUBLIC", max_output_tokens=64), "Hello")
        self.assertEqual(json.loads(opener.return_value.open.call_args.args[0].data)["max_tokens"], 64)
        health = self.hub.status("openai")
        self.assertEqual((health["status"], health["attempts"], health["failures"]), ("CONNECTED", 1, 0))
        opener.return_value.open.side_effect = urllib.error.HTTPError("https://private.invalid", 429, "sensitive detail", {}, None)
        with self.assertRaises(ProviderError):
            client.complete(self.messages, "NORMAL", "PUBLIC")
        health = self.hub.status("openai")
        self.assertEqual((health["status"], health["attempts"], health["failures"]), ("RATE_LIMITED", 2, 1))
        self.assertNotIn("sensitive", str(health))
        with self.assertRaises(PrivacyError):
            client.complete(self.messages, "PRIVATE", "PUBLIC")
        self.assertEqual(self.hub.status("openai"), health)
        self.assertEqual(opener.return_value.open.call_count, 2)
