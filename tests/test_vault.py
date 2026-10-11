"""DPAPI behavior is mocked. Real Windows user binding is not exercised on Linux."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import PropertyMock, patch

from nova.vault import SecretVault, VaultError


class VaultTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.vault = SecretVault(self.tmp.name)

    @patch("nova.vault.SecretVault.available", new_callable=PropertyMock, return_value=False)
    def test_unsupported_platform_fails_closed(self, available):
        for operation in (lambda: self.vault.put("openai", "synthetic-auth"),
                          lambda: self.vault.get("openai")):
            with self.assertRaises(VaultError):
                operation()
        self.assertEqual(list(Path(self.tmp.name).iterdir()), [])
        self.vault.forget("openai")  # Ciphertext deletion is safe even without DPAPI.

    @patch("nova.vault.SecretVault.available", new_callable=PropertyMock, return_value=True)
    @patch("nova.vault._dpapi")
    def test_mock_crypto_roundtrip_persists_only_ciphertext(self, crypto, available):
        crypto.side_effect = [b"mock-encrypted-bytes", b"synthetic-auth"]
        self.vault.put("openai", "synthetic-auth")
        path = Path(self.tmp.name) / "secrets" / "openai.dpapi"
        self.assertEqual(path.read_bytes(), b"mock-encrypted-bytes")
        self.assertNotIn(b"synthetic-auth", path.read_bytes())
        self.assertEqual(SecretVault(self.tmp.name).get("openai"), "synthetic-auth")
        crypto.assert_called_with(b"mock-encrypted-bytes", decrypt=True)
        self.vault.forget("openai")
        self.assertFalse(path.exists())
        self.assertIsNone(self.vault.get("openai"))

    @patch("nova.vault.SecretVault.available", new_callable=PropertyMock, return_value=True)
    @patch("nova.vault._dpapi", side_effect=VaultError("Windows could not unlock credential."))
    def test_crypto_failure_never_persists_plaintext(self, crypto, available):
        with self.assertRaises(VaultError):
            self.vault.put("openai", "synthetic-auth")
        self.assertEqual(list(Path(self.tmp.name).iterdir()), [])

    @patch("nova.vault.SecretVault.available", new_callable=PropertyMock, return_value=True)
    def test_invalid_name_and_credentials(self, available):
        for name, value in [("../bad", "synthetic-auth"), ("openai", ""), ("openai", "x\r\ny"), ("openai", "x" * 4097)]:
            with self.assertRaises(VaultError):
                self.vault.put(name, value)
