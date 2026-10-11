"""Exercise the actual Streamlit workflow without any model or network calls."""

import os
from contextlib import ExitStack
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

try:
    from streamlit.testing.v1 import AppTest
except ImportError:
    AppTest = None


@unittest.skipIf(AppTest is None, "Install Streamlit to run dashboard tests")
class DashboardTests(unittest.TestCase):
    def test_local_workflow_and_provider_configuration_survive_navigation(self):
        from nova.core import NovaCore
        from streamlit import cache_resource

        with tempfile.TemporaryDirectory() as directory, ExitStack() as resources, patch.dict(os.environ, {"NOVA_DATA_DIR": directory}), patch(
            "nova.providers.urllib.request.build_opener", side_effect=AssertionError("Unexpected network request")
        ) as network:
            resources.callback(cache_resource.clear)

            def create_core(*args, **kwargs):
                self.assertEqual(kwargs.get("data_dir"), directory)
                core = NovaCore(*args, **kwargs)
                resources.callback(core.close)
                return core

            resources.enter_context(patch("nova.core.NovaCore", side_effect=create_core))
            app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "nova_app.py"), default_timeout=10).run()
            self.assertFalse(app.exception)
            self.assertFalse(app.error)
            self.assertEqual(app.session_state.nova_language, "auto")

            def navigate(page):
                primary = {'Chat', 'Voice', 'Projects', 'Memory', 'Settings'}
                if page not in primary:
                    app.sidebar.radio[0].set_value('Settings').run()
                    if app.session_state.nova_page != 'Settings':
                        next(item for item in app.button if item.label == 'Back to Settings').click().run()
                    next(item for item in app.button if item.label == 'Open ' + page).click().run()
                else:
                    app.sidebar.radio[0].set_value(page).run()
                    if page == 'Settings' and app.session_state.nova_page != 'Settings':
                        next(item for item in app.button if item.label == 'Back to Settings').click().run()
                self.assertFalse(app.exception)
                self.assertFalse(app.error)

            def button(label):
                return next(item for item in app.button if item.label == label)

            for page in ("Projects", "Agents", "Automations", "Tools", "Integrations", "Devices", "Privacy"):
                navigate(page)
            navigate("Voice")
            self.assertTrue(any("Voice unavailable" in item.value for item in app.markdown))
            self.assertFalse(app.toggle)
            navigate("Chat")
            app.chat_input[0].set_value('Gemini eka open karanna').run()
            self.assertFalse(app.error)
            self.assertTrue(any('unavailable' in item.value for item in app.markdown))
            button('Clear this conversation').click().run()
            app.chat_input[0].set_value("/help").run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.chat_message), 2)

            navigate("Memory")
            next(item for item in app.selectbox if item.label == "Memory scope").set_value("GLOBAL")
            app.text_input[0].set_value("language")
            app.text_area[0].set_value("සිංහල")
            button("Save memory").click().run()
            self.assertFalse(app.exception)
            self.assertTrue(any("language" in item.label for item in app.expander))
            self.assertTrue(any("GLOBAL" in item.label for item in app.expander))

            navigate("Missions")
            app.text_area[0].set_value("/write hello.txt | ආයුබෝවන්")
            button("Prepare plan").click().run()
            self.assertFalse(app.exception)
            self.assertFalse(app.error)
            self.assertFalse((Path(directory) / "workspace" / "hello.txt").exists())
            button("Run prepared plan").click().run()
            button("Approve once").click().run()
            deadline = time.monotonic() + 5
            output = Path(directory) / "workspace" / "hello.txt"
            while not output.exists() and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertEqual(output.read_text(encoding="utf-8"), "ආයුබෝවන්")
            button("Refresh mission status").click().run()
            self.assertFalse(app.exception)
            button("Undo file write").click().run()
            self.assertFalse(app.error)
            self.assertFalse(output.exists())

            navigate("Memory")
            navigate("Settings")
            app.selectbox(key="widget_nova_mode").set_value("READ_ONLY").run()
            navigate("Memory")
            self.assertTrue(button("Save memory").disabled)
            navigate("Settings")
            app.selectbox(key="widget_nova_mode").set_value("LOCAL_ONLY").run()
            navigate("Memory")
            app.checkbox[0].check().run()
            button("Forget").click().run()
            self.assertFalse(any("language" in item.label for item in app.expander))

            navigate("Settings")
            app.selectbox(key="widget_nova_provider").set_value("Ollama (local)").run()
            app.text_input(key="provider_model_ollama").set_value("example-local-model")
            app.button(key="save_ollama").click().run()
            navigate("Chat")
            navigate("Settings")
            self.assertEqual(app.selectbox(key="widget_nova_provider").value, "Ollama (local)")
            self.assertEqual(app.selectbox(key="widget_nova_language").value, "auto")
            self.assertEqual(app.text_input(key="provider_model_ollama").value, "example-local-model")
            app.selectbox(key="widget_nova_provider").set_value("Groq (cloud)").run()
            self.assertTrue(app.text_input(key="provider_secret_groq").disabled)
            navigate("Chat")
            app.chat_input[0].set_value("/help").run()
            self.assertFalse(app.error)
            history = list(app.session_state.nova_messages)
            sensitive = "api_key = synthetic-example-secret"
            app.chat_input[0].set_value(sensitive).run()
            self.assertTrue(app.warning)
            self.assertEqual(app.session_state.nova_messages, history)
            self.assertFalse(any(sensitive in item.value for item in app.markdown))
            navigate("Settings")
            app.selectbox(key="widget_nova_classification").set_value("SECRET").run()
            navigate("Chat")
            protected = "A protected personal fact"
            app.chat_input[0].set_value(protected).run()
            self.assertTrue(app.warning)
            self.assertEqual(app.session_state.nova_messages, history)
            self.assertFalse(any(protected in item.value for item in app.markdown))
            app.chat_input[0].set_value("Nova stop").run()
            self.assertFalse(app.exception)
            self.assertTrue(any(item.label == "Resume agent" for item in app.button))
            app.chat_input[0].set_value("Nova resume").run()
            self.assertFalse(app.exception)
            self.assertTrue(any(item.label == "Emergency stop" for item in app.button))
            navigate("Settings")
            app.selectbox(key="widget_nova_classification").set_value("PERSONAL").run()
            navigate("Chat")
            app.chat_input[0].set_value("Please introduce yourself").run()
            self.assertTrue(any("NORMAL" in item.value for item in app.error))
            app.run()

            button("Emergency stop").click().run()
            self.assertFalse(app.exception)
            self.assertTrue(any(item.label == "Resume agent" for item in app.button))
            button("Resume agent").click().run()
            self.assertFalse(app.exception)
            network.assert_not_called()


    def test_mocked_secure_provider_save_clears_field_and_check_is_explicit(self):
        """Mock vault and HTTP model: validates UI handling, not Windows or live auth."""
        from nova.core import NovaCore
        from nova.provider_hub import ProviderHub
        from streamlit import cache_resource
        with tempfile.TemporaryDirectory() as directory, ExitStack() as resources:
            resources.enter_context(patch.dict(os.environ, {"NOVA_DATA_DIR": directory}))
            resources.callback(cache_resource.clear)
            cores = []
            def create_core(*args, **kwargs):
                core = NovaCore(*args, **kwargs)
                cores.append(core)
                resources.callback(core.close)
                return core
            resources.enter_context(patch("nova.core.NovaCore", side_effect=create_core))
            from unittest.mock import PropertyMock
            resources.enter_context(patch.object(ProviderHub, "vault_available", new_callable=PropertyMock, return_value=True))
            save = resources.enter_context(patch("nova.vault.SecretVault.put"))
            resources.enter_context(patch("nova.vault.SecretVault.get", return_value="synthetic-test-value"))
            complete = resources.enter_context(patch("nova.providers.ModelProvider.complete", return_value="OK"))
            app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "nova_app.py"), default_timeout=10).run()
            self.assertFalse(app.exception)
            self.assertFalse(any(x.label == "Expand navigation" for x in app.toggle))
            self.assertFalse(any(x.label == "Operating mode" for x in app.selectbox))
            self.assertFalse(any("/help" in x.value for x in app.markdown))
            app.sidebar.radio[0].set_value("Settings").run()
            self.assertFalse(app.exception)
            complete.assert_not_called()
            self.assertTrue(app.button(key="check_openai").disabled)
            app.text_input(key="provider_secret_openai").set_value("synthetic-test-value")
            app.button(key="save_openai").click().run()
            self.assertFalse(app.exception)
            save.assert_called_once_with("openai", "synthetic-test-value")
            self.assertEqual(app.text_input(key="provider_secret_openai").value, "")
            self.assertNotIn("synthetic-test-value", str(app.session_state))
            self.assertFalse(any("synthetic-test-value" in x.value for x in app.markdown))
            complete.assert_not_called()
            self.assertEqual(cores[0].provider_hub.status("openai")["status"], "DISCONNECTED")
            app.selectbox(key="widget_nova_mode").set_value("NORMAL").run()
            app.button(key="check_openai").click().run()
            self.assertFalse(app.exception)
            complete.assert_called_once()
            self.assertEqual(cores[0].provider_hub.status("openai")["status"], "CONNECTED")
            app.sidebar.radio[0].set_value("Chat").run()
            app.sidebar.radio[0].set_value("Settings").run()
            self.assertEqual(app.text_input(key="provider_secret_openai").value, "")


if __name__ == "__main__":
    unittest.main()
