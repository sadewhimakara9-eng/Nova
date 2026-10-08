"""Provider contract tests using mocked HTTP only; no live inference is exercised."""

import io
import json
import ssl
import unittest
import urllib.error
import urllib.request
from unittest.mock import patch

from nova.providers import (
    BLOCKED_CLASSIFICATIONS, MAX_INPUT_BYTES, MAX_OUTPUT_BYTES, MAX_RESPONSE_BYTES,
    MODES, ModelProvider, PrivacyError, ProviderError, _NoRedirect, contains_credentials,
)


class FakeResponse(io.BytesIO):
    def __init__(self, body, url, status=200):
        super().__init__(body)
        self.url, self.status = url, status

    def geturl(self):
        return self.url


class MockHTTPProviderTests(unittest.TestCase):
    def setUp(self):
        self.messages = [{"role": "user", "content": "ආයුබෝවන් Nova"}]

    def mock_response(self, opener, provider="ollama", answer="ආයුබෝවන්!"):
        if provider == "ollama":
            body = {"message": {"content": answer}}
            url = "http://127.0.0.1:11434/api/chat"
        else:
            body = {"choices": [{"message": {"content": answer}}]}
            url = "https://api.groq.com/openai/v1/chat/completions"
        opener.return_value.open.return_value = FakeResponse(json.dumps(body).encode(), url)

    @patch("nova.providers.urllib.request.build_opener")
    def test_local_route_unicode_timeout_and_proxy_protection(self, opener):
        self.mock_response(opener)
        self.assertEqual(ModelProvider().complete(self.messages, mode="OFFLINE"), "ආයුබෝවන්!")
        request = opener.return_value.open.call_args.args[0]
        self.assertEqual(request.full_url, "http://127.0.0.1:11434/api/chat")
        self.assertEqual(json.loads(request.data)["messages"], self.messages)
        self.assertIsNone(request.get_header("Authorization"))
        self.assertEqual(opener.return_value.open.call_args.kwargs["timeout"], 25)
        handlers = opener.call_args.args
        self.assertTrue(any(isinstance(h, _NoRedirect) for h in handlers))
        self.assertEqual(next(h for h in handlers if isinstance(h, urllib.request.ProxyHandler)).proxies, {})

    @patch("nova.providers.urllib.request.build_opener")
    def test_cloud_request_requires_explicit_public_route(self, opener):
        self.mock_response(opener, "groq")
        provider = ModelProvider("groq", "llama-3.3-70b-versatile", "test-auth-value")
        self.assertEqual(provider.complete(self.messages, "NORMAL", "PUBLIC"), "ආයුබෝවන්!")
        request = opener.return_value.open.call_args.args[0]
        self.assertEqual(request.full_url, "https://api.groq.com/openai/v1/chat/completions")
        self.assertEqual(request.get_header("Authorization"), "Bearer test-auth-value")
        https = next(h for h in opener.call_args.args if isinstance(h, urllib.request.HTTPSHandler))
        self.assertEqual(https._context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(https._context.check_hostname)

    @patch("nova.providers.urllib.request.build_opener")
    def test_cloud_privacy_policy_blocks_before_network(self, opener):
        provider = ModelProvider("groq", api_key="test-auth-value")
        for mode in MODES - {"NORMAL"}:
            with self.subTest(mode=mode), self.assertRaises(PrivacyError):
                provider.complete(self.messages, mode, "PUBLIC")
        with self.assertRaises(PrivacyError):
            provider.complete(self.messages, "NORMAL", "PERSONAL")
        with self.assertRaises(PrivacyError):
            provider.complete(self.messages, "NORMAL", "PRIVATE")
        opener.assert_not_called()

    @patch("nova.providers.urllib.request.build_opener")
    def test_private_classification_is_available_locally(self, opener):
        self.mock_response(opener)
        self.assertEqual(ModelProvider().complete(self.messages, classification="PRIVATE"), "ආයුබෝවන්!")

    @patch.dict("os.environ", {"https_proxy": "http://proxy.invalid:3128"}, clear=True)
    @patch("nova.providers.urllib.request.build_opener")
    def test_cloud_honors_system_proxy(self, opener):
        self.mock_response(opener, "groq")
        ModelProvider("groq", api_key="test-auth-value").complete(self.messages, "NORMAL", "PUBLIC")
        proxy = next(h for h in opener.call_args.args if isinstance(h, urllib.request.ProxyHandler))
        self.assertEqual(proxy.proxies["https"], "http://proxy.invalid:3128")

    @patch("nova.providers.urllib.request.build_opener")
    def test_unknown_and_sensitive_classifications_fail_closed(self, opener):
        for provider_name in ("ollama", "groq"):
            provider = ModelProvider(provider_name)
            for classification in BLOCKED_CLASSIFICATIONS | {"unknown"}:
                with self.subTest(provider=provider_name, classification=classification), self.assertRaises(PrivacyError):
                    provider.complete(self.messages, "NORMAL", classification)
            with self.assertRaises(PrivacyError):
                provider.complete(self.messages, "unknown", "PUBLIC")
        opener.assert_not_called()

    @patch("nova.providers.urllib.request.build_opener")
    def test_credentials_are_blocked_even_when_declared_public(self, opener):
        examples = [
            "gsk_" + "x" * 30, "sk-proj-" + "x" * 30, "password=hunter2",
            '{"api_key": "example-sensitive-value"}', "my password is hunter2",
            "-----BEGIN RSA PRIVATE KEY-----", "postgres://user:password@localhost/db",
        ]
        for value in examples:
            with self.subTest(value_kind=value[:8]):
                self.assertTrue(contains_credentials(value))
                with self.assertRaises(PrivacyError):
                    ModelProvider().complete([{"role": "user", "content": value}], "NORMAL", "PUBLIC")
        self.assertFalse(contains_credentials("Please explain password policies and API keys."))
        opener.assert_not_called()

    @patch("nova.providers.urllib.request.build_opener")
    def test_input_limits_and_invalid_messages(self, opener):
        for messages in ([], [{"role": "tool", "content": "text"}],
                         [{"role": "user", "content": "x" * (MAX_INPUT_BYTES + 1)}],
                         [{"role": "user", "content": "text", "secret": "extra"}]):
            with self.assertRaises(ProviderError):
                ModelProvider().complete(messages)
        opener.assert_not_called()

    @patch("nova.providers.urllib.request.build_opener")
    def test_errors_do_not_expose_request_or_credentials(self, opener):
        opener.return_value.open.side_effect = urllib.error.URLError("SECRET_REQUEST_VALUE")
        with self.assertRaises(ProviderError) as error:
            ModelProvider().complete(self.messages)
        self.assertNotIn("SECRET_REQUEST_VALUE", str(error.exception))

    @patch("nova.providers.urllib.request.build_opener")
    def test_bad_and_oversized_responses(self, opener):
        url = "http://127.0.0.1:11434/api/chat"
        for body in (b"not JSON", b"{}", b"[]", b"x" * (MAX_RESPONSE_BYTES + 1)):
            opener.return_value.open.return_value = FakeResponse(body, url)
            with self.assertRaises(ProviderError):
                ModelProvider().complete(self.messages)
        self.mock_response(opener, answer="x" * (MAX_OUTPUT_BYTES + 1))
        with self.assertRaises(ProviderError):
            ModelProvider().complete(self.messages)

    @patch("nova.providers.urllib.request.build_opener")
    def test_redirect_response_is_rejected(self, opener):
        opener.return_value.open.return_value = FakeResponse(b"{}", "https://other.invalid")
        with self.assertRaises(ProviderError):
            ModelProvider().complete(self.messages)
        request = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions")
        self.assertIsNone(_NoRedirect().redirect_request(request, None, 302, "Found", {}, "https://other.invalid"))

    @patch("nova.providers.urllib.request.build_opener")
    def test_status_does_not_claim_a_connection_or_expose_key(self, opener):
        provider = ModelProvider("groq", api_key="example-private-auth")
        self.assertEqual(provider.status()["connection"], "not_checked")
        self.assertTrue(provider.status()["configured"])
        self.assertNotIn("example-private-auth", str(provider.status()))
        opener.assert_not_called()

    @patch.dict("os.environ", {}, clear=True)
    @patch("nova.providers.urllib.request.build_opener")
    def test_missing_cloud_key_is_actionable_and_never_connects(self, opener):
        with self.assertRaisesRegex(ProviderError, "GROQ_API_KEY"):
            ModelProvider("groq").complete(self.messages, "NORMAL", "PUBLIC")
        opener.assert_not_called()


if __name__ == "__main__":
    unittest.main()
