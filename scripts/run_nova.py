"""One-command bootstrap for the new Nova dashboard on Windows/macOS/Linux."""

import os
from pathlib import Path
import subprocess
import sys
import venv


def main():
    if sys.version_info < (3, 11):
        print("Nova needs Python 3.11 or newer. Install it from https://www.python.org/downloads/ and launch again.")
        return 1
    root = Path(__file__).resolve().parent.parent
    environment = root / ".venv-nova"
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.exists():
        print("Preparing Nova for the first time…")
        venv.EnvBuilder(with_pip=True).create(environment)
    check = subprocess.run(
        [str(python), "-c", "import importlib.metadata; assert importlib.metadata.version('streamlit') == '1.65.0'"],
        capture_output=True, check=False,
    )
    if check.returncode:
        print("Installing the dashboard. Internet access is needed on the first launch.")
        subprocess.run([str(python), "-m", "pip", "install", "--disable-pip-version-check",
                        "-r", str(root / "nova-requirements.txt")], check=True)
    print("Opening Nova. Keep this window open; press Ctrl+C to close Nova.")
    return subprocess.call([
        str(python), "-m", "streamlit", "run", str(root / "nova_app.py"),
        "--server.address", "127.0.0.1", "--server.port", "8502",
        "--browser.gatherUsageStats", "false",
    ], cwd=root)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, subprocess.CalledProcessError):
        print("Nova could not start. Check Python, your internet connection, and write access to this folder, then launch again.")
        raise SystemExit(1) from None
    except KeyboardInterrupt:
        print("Nova closed.")
