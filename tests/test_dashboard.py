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
            self.assertTrue(any("Microphone unavailable" == item.label and item.disabled for item in app.button))
            app.toggle(key="nova_voice_preview").set_value(True).run()
            app.selectbox(key="nova_voice_demo_state").set_value("listening").run()
            self.assertTrue(any("Simulated animation only" in item.value for item in app.caption))
            button("Stop preview").click().run()
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
            app.selectbox(key="nova_mode").set_value("READ_ONLY").run()
            self.assertTrue(button("Save memory").disabled)
            app.selectbox(key="nova_mode").set_value("LOCAL_ONLY").run()
            app.checkbox[0].check().run()
            button("Forget").click().run()
            self.assertFalse(any("language" in item.label for item in app.expander))

            navigate("Settings")
            app.selectbox(key="widget_nova_provider").set_value("Ollama (local)").run()
            app.text_input(key="widget_nova_ollama_model").set_value("example-local-model").run()
            navigate("Home")
            app.run()
            navigate("Settings")
            self.assertEqual(app.selectbox(key="widget_nova_provider").value, "Ollama (local)")
            self.assertEqual(app.text_input(key="widget_nova_ollama_model").value, "example-local-model")

            app.selectbox(key="widget_nova_provider").set_value("Groq (cloud)").run()
            app.text_input(key="widget_nova_api_key").set_value("test-session-value").run()
            navigate("Home")
            navigate("Settings")
            self.assertEqual(app.text_input(key="widget_nova_api_key").value, "test-session-value")
            button("Clear API key").click().run()
            self.assertEqual(app.text_input(key="widget_nova_api_key").value, "")

            navigate("Chat")
            app.chat_input[0].set_value("/help").run()
            self.assertFalse(app.error)
            history = list(app.session_state.nova_messages)
            sensitive = "api_key = synthetic-example-secret"
            app.chat_input[0].set_value(sensitive).run()
            self.assertTrue(app.warning)
            self.assertEqual(app.session_state.nova_messages, history)
            self.assertFalse(any(sensitive in item.value for item in app.markdown))
            app.selectbox(key="nova_classification").set_value("SECRET").run()
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
            app.selectbox(key="nova_classification").set_value("PERSONAL").run()
            app.chat_input[0].set_value("Please introduce yourself").run()
            self.assertTrue(any("NORMAL" in item.value for item in app.error))
            app.run()

            button("Emergency stop").click().run()
            self.assertFalse(app.exception)
            self.assertTrue(any(item.label == "Resume agent" for item in app.button))
            button("Resume agent").click().run()
            self.assertFalse(app.exception)
            network.assert_not_called()


if __name__ == "__main__":
    unittest.main()
