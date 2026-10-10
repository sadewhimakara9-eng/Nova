from pathlib import Path
import json
import sqlite3
import tempfile
import unittest

from nova.core import NovaCore


class DecisionTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.path = Path(self.directory.name)
        self.core = NovaCore(self.path)

    def tearDown(self):
        self.core.close()
        self.directory.cleanup()

    def test_record_search_edit_restart_and_forget(self):
        mid = self.core.save_decision('Game', 'Unreal තෝරමු', 'Rendering tools', 'Godot; Unity')
        self.core.save_decision('Other project', 'Use Godot', 'Small download')
        row = self.core.decisions('තෝරමු', project='game')[0]
        self.assertEqual(row['id'], mid)
        self.assertEqual(row['revision'], 1)
        created = row['created_at']
        self.core.save_decision('Game', 'Unreal තෝරමු', 'Updated recorded reason', 'Godot', decision_id=mid, revision=1)
        self.core.close()
        self.core = NovaCore(self.path)
        row = self.core.decisions(project='Game')[0]
        self.assertEqual(row['created_at'], created)
        self.assertEqual(row['revision'], 2)
        self.assertIn('Updated recorded reason', self.core.chat('/decisions Unreal'))
        self.assertIn('No recorded decisions', self.core.chat('/decisions unavailable'))
        self.assertTrue(self.core.forget_decision(mid, 2))
        self.assertEqual(self.core.decisions(project='Game'), [])
        self.assertEqual(len(self.core.decisions()), 1)

    def test_stale_edit_or_delete_cannot_destroy_a_newer_decision(self):
        mid = self.core.save_decision('Game', 'Engine', 'Original reason')
        self.core.save_decision('Game', 'Engine', 'New reason', decision_id=mid, revision=1)
        with self.assertRaisesRegex(ValueError, 'changed or was removed'):
            self.core.save_decision('Game', 'Engine', 'Stale reason', decision_id=mid, revision=1)
        with self.assertRaisesRegex(ValueError, 'changed or was removed'):
            self.core.forget_decision(mid, 1)
        self.assertEqual(self.core.decisions()[0]['reason'], 'New reason')

    def test_policy_credentials_and_validation_precede_any_write(self):
        mid = self.core.save_decision('Game', 'Engine', 'Recorded reason')
        for mode in ('READ_ONLY', 'DRY_RUN', 'SAFE_MODE'):
            with self.assertRaises(ValueError): self.core.save_decision('Game', 'Engine', 'Reason', mode=mode)
            with self.assertRaises(ValueError): self.core.forget_decision(mid, 1, mode=mode)
        self.core.stop()
        with self.assertRaises(ValueError): self.core.save_decision('Game', 'Engine', 'Reason')
        with self.assertRaises(ValueError): self.core.forget_decision(mid, 1)
        self.assertEqual(len(self.core.decisions()), 1)
        self.core.resume()
        for values in (('', 'Choice', 'Reason'), ('x'*101, 'Choice', 'Reason'),
                       ('Game', 'Choice', 'password=synthetic-secret')):
            with self.assertRaises(ValueError): self.core.save_decision(*values)
        with self.assertRaises(ValueError): self.core.save_decision('Game', 'Choice', 'Reason', alternatives='api_key=synthetic-secret')
        with self.assertRaises(ValueError): self.core.decisions('x'*201)
        with self.assertRaises(ValueError): self.core.forget_decision(mid, True)
        events = json.dumps(self.core.events())
        self.assertNotIn('Recorded reason', events)
        self.assertNotIn('synthetic-secret', events)
        self.assertEqual(len(self.core.decisions()), 1)

    def test_existing_database_and_memory_survive_additive_migration(self):
        self.core.remember('language', 'Sinhala')
        self.core.close()
        with sqlite3.connect(self.path / 'nova.sqlite3') as db:
            db.execute('DROP TABLE decisions')
        self.core = NovaCore(self.path)
        self.assertEqual(self.core.memories()[0]['value'], 'Sinhala')
        self.core.save_decision('Project', 'Choice', 'Reason')
        self.assertEqual(len(self.core.decisions()), 1)


if __name__ == '__main__':
    unittest.main()
