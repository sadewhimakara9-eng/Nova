import tempfile
import unittest
from pathlib import Path

from scripts.package_release import check_release, release_files


class ReleaseTests(unittest.TestCase):
    def test_release_allowlist_excludes_legacy_credentials_and_runtime_data(self):
        root = Path(__file__).resolve().parents[1]
        files = release_files(root)
        self.assertNotIn(root / 'app.py', files)
        self.assertNotIn(root / '.env', files)
        self.assertTrue(all('.venv-nova' not in p.parts for p in files))
        self.assertIn(root / 'nova/ui/glass.css', files)

    def test_token_blocks_release_without_printing_token(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'unsafe.py'
            secret = 'gsk_' + 'A1' * 20
            path.write_text(secret)
            with self.assertRaises(ValueError) as error:
                check_release(root, [path])
            self.assertNotIn(secret, str(error.exception))

    def test_private_key_material_is_blocked_but_marker_example_is_not(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'example.txt'
            marker = '-----BEGIN ' + 'PRIVATE KEY-----'
            path.write_text(marker)
            check_release(root, [path])
            path.write_text(marker + '\n' + 'A' * 64 + '\n-----END ' + 'PRIVATE KEY-----')
            with self.assertRaises(ValueError):
                check_release(root, [path])


if __name__ == '__main__':
    unittest.main()
