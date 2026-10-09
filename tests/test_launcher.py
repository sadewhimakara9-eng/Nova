"""Desktop API behavior is mocked; managed server health/cleanup uses a real child."""

import importlib.util
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

from scripts import desktop, run_nova


class LauncherTests(unittest.TestCase):
    def test_theme_and_security_flags_are_shared_by_both_windows(self):
        command = desktop.StreamlitServer(Path.cwd()).command()
        for flag, value in (
            ("--server.address", "127.0.0.1"), ("--server.port", "8502"),
            ("--server.enableCORS", "true"), ("--server.enableXsrfProtection", "true"),
            ("--theme.base", "light"), ("--theme.primaryColor", "#1676ed"),
            ("--theme.backgroundColor", "#f8fcff"), ("--theme.secondaryBackgroundColor", "#eff7fc"),
            ("--theme.textColor", "#203a53"),
        ):
            self.assertEqual(command[command.index(flag) + 1], value)

    def test_occupied_port_is_never_attached_to_or_terminated(self):
        with socket.socket() as unrelated:
            unrelated.bind(("127.0.0.1", 0))
            unrelated.listen()
            port = unrelated.getsockname()[1]
            server = desktop.StreamlitServer(Path.cwd(), port=port)
            with patch.object(desktop.subprocess, "Popen") as spawn:
                with self.assertRaisesRegex(desktop.LaunchError, "already in use"):
                    server.start()
                server.close()
                spawn.assert_not_called()
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                pass

    def test_close_only_terminates_owned_process_and_escalates_if_needed(self):
        server = desktop.StreamlitServer(Path.cwd())
        process = Mock()
        process.poll.return_value = None
        process.wait.side_effect = [subprocess.TimeoutExpired("owned-child", 5), 0]
        server.process = process
        server.close()
        process.terminate.assert_called_once_with()
        process.kill.assert_called_once_with()
        self.assertEqual(process.wait.call_count, 2)
        process.poll.return_value = 0
        server.close()
        process.terminate.assert_called_once()

    @patch.object(desktop.subprocess, "Popen")
    def test_failed_health_startup_cleans_up_its_child(self, spawn):
        child = spawn.return_value
        child.poll.return_value = None
        with socket.socket() as reservation:
            reservation.bind(("127.0.0.1", 0))
            port = reservation.getsockname()[1]
        server = desktop.StreamlitServer(Path.cwd(), port=port)
        with self.assertRaisesRegex(desktop.LaunchError, "did not become healthy"):
            server.start(timeout=0)
        child.terminate.assert_called_once()
        child.wait.assert_called_once_with(timeout=5)

    @patch.object(desktop.sys, "platform", "win32")
    @patch.object(desktop, "StreamlitServer")
    def test_native_window_has_standard_controls_and_always_closes_child(self, factory):
        server = factory.return_value
        server.url = "http://127.0.0.1:8502"
        webview = Mock()
        with patch.dict(sys.modules, {"webview": webview}):
            self.assertEqual(desktop.run_desktop(Path.cwd()), 0)
        server.start.assert_called_once()
        server.close.assert_called_once()
        options = webview.create_window.call_args.kwargs
        self.assertEqual((options["width"], options["height"]), (1366, 900))
        self.assertEqual(options["min_size"], (760, 600))
        self.assertTrue(options["resizable"])
        self.assertFalse(options["frameless"])
        self.assertNotIn("js_api", options)
        self.assertTrue(webview.start.call_args.kwargs["private_mode"])
        self.assertFalse(webview.start.call_args.kwargs["debug"])

    @patch.object(desktop.sys, "platform", "win32")
    @patch.object(desktop, "run_browser", return_value=0)
    @patch.object(desktop, "StreamlitServer")
    def test_failed_native_window_closes_child_before_browser_fallback(self, factory, browser):
        webview = Mock()
        webview.start.side_effect = RuntimeError("Unavailable native runtime")
        browser.side_effect = lambda root: (factory.return_value.close.assert_called_once(), 0)[1]
        with patch.dict(sys.modules, {"webview": webview}):
            self.assertEqual(desktop.run_desktop(Path.cwd()), 0)
        browser.assert_called_once()

    @patch.object(desktop.sys, "platform", "linux")
    @patch.object(desktop, "run_browser", return_value=0)
    def test_unsupported_platform_opens_browser(self, browser):
        self.assertEqual(desktop.run_desktop(Path.cwd()), 0)
        browser.assert_called_once()

    @patch.object(desktop.sys, "platform", "win32")
    @patch.object(desktop, "run_browser", return_value=0)
    def test_missing_optional_native_dependency_falls_back(self, browser):
        with patch.dict(sys.modules, {"webview": None}):
            self.assertEqual(desktop.run_desktop(Path.cwd()), 0)
        browser.assert_called_once()

    @patch.object(run_nova.sys, "platform", "win32")
    @patch.object(run_nova.Path, "exists", return_value=True)
    @patch.object(run_nova.subprocess, "call", return_value=0)
    @patch.object(run_nova.subprocess, "run")
    def test_windows_bootstrap_installs_optional_requirements_and_launches_native(self, run, call, exists):
        run.side_effect = [Mock(returncode=0), Mock(returncode=1), Mock(returncode=0)]
        self.assertEqual(run_nova.main([]), 0)
        pip_command = run.call_args_list[2].args[0]
        self.assertTrue(pip_command[-1].endswith("nova-desktop-requirements.txt"))
        self.assertNotIn("--browser", call.call_args.args[0])
        self.assertEqual(run_nova.os.environ["PYTHONUTF8"], "1")

    @patch.object(run_nova.sys, "platform", "win32")
    @patch.object(run_nova.Path, "exists", return_value=True)
    @patch.object(run_nova.subprocess, "call", return_value=0)
    @patch.object(run_nova.subprocess, "run")
    def test_optional_install_failure_falls_back_without_blocking_dashboard(self, run, call, exists):
        run.side_effect = [Mock(returncode=0), Mock(returncode=1), subprocess.CalledProcessError(1, "pip")]
        self.assertEqual(run_nova.main([]), 0)
        self.assertEqual(call.call_args.args[0][-1], "--browser")

    @patch.object(run_nova.sys, "platform", "linux")
    @patch.object(run_nova.Path, "exists", return_value=True)
    @patch.object(run_nova.subprocess, "call", return_value=0)
    @patch.object(run_nova.subprocess, "run", return_value=Mock(returncode=0))
    def test_linux_never_installs_optional_windows_requirements(self, run, call, exists):
        self.assertEqual(run_nova.main([]), 0)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(call.call_args.args[0][-1], "--browser")

    def test_real_streamlit_health_and_owned_child_shutdown(self):
        if importlib.util.find_spec("streamlit") is None:
            self.skipTest("Run with .venv-nova Python to exercise real Streamlit startup")
        with tempfile.TemporaryDirectory(prefix="nova-launch-test-") as temporary:
            root = Path(temporary)
            (root / "nova_app.py").write_text("import streamlit as st\nst.title('Launcher health test')\n", encoding="utf-8")
            with socket.socket() as reservation:
                reservation.bind(("127.0.0.1", 0))
                port = reservation.getsockname()[1]
            # Relaunch immediately on the same port, including TIME_WAIT sockets
            # left by the health request. A running unrelated listener is covered
            # separately and must still prevent startup.
            for _ in range(2):
                server = desktop.StreamlitServer(root, port=port)
                try:
                    server.start(timeout=15)
                    self.assertIsNone(server.process.poll())
                    self.assertTrue(server.url.startswith("http://127.0.0.1:"))
                finally:
                    server.close()
                self.assertIsNotNone(server.process.poll())
                with socket.socket() as probe:
                    probe.settimeout(1)
                    self.assertNotEqual(probe.connect_ex(("127.0.0.1", port)), 0)


if __name__ == "__main__":
    unittest.main()
