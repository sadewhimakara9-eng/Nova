import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import Mock

from nova.catalog import coverage, expansion_requirements, master_requirements
from nova.core import NovaCore
from scripts.sync_roadmap import traceability, master_traceability


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.core = NovaCore(Path(self.directory.name))

    def tearDown(self):
        self.core.close()
        self.directory.cleanup()

    def test_every_requirement_is_preserved_and_evidence_paths_exist(self):
        root = Path(__file__).resolve().parents[1]
        prompt = (root / 'docs/spec/NOVA_ADVANCED_EXPANSION.md').read_text()
        headings = re.findall(r'^# (\d+)\. (.+)$', prompt, re.M)
        rows = expansion_requirements()
        self.assertEqual(len(rows), 132)
        self.assertEqual([r['section'] for r in rows], list(range(1, 133)))
        self.assertEqual([r['title'] for r in rows], [title.title() for _, title in headings])
        for row in rows:
            for path in row['implementation'] + row['tests']:
                self.assertTrue((root / path).is_file(), (row['id'], path))
            if row['status'] == 'WORKING':
                self.assertTrue(row['implementation'] and row['tests'])
        self.assertEqual(sum(coverage().values()), 128)
        self.assertEqual((root / 'docs/EXPANSION_TRACEABILITY.md').read_text(), traceability(root))
        self.assertEqual((root / 'docs/REQUIREMENT_MATRIX.md').read_text(), master_traceability(root))
        master = master_requirements()
        self.assertEqual([r['section'] for r in master], list(range(136)))
        self.assertEqual(len(re.findall(r'^# \d+\. ', (root / 'docs/NOVA_MASTER_SPEC.md').read_text(), re.M)), len(master))
        for row in master:
            for path in row['implementation'] + row['tests']:
                self.assertTrue((root / path).is_file(), (row['id'], path))

    def test_search_filters_and_no_external_capabilities_become_executable(self):
        before = self.core.tools()
        rows = self.core.feature_catalog('WhatsApp')
        self.assertTrue(rows)
        inbox = next(r for r in rows if r['id'] == 'EXP-002')
        self.assertEqual(inbox['status'], 'NOT_STARTED')
        self.assertEqual(inbox['availability'], 'REFERENCE_ONLY')
        self.assertFalse(any(r['kind'] == 'tool' for r in rows))
        self.assertEqual(self.core.tools(), before)
        self.assertEqual(self.core.missions(), [])
        self.assertTrue(all(r['status'] == 'NOT_STARTED' for r in self.core.feature_catalog(status='NOT_STARTED')))
        self.assertEqual(self.core.feature_catalog('unknown-integration-xyz'), [])
        for args in ({'query': 'x'*201}, {'status': 'CONNECTED'}, {'mode': 'UNRESTRICTED'}):
            with self.assertRaises(ValueError): self.core.feature_catalog(**args)

    def test_actual_tool_availability_obeys_mode_and_stop(self):
        def entry(name, mode='LOCAL_ONLY'):
            return next(r for r in self.core.feature_catalog(mode=mode) if r['id'] == name)
        self.assertEqual(entry('files.create')['availability'], 'AVAILABLE')
        self.assertEqual(entry('files.create', 'READ_ONLY')['availability'], 'RESTRICTED')
        self.assertEqual(entry('files.read', 'READ_ONLY')['availability'], 'AVAILABLE')
        self.assertEqual(entry('files.read', 'DRY_RUN')['availability'], 'RESTRICTED')
        self.assertEqual(entry('provider.groq')['availability'], 'RESTRICTED')
        self.assertEqual(entry('provider.groq', 'NORMAL')['availability'], 'NOT_VERIFIED')
        self.core.stop()
        self.assertEqual(entry('files.read')['availability'], 'PAUSED')
        self.assertEqual(entry('EXP-017')['availability'], 'READ_ONLY')

    def test_local_search_needs_no_model_and_chat_does_not_leak_decisions(self):
        provider = Mock(provider='ollama')
        provider.complete.return_value = 'Mocked answer'
        self.core.save_decision('Secret project name', 'Use an engine', 'Unshared recorded reason')
        reply = self.core.chat('/capabilities video', provider)
        self.assertIn('NOT_STARTED', reply)
        provider.complete.assert_not_called()
        self.assertIn('No matching capability', self.core.chat('/capabilities unique-unknown-feature'))
        self.core.chat('Why did we choose that engine?', provider)
        sent = json.dumps(provider.complete.call_args.args[0])
        self.assertNotIn('Secret project name', sent)
        self.assertNotIn('Unshared recorded reason', sent)
        self.assertIn('/decisions', sent)
        self.assertIn('not installed', sent)


if __name__ == '__main__':
    unittest.main()
