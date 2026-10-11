"""Owner-uploaded image-to-text extraction, entirely local and never persisted."""
from __future__ import annotations

import hashlib
import io
import re
import shutil
import subprocess
import threading
import warnings

from PIL import Image, UnidentifiedImageError

from .providers import contains_credentials

MAX_IMAGE_BYTES = 8 * 1024 * 1024
MAX_IMAGE_PIXELS = 16_000_000
MAX_OUTPUT_BYTES = 64 * 1024
TIMEOUT_SECONDS = 20
_ALLOWED_POLICIES = frozenset({"LOCAL_VISION_ONLY", "NO_CLOUD_VISION"})


class VisionError(RuntimeError):
    """Safe owner-facing failure; never includes images or OCR output."""


def _run(argv: list[str], data: bytes = b"", *, limit: int = MAX_OUTPUT_BYTES) -> bytes:
    """Bound both output pipes and wall time; no shell, files or network calls."""
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, creationflags=flags)
    except OSError:
        raise VisionError("Local OCR could not start. Check your Tesseract installation.") from None
    output = bytearray()
    overflow = threading.Event()

    def read_pipe(pipe, retain: bool):
        count = 0
        try:
            while chunk := pipe.read(4096):
                count += len(chunk)
                if count > limit:
                    overflow.set()
                    process.kill()
                    break
                if retain:
                    output.extend(chunk)
        finally:
            pipe.close()

    def write_input():
        try:
            process.stdin.write(data)
        except (BrokenPipeError, OSError):
            pass
        finally:
            process.stdin.close()

    workers = [threading.Thread(target=read_pipe, args=(process.stdout, True), daemon=True),
               threading.Thread(target=read_pipe, args=(process.stderr, False), daemon=True),
               threading.Thread(target=write_input, daemon=True)]
    for worker in workers:
        worker.start()
    timed_out = False
    try:
        process.wait(timeout=TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        process.wait()
    finally:
        for worker in workers:
            worker.join()
    if timed_out:
        raise VisionError("Local OCR timed out. Try a smaller, clearer image.")
    if overflow.is_set():
        raise VisionError("Local OCR exceeded the safe output limit. Use a smaller image.")
    if process.returncode:
        raise VisionError("Local OCR could not read this image. Try a clear PNG or JPEG.")
    return bytes(output)


class VisionGateway:
    """No capture or semantic scene understanding: explicit uploaded pixels only."""

    def health(self) -> dict:
        executable = shutil.which("tesseract")
        if not executable:
            return {"available": False, "languages": [],
                    "detail": "Tesseract is not installed. Install it locally to enable image text extraction."}
        try:
            result = _run([executable, "--list-langs"], limit=16 * 1024).decode("utf-8", "replace")
            languages = sorted({line.strip() for line in result.splitlines()
                                if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,31}", line.strip())
                                and line.strip() != "osd"})
        except VisionError:
            return {"available": False, "languages": [],
                    "detail": "Tesseract is installed but its language check failed."}
        return {"available": bool(languages), "languages": languages,
                "detail": "Local text extraction only; language availability does not establish accuracy."
                if languages else "Install a Tesseract OCR language locally to enable text extraction."}

    def analyze_image(self, data: bytes, *, policy: str = "LOCAL_VISION_ONLY",
                      language: str = "eng") -> dict:
        if not isinstance(policy, str) or policy not in _ALLOWED_POLICIES:
            raise VisionError("Image text extraction is blocked by the selected vision policy.")
        if not isinstance(data, bytes) or not data or len(data) > MAX_IMAGE_BYTES:
            raise VisionError("Upload a nonempty PNG or JPEG smaller than 8 MiB.")
        if not isinstance(language, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,31}", language):
            raise VisionError("Select one installed OCR language.")
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error", Image.DecompressionBombWarning)
                with Image.open(io.BytesIO(data)) as original:
                    if original.format not in {"PNG", "JPEG"}:
                        raise VisionError("Only PNG and JPEG images are supported.")
                    width, height = original.size
                    if width * height > MAX_IMAGE_PIXELS:
                        raise VisionError("Image exceeds the 16 million pixel limit.")
                    original.verify()
                with Image.open(io.BytesIO(data)) as original:
                    normalized = original.convert("RGB")
                    clean = io.BytesIO()
                    normalized.save(clean, format="PNG")
                    normalized.close()
        except VisionError:
            raise
        except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError,
                Image.DecompressionBombWarning):
            raise VisionError("This image is corrupt, unsupported, or too large to decode safely.") from None
        status = self.health()
        if not status["available"]:
            raise VisionError(status["detail"])
        if language not in status["languages"]:
            raise VisionError("That OCR language is not installed. Choose an available language.")
        executable = shutil.which("tesseract")
        if not executable:
            raise VisionError("Tesseract is no longer available. Check the local installation.")
        output = _run([executable, "stdin", "stdout", "-l", language, "--psm", "6"], clean.getvalue())
        text = output.decode("utf-8", "replace").strip()
        if contains_credentials(text):
            raise VisionError("OCR output was withheld because it resembles credential data.")
        return {"text": text, "width": width, "height": height,
                "sha256": hashlib.sha256(data).hexdigest(), "engine": "tesseract",
                "language": language, "verified": True, "scope": "local_image_text_extraction"}
