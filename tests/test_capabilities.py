import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from nova.core import NovaCore, NovaError


class CapabilityTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.core = NovaCore(Path(self.directory.name))

    def tearDown(self):
        self.core.close()
        self.directory.cleanup()

    def test_registry_contains_only_installed_and_authorized_tools(self):
        capabilities = self.core.capabilities()
        self.assertEqual({c['capability_id'] for c in capabilities}, {t['name'] for t in self.core.tools()})
        self.assertNotIn('email.send', {c['capability_id'] for c in capabilities})
        self.assertTrue(all(c['reliability_score'] is None for c in capabilities))
        create = next(c for c in capabilities if c['capability_id'] == 'files.create')
        self.assertEqual(create['required_agents'], ('file-agent',))
        self.assertEqual(create['supported_inputs']['required'], ['path', 'content'])
        self.assertFalse(create['supported_inputs']['additionalProperties'])

    def test_model_planner_receives_dynamic_registry_and_composes_tools(self):
        provider = Mock()
        steps = [
            {'tool': 'files.create', 'args': {'path': 'note.txt', 'content': 'A new idea'}, 'goal': 'Save the idea'},
            {'tool': 'files.read', 'args': {'path': 'note.txt'}, 'goal': 'Verify the saved idea'},
        ]
        provider.complete.return_value = json.dumps(steps)
        self.assertEqual(self.core.plan('Please keep this idea as a note and inspect it afterward', provider), steps)
        prompt = provider.complete.call_args.args[0][0]['content']
        self.assertIn('capability_id', prompt)
        self.assertIn('verification_method', prompt)
        self.assertEqual(self.core.missions(), [])

    def test_capability_gap_never_schedules_a_partial_goal(self):
        provider = Mock()
        provider.complete.return_value = json.dumps({'steps': [], 'missing_capabilities': ['image editing', 'email sending']})
        with self.assertRaisesRegex(NovaError, 'not installed: image editing, email sending'):
            self.core.plan('Edit a picture and email it', provider)
        self.assertEqual(self.core.missions(), [])
        self.assertEqual(self.core.events()[0]['kind'], 'CAPABILITY_GAP')
        self.assertNotIn('image editing', self.core.events()[0]['detail'])

    def test_invalid_or_secret_gap_report_is_rejected(self):
        provider = Mock()
        for report in ({'steps': [], 'missing_capabilities': 'email'},
                       {'steps': [], 'missing_capabilities': ['password=not-a-real-secret']},
                       {'steps': [{'tool': 'system.info'}], 'missing_capabilities': ['email']}):
            provider.complete.return_value = json.dumps(report)
            with self.assertRaises(NovaError):
                self.core.plan('Prepare a goal', provider)
        self.assertEqual(self.core.missions(), [])


if __name__ == '__main__':
    unittest.main()
