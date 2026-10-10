"""Managed loopback dashboard with an optional native Windows webview shell.

The webview is presentation only: it exposes no Python/JavaScript bridge, file
dialogs, or additional automation permissions to the dashboard.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import webbrowser


HOST = "127.0.0.1"
PORT = 8502
THEME_FLAGS = [
    "--theme.base", "light",
    "--theme.primaryColor", "#1676ed",
    "--theme.backgroundColor", "#f8fcff",
    "--theme.secondaryBackgroundColor", "#eff7fc",
    "--theme.textColor", "#203a53",
]


class LaunchError(RuntimeError):
    """A safe, actionable local startup error."""


class StreamlitServer:
    """Own exactly one subprocess; never attach to or stop an unrelated service."""

    def __init__(self, root: Path, python: str | None = None, port: int = PORT):
        self.root = Path(root).resolve()
        self.python = python or sys.executable
        self.port = port
        self.url = f"http://{HOST}:{port}"
        self.process: subprocess.Popen | None = None

    def command(self) -> list[str]:
        return [
            self.python, "-m", "streamlit", "run", str(self.root / "nova_app.py"),
            "--server.address", HOST, "--server.port", str(self.port),
            "--server.headless", "true", "--browser.gatherUsageStats", "false",
            "--server.enableCORS", "true", "--server.enableXsrfProtection", "true",
            *THEME_FLAGS,
        ]

    def start(self, timeout: float = 30) -> "StreamlitServer":
        if self.process is not None:
            raise LaunchError("This Nova server has already been started.")
        # Permit POSIX TIME_WAIT sockets after our previous server shuts down.
        # Windows reuse semantics differ: request an exclusive bind there.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            if sys.platform == "win32":
                probe.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            else:
                probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                probe.bind((HOST, self.port))
            except OSError:
                raise LaunchError(
                    f"Local port {self.port} is already in use. Close the existing Nova window "
                    "or stop that service yourself, then launch again. No existing process was changed."
                ) from None
        environment = os.environ.copy()
        environment["PYTHONUTF8"] = "1"
        # Inherit logs for useful diagnostics; no shell and no credential arguments.
        options = {"creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0)} if sys.platform == "win32" else {}
        self.process = subprocess.Popen(self.command(), cwd=self.root, env=environment, **options)
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        deadline = time.monotonic() + timeout
        try:
            while time.monotonic() < deadline:
                if self.process.poll() is not None:
                    raise LaunchError("Nova's dashboard exited during startup. Check the console output above.")
                try:
                    with opener.open(self.url + "/_stcore/health", timeout=0.5) as response:
                        healthy = response.status == 200 and response.read(16).strip() == b"ok"
                    if healthy:
                        # Allow a competing bind/startup failure to surface before opening.
                        time.sleep(0.15)
                        if self.process.poll() is None:
                            return self
                except (urllib.error.URLError, OSError):
                    pass
                time.sleep(0.1)
            raise LaunchError(f"Nova did not become healthy within {timeout:g} seconds. Check the console output and retry.")
        except BaseException:
            self.close()
            raise

    def close(self) -> None:
        process = self.process
        if process is None or process.poll() is not None:
            return
        try:
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        except ProcessLookupError:
            pass


def run_browser(root: Path) -> int:
    server = StreamlitServer(root)
    try:
        server.start()
        print(f"Nova is ready at {server.url}. Keep this console open; press Ctrl+C to stop Nova.", flush=True)
        if not webbrowser.open(server.url):
            print(f"Open {server.url} in your browser.", flush=True)
        if sys.platform == 'win32' and os.environ.get('NOVA_GUI') == '1':
            import ctypes
            ctypes.windll.user32.MessageBoxW(None,
                "NOVA is running in your browser because native mode is unavailable. Leave this message open while using NOVA. Click OK to shut down NOVA's local server.",
                "NOVA browser session", 0x40)
            return 0
        return server.process.wait()
    finally:
        server.close()


def run_desktop(root: Path) -> int:
    if sys.platform != "win32":
        print("The native Nova window is currently supported on Windows. Opening browser mode.", flush=True)
        return run_browser(root)
    try:
        import webview
    except Exception:
        print("The optional Windows desktop component is unavailable. Opening Nova in your browser.", flush=True)
        return run_browser(root)

    server = StreamlitServer(root)
    finished = threading.Event()
    server_failed = threading.Event()
    desktop_failed = False
    try:
        server.start()
        try:
            window = webview.create_window(
                "NOVA", server.url, width=1366, height=900, min_size=(760, 600),
                resizable=True, frameless=False, easy_drag=False, background_color="#f8fcff",
            )

            def watch_server():
                while not finished.wait(0.25):
                    if server.process.poll() is not None:
                        server_failed.set()
                        print("Nova's dashboard stopped. Closing its desktop window.", flush=True)
                        window.destroy()
                        return

            # Native OS frame supplies accessible minimize/maximize/close controls.
            # Edge Chromium uses the maintained Windows WebView2 runtime.
            webview.start(watch_server, gui="edgechromium", debug=False, private_mode=True)
        except Exception:
            desktop_failed = True
            print("The Windows desktop window could not open. Install Microsoft WebView2 for native mode. "
                  "Opening Nova in your browser instead.", flush=True)
    finally:
        finished.set()
        server.close()
    return run_browser(root) if desktop_failed else int(server_failed.is_set())


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Start Nova's managed desktop or browser dashboard.")
    parser.add_argument("--browser", action="store_true", help="Use the system browser instead of a native window.")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    return run_browser(root) if args.browser else run_desktop(root)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Nova closed.")
        raise SystemExit(0) from None
    except (LaunchError, OSError):
        # LaunchError messages are constructed locally and contain no input values.
        error = sys.exc_info()[1]
        print(str(error) if isinstance(error, LaunchError) else "Nova could not start. Check folder access and Python.")
        raise SystemExit(1) from None
