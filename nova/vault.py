"""Per-user Windows DPAPI secrets. No plaintext or unsupported-platform fallback."""
from __future__ import annotations

import ctypes
import os
from pathlib import Path
import tempfile


class VaultError(RuntimeError):
    pass


_NAMES = frozenset({"openai", "gemini", "groq", "ollama"})


def _dpapi(data: bytes, decrypt: bool = False) -> bytes:
    """Use current Windows user's DPAPI identity; prohibit any interactive prompt."""
    if os.name != "nt":
        raise VaultError("Secure persistent storage requires Windows DPAPI.")
    from ctypes import wintypes

    class Blob(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_ubyte))]

    buffer = (ctypes.c_ubyte * len(data)).from_buffer_copy(data)
    source = Blob(len(data), buffer)
    output = Blob()
    crypt = ctypes.WinDLL("crypt32", use_last_error=True)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    function = crypt.CryptUnprotectData if decrypt else crypt.CryptProtectData
    function.argtypes = [ctypes.POINTER(Blob), ctypes.c_void_p, ctypes.POINTER(Blob),
                         ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(Blob)]
    function.restype = wintypes.BOOL
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    kernel.LocalFree.restype = ctypes.c_void_p
    try:
        if not function(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(output)):
            raise VaultError("Windows could not access the encrypted credential.")
        return ctypes.string_at(output.pbData, output.cbData)
    finally:
        if output.pbData:
            kernel.LocalFree(output.pbData)
        ctypes.memset(buffer, 0, len(data))


class SecretVault:
    def __init__(self, data_dir):
        self.directory = Path(data_dir) / "secrets"

    @property
    def available(self):
        return os.name == "nt"

    def _path(self, name):
        if name not in _NAMES:
            raise VaultError("Unsupported credential name.")
        if not self.available:
            raise VaultError("Secure persistent storage requires Windows DPAPI.")
        return self.directory / (name + ".dpapi")

    def put(self, name, value):
        path = self._path(name)
        if not isinstance(value, str) or not value.strip() or len(value) > 4096 or any(c in value for c in "\r\n\x00"):
            raise VaultError("Invalid provider credential.")
        try:
            encrypted = _dpapi(value.encode("utf-8"))
            self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
            fd, temporary = tempfile.mkstemp(prefix=".credential-", dir=self.directory)
            try:
                with os.fdopen(fd, "wb") as handle:
                    handle.write(encrypted)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temporary, path)
            finally:
                Path(temporary).unlink(missing_ok=True)
        except (OSError, UnicodeError):
            raise VaultError("Could not securely save the provider credential.") from None

    def get(self, name):
        path = self._path(name)
        try:
            if not path.exists():
                return None
            with path.open("rb") as handle:
                encrypted = handle.read(16385)
            if not encrypted or len(encrypted) > 16384:
                raise VaultError("The encrypted credential is invalid.")
            value = _dpapi(encrypted, decrypt=True).decode("utf-8")
            if not value or len(value) > 4096 or any(c in value for c in "\r\n\x00"):
                raise VaultError("The encrypted credential is invalid.")
            return value
        except (OSError, UnicodeError):
            raise VaultError("Could not unlock the provider credential.") from None

    def forget(self, name):
        # Ciphertext deletion does not require decrypting it or a Windows identity.
        if name not in _NAMES:
            raise VaultError("Unsupported credential name.")
        path = self.directory / (name + ".dpapi")
        try:
            path.unlink(missing_ok=True)
        except OSError:
            raise VaultError("Could not remove the encrypted credential.") from None
