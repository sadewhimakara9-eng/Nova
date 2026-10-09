"""One-command bootstrap for the new Nova dashboard on Windows/macOS/Linux."""

import argparse
import os
from pathlib import Path
import subprocess
import sys
import venv


def main(argv=None):
    parser = argparse.ArgumentParser(description="Install and launch Nova.")
    parser.add_argument("--browser", action="store_true", help="Open the browser dashboard without installing native desktop components.")
    args = parser.parse_args(argv)
    if sys.version_info < (3, 11):
        print("Nova needs Python 3.11 or newer. Install it from https://www.python.org/downloads/ and launch again.")
        return 1
    os.environ["PYTHONUTF8"] = "1"
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
    use_desktop = sys.platform == "win32" and not args.browser
    if use_desktop:
        desktop_check = subprocess.run(
            [str(python), "-c", "import importlib.metadata; assert importlib.metadata.version('pywebview') == '6.2.1'; import webview"],
            capture_output=True, check=False,
        )
        if desktop_check.returncode:
            print("Installing the optional Windows desktop window. First launch needs internet access.")
            try:
                subprocess.run([str(python), "-m", "pip", "install", "--disable-pip-version-check",
                                "-r", str(root / "nova-desktop-requirements.txt")], check=True)
            except (OSError, subprocess.CalledProcessError):
                use_desktop = False
                print("The optional desktop component could not be installed. Nova will open in your browser.")
    print("Opening Nova. Keep this console open; press Ctrl+C to close Nova.")
    command = [str(python), str(root / "scripts" / "desktop.py")]
    if not use_desktop:
        command.append("--browser")
    # The child owns its Streamlit process and reliably cleans it up on exit.
    return subprocess.call(command, cwd=root)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, subprocess.CalledProcessError):
        print("Nova could not start. Check Python, your internet connection, and write access to this folder, then launch again.")
        raise SystemExit(1) from None
    except KeyboardInterrupt:
        print("Nova closed.")
