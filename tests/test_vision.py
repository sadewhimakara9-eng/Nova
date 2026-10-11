"""Local OCR acceptance plus deterministic privacy and failure regressions."""
import hashlib
import io
import shutil
import sys
import unittest
from unittest.mock import patch

from PIL import Image, ImageDraw, ImageFont

from nova.vision import VisionError, VisionGateway, _run


def picture(format="PNG"):
    image = Image.new("RGB", (900, 160), "white")
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 48)
    except OSError:
        font = ImageFont.load_default(size=48)
    draw.text((30, 45), "NOVA LOCAL TEST 123", font=font, fill="black")
    stream = io.BytesIO()
    image.save(stream, format=format)
    image.close()
    return stream.getvalue()


class VisionTests(unittest.TestCase):
    def setUp(self):
        self.gateway = VisionGateway()
        self.data = picture()

    @unittest.skipUnless(shutil.which("tesseract"), "Optional local Tesseract is not installed")
    def test_real_local_ocr(self):
        health = self.gateway.health()
        self.assertTrue(health["available"])
        self.assertIn("eng", health["languages"])
        receipt = self.gateway.analyze_image(self.data)
        self.assertIn("NOVA LOCAL TEST 123", receipt["text"])
        self.assertEqual((receipt["width"], receipt["height"]), (900, 160))
        self.assertEqual(receipt["sha256"], hashlib.sha256(self.data).hexdigest())
        self.assertTrue(receipt["verified"])
        self.assertEqual(receipt["scope"], "local_image_text_extraction")

    def test_privacy_rejects_before_engine_or_image_decode(self):
        with patch("nova.vision._run") as run, patch("nova.vision.Image.open") as decode:
            for policy in ("NO_CAPTURE", "NO_OCR", "CLOUD", None, [], ""):
                with self.subTest(policy=policy), self.assertRaises(VisionError):
                    self.gateway.analyze_image(self.data, policy=policy)
            run.assert_not_called()
            decode.assert_not_called()

    def test_corrupt_unsupported_and_oversized_inputs_do_not_invoke_engine(self):
        with patch("nova.vision._run") as run:
            for data in (b"broken image", b"", "https://example.com/image.png", picture("GIF")):
                with self.subTest(kind=type(data).__name__), self.assertRaises(VisionError):
                    self.gateway.analyze_image(data)
            with patch("nova.vision.MAX_IMAGE_BYTES", 10), self.assertRaises(VisionError):
                self.gateway.analyze_image(self.data)
            with patch("nova.vision.MAX_IMAGE_PIXELS", 100), self.assertRaises(VisionError):
                self.gateway.analyze_image(self.data)
            with patch("nova.vision.Image.MAX_IMAGE_PIXELS", 100), self.assertRaises(VisionError):
                self.gateway.analyze_image(self.data)
            run.assert_not_called()

    def test_missing_engine_friendly(self):
        with patch("nova.vision.shutil.which", return_value=None), patch("nova.vision._run") as run:
            self.assertFalse(self.gateway.health()["available"])
            with self.assertRaisesRegex(VisionError, "not installed"):
                self.gateway.analyze_image(self.data)
            run.assert_not_called()

    def test_languages_are_installed_not_claimed(self):
        with patch("nova.vision.shutil.which", return_value="/fixed/tesseract"), patch(
            "nova.vision._run", return_value=b"List of available languages (2):\neng\nosd\n"
        ) as run:
            self.assertEqual(self.gateway.health()["languages"], ["eng"])
            with self.assertRaisesRegex(VisionError, "not installed"):
                self.gateway.analyze_image(self.data, language="sin")
            with self.assertRaises(VisionError):
                self.gateway.analyze_image(self.data, language="eng; bad")
            self.assertTrue(all(call.args[0] == ["/fixed/tesseract", "--list-langs"]
                                for call in run.call_args_list))

    def test_credentials_withheld_without_value_in_exception(self):
        sensitive = b"password: synthetic-example-only"
        with patch.object(self.gateway, "health", return_value={"available": True, "languages": ["eng"]}), patch(
            "nova.vision.shutil.which", return_value="/fixed/tesseract"
        ), patch("nova.vision._run", return_value=sensitive):
            with self.assertRaisesRegex(VisionError, "withheld") as error:
                self.gateway.analyze_image(self.data)
            self.assertNotIn(sensitive.decode(), str(error.exception))

    def test_fixed_argv_and_jpeg_normalized_to_png(self):
        with patch.object(self.gateway, "health", return_value={"available": True, "languages": ["eng"]}), patch(
            "nova.vision.shutil.which", return_value="/fixed/tesseract"
        ), patch("nova.vision._run", return_value=b"clean text") as run:
            self.gateway.analyze_image(picture("JPEG"), policy="NO_CLOUD_VISION")
            self.assertEqual(run.call_args.args[0],
                             ["/fixed/tesseract", "stdin", "stdout", "-l", "eng", "--psm", "6"])
            self.assertTrue(run.call_args.args[1].startswith(b"\x89PNG"))

    def test_timeout_is_safe_and_child_is_reaped(self):
        with patch("nova.vision.TIMEOUT_SECONDS", 0.05), self.assertRaisesRegex(VisionError, "timed out"):
            _run([sys.executable, "-c", "import time; time.sleep(5)"])

    def test_output_is_bounded(self):
        with self.assertRaisesRegex(VisionError, "output limit"):
            _run([sys.executable, "-c", "print('x' * 1000000)"], limit=1024)
        with self.assertRaisesRegex(VisionError, "output limit"):
            _run([sys.executable, "-c", "import sys; sys.stderr.write('x' * 1000000)"], limit=1024)

    def test_engine_failure_never_repeats_stderr(self):
        with self.assertRaises(VisionError) as error:
            _run([sys.executable, "-c", "import sys; sys.stderr.write('private pixels'); sys.exit(1)"])
        self.assertNotIn("private pixels", str(error.exception))


if __name__ == "__main__":
    unittest.main()
