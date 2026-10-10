"""Windows OS APIs are mocked here; real Windows acceptance remains pending."""
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import Mock, patch

from nova.core import NovaCore
from nova.local_commands import local_intent
from nova.windows_apps import App, AppError, WindowsApps, resolve


class WindowsCommandTests(unittest.TestCase):
    def test_router_extracts_unlisted_names_and_mixed_language_without_model(self):
        for text, target in [('Nova, open Krita', 'Krita'), ('Chrome eka open karanna', 'Chrome'),
                             ('Calculator open karanna', 'Calculator'), ('Blender arinna', 'Blender'),
                             ('YouTube yanna', 'YouTube'), ('Nova Gemini විවෘත කරන්න', 'Gemini'),
                             ('please launch My Custom Editor', 'My Custom Editor')]:
            self.assertEqual(local_intent(text).target, target)
        self.assertIsNone(local_intent('Could you explain rendering?'))
        self.assertEqual(local_intent('close Chrome').action, 'UNSUPPORTED_WINDOW_ACTION')
        for text in ('open C:\\Windows\\cmd.exe', 'open chrome; shutdown', 'open https://evil.test', 'open app --run=x'):
            with self.assertRaises(ValueError): local_intent(text)

    def test_resolver_discovers_arbitrary_names_and_refuses_ambiguity(self):
        apps = [App('Krita', '/apps/krita.exe'), App('Custom Editor', '/apps/editor.exe'),
                App('Custom Editor Beta', '/apps/editor-beta.exe')]
        self.assertEqual(resolve('Krita', apps), apps[0])
        self.assertEqual(resolve('Google Chrome', [App('chrome', '/apps/chrome.exe', aliases=('Google Chrome',))]).name, 'chrome')
        self.assertEqual(resolve('Custom Editorr', apps), apps[1])
        with self.assertRaisesRegex(AppError, 'ambiguous'):
            resolve('Custom Editor', apps + [App('Custom Editor', '/other/editor.exe')])
        with self.assertRaisesRegex(AppError, 'No matching'):
            resolve('Uninstalled game engine', apps)

    def test_launch_success_needs_matching_visible_identity(self):
        adapter = WindowsApps(); adapter.platform = 'win32'
        app = App('Krita', '/apps/krita.exe')
        with patch.object(adapter, 'discover', return_value=[app]), patch.object(adapter, 'launch') as launch, patch.object(adapter, 'visible_windows', side_effect=[[], [('/apps/krita.exe', '', 'Canvas')]]):
            receipt = adapter.open('Krita')
            self.assertTrue(receipt['verified'])
            launch.assert_called_once_with(app)
        with patch.object(adapter, 'discover', return_value=[app]), patch.object(adapter, 'launch') as launch, patch.object(adapter, 'visible_windows', return_value=[('/apps/krita.exe', '', 'Canvas')]):
            self.assertEqual(adapter.open('Krita')['state'], 'ALREADY_VISIBLE')
            launch.assert_not_called()
        with patch.object(adapter, 'discover', return_value=[app]), patch.object(adapter, 'launch'), patch.object(adapter, 'visible_windows', return_value=[]), patch('nova.windows_apps.time.monotonic', side_effect=[0, 11]):
            with self.assertRaisesRegex(AppError, 'not verified'):
                adapter.open('Krita')

    def test_official_website_handoff_is_not_page_verification(self):
        adapter = WindowsApps(); adapter.platform = 'win32'
        with patch.object(adapter, 'discover', return_value=[]), patch('nova.windows_apps.os.startfile', create=True) as start:
            result = adapter.open_site('Gemini')
            self.assertFalse(result['verified'])
            start.assert_called_once_with('https://gemini.google.com/')
            with self.assertRaises(AppError): adapter.open_site('https://other.test')

    def test_shell_targets_are_not_eligible(self):
        with tempfile.TemporaryDirectory() as directory:
            for name in ('cmd.exe', 'python.exe', 'powershell.exe', 'mshta.exe'):
                path = Path(directory) / name; path.touch()
                self.assertFalse(WindowsApps.safe_candidate(App('Friendly Name', str(path))))
        self.assertFalse(WindowsApps.safe_candidate(App('Remote', r'\\server\share\app.exe')))
        self.assertFalse(WindowsApps.safe_candidate(App('Injected', 'bad;command', 'package')))

    def test_linux_local_request_does_not_call_selected_provider(self):
        with tempfile.TemporaryDirectory() as directory:
            core = NovaCore(Path(directory))
            try:
                provider = Mock()
                if 'apps.open' not in {t['name'] for t in core.tools()}:
                    self.assertIn('unavailable', core.chat('Gemini eka open karanna', provider))
                    provider.complete.assert_not_called()
            finally: core.close()

    def test_windows_policy_and_browser_receipt_are_honest(self):
        with tempfile.TemporaryDirectory() as directory, patch('nova.tools.sys.platform', 'win32'), patch('nova.agents.sys.platform', 'win32'):
            core = NovaCore(Path(directory))
            try:
                for mode in ('OFFLINE', 'LOCAL_ONLY', 'PRIVATE', 'READ_ONLY', 'DRY_RUN', 'SAFE_MODE'):
                    with self.assertRaises(ValueError): core.enqueue('web.open', {'site': 'gemini'}, mode=mode)
                with self.assertRaises(ValueError):
                    core.submit_plan([{'tool':'files.create','args':{'path':'partial.txt','content':'test'},'goal':'Note'},
                                      {'tool':'web.open','args':{'site':'gemini'},'goal':'Open site'}])
                self.assertEqual(core.missions(), [])
                with patch('nova.windows_apps.WindowsApps.open_site', return_value={'verified':False,'verification':'OS_HANDOFF_ONLY','state':'CHECK_BROWSER'}):
                    mid = core.enqueue('web.open', {'site':'gemini'}, mode='NORMAL')
                    deadline=time.monotonic()+3
                    while time.monotonic()<deadline:
                        row=next(m for m in core.missions() if m['id']==mid)
                        if row['status'] in {'BLOCKED','FAILED','COMPLETED'}: break
                        time.sleep(.02)
                    self.assertEqual(row['status'], 'BLOCKED')
                    self.assertFalse(row['result']['verified'])
            finally: core.close()


if __name__ == '__main__': unittest.main()
