"""Build and verify a standalone release without legacy source or runtime data."""
import argparse
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def release_files(root):
    names = ("README.md", "AGENTS.md", ".gitignore", ".env.example", "Start Nova.bat", "Start Nova.pyw",
             "start-nova.sh", "nova-requirements.txt", "nova-desktop-requirements.txt", "nova_app.py")
    files = [root / name for name in names]
    for folder in ("nova", "scripts", "tests", "docs"):
        files.extend(path for path in (root / folder).rglob("*")
                     if path.is_file() and "__pycache__" not in path.parts
                     and path.suffix not in {".pyc", ".sqlite3", ".log"})
    return sorted(files)


def check_release(root, files):
    """Detect high-confidence token/private-key formats without printing values.

    This is a release guard, not a complete secret audit. Generic password-like
    examples in test cases are deliberately not classified as actual credentials.
    """
    token = re.compile(r"\b(?:gsk_|sk-proj-|github_pat_|ghp_)[A-Za-z0-9_-]{24,}|"
                       r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----\s+"
                       r"[A-Za-z0-9+/=\r\n]{40,}-----END ")
    for path in files:
        relative = path.relative_to(root)
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"Release file escapes the checkout: {relative}")
        if path.suffix in {".py", ".pyw", ".json", ".md", ".txt", ".example", ".bat", ".sh"}:
            if token.search(path.read_text(encoding="utf-8")):
                raise ValueError(f"Possible credential detected; release blocked: {relative}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="downloads/Nova-agent-v0.4.zip")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    destination = root / args.output
    files = release_files(root)
    check_release(root, files)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, Path("Nova-agent") / path.relative_to(root))
    with ZipFile(destination) as archive:
        assert archive.testzip() is None
        assert "Nova-agent/app.py" not in archive.namelist()
        assert "Nova-agent/nova/ui/glass.css" in archive.namelist()
        assert "Nova-agent/scripts/desktop.py" in archive.namelist()
        assert "Nova-agent/nova/feature_catalog.json" in archive.namelist()
        print(f"Verified {destination.name}: {len(archive.namelist())} files; legacy source and runtime data excluded.")


if __name__ == "__main__":
    main()
