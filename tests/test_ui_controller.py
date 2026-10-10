"""Presentation state stays honest and cannot enable missing integrations."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from nova.core import NovaCore
from nova.ui.controller import (UIController, appearance_settings, assistant_state,
                                greeting, mission_group, elapsed_label)
from nova.ui.glass import badge, header, orb, apply_theme


class PresentationTests(unittest.TestCase):
    def test_orb_state_uses_actual_missions_and_stop_overrides_work(self):
        rows = [{"status": "RUNNING"}, {"status": "QUEUED"}, {"status": "BLOCKED"}]
        live = assistant_state(rows)
        self.assertEqual((live.running, live.queued, live.waiting, live.orb), (1, 1, 1, "working"))
        self.assertEqual(assistant_state(rows, stopped=True).orb, "warning")
        self.assertEqual(assistant_state([], mode="OFFLINE").orb, "offline")
        self.assertEqual(assistant_state([], mode="LOCAL_ONLY").orb, "privacy")

    def test_appearance_is_validated_persisted_and_contains_no_arbitrary_settings(self):
        with tempfile.TemporaryDirectory() as directory:
            core = NovaCore(Path(directory))
            try:
                controller = UIController(core)
                saved = controller.save_appearance({"glass": 80, "blur": 0, "performance": True,
                                                    "api_key": "do-not-save", "scale": 100000, "accent": "Mint"})
                self.assertEqual(saved['accent'], 'Mint')
                self.assertEqual(appearance_settings({'accent': '<script>'})['accent'], 'Ice Blue')
                self.assertEqual(saved["scale"], 100)
                self.assertEqual(saved, controller.appearance())
                self.assertNotIn("api_key", core.store.setting("ui.appearance"))
                core.store.set_setting("ui.appearance", "bad-json")
                self.assertEqual(controller.appearance(), appearance_settings(None))
            finally:
                core.close()

    def test_cloud_activity_is_not_inferred_from_local_or_start_events(self):
        with tempfile.TemporaryDirectory() as directory:
            core = NovaCore(Path(directory))
            try:
                controller = UIController(core)
                core.store.event("MODEL_RESPONSE", provider="ollama")
                self.assertEqual(controller.external_activity(), [])
                core.store.event("MODEL_RESPONSE", provider="groq")
                self.assertEqual(len(controller.external_activity()), 1)
                self.assertEqual(len(controller.agents()), len(core.agents.agents))
                self.assertEqual(controller.agents()[0]["reliability"], "Not measured yet")
            finally:
                core.close()

    def test_mission_groups_and_sinhala_greeting(self):
        self.assertEqual(mission_group("FAILED"), "Waiting for You")
        self.assertEqual(mission_group("PAUSED"), "Waiting for You")
        self.assertEqual(mission_group("COMPLETED"), "Completed")
        self.assertEqual(greeting("si", 8), "සුභ උදෑසනක්.")
        self.assertEqual(greeting("en", 20), "Good evening.")
        self.assertEqual(elapsed_label({}), "—")

    def test_presentational_html_escapes_text_and_appearance_cannot_inject_css(self):
        with patch("nova.ui.glass.st.html") as output:
            header('<script>alert(1)</script>', '<img src=x>')
            rendered = output.call_args.args[0]
            self.assertNotIn('<script>', rendered)
            self.assertIn('&lt;script&gt;', rendered)
            self.assertIn('&lt;img', badge('<img src=x>'))
            orb('not-a-state', 9999, '<private>')
            rendered = output.call_args.args[0]
            self.assertIn('nova-orb-idle', rendered)
            self.assertNotIn('<private>', rendered)
            apply_theme({'blur': '}</style><script>injected</script>'})
            self.assertNotIn('<script>', output.call_args.args[0])
            self.assertIn('prefers-reduced-motion', output.call_args.args[0])


if __name__ == '__main__':
    unittest.main()
