"""Owner workflows exercise the actual local core, without live providers."""
from contextlib import ExitStack
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from streamlit import cache_resource
from streamlit.testing.v1 import AppTest
from nova.core import NovaCore


class ExpansionUITests(unittest.TestCase):
    def test_coverage_and_decision_lifecycle(self):
        with tempfile.TemporaryDirectory() as directory, ExitStack() as resources:
            resources.enter_context(patch.dict(os.environ, {'NOVA_DATA_DIR': directory}))
            network = resources.enter_context(patch('nova.providers.urllib.request.build_opener', side_effect=AssertionError('Unexpected network')))
            resources.callback(cache_resource.clear)

            def create_core(*args, **kwargs):
                core = NovaCore(*args, **kwargs)
                resources.callback(core.close)
                return core

            resources.enter_context(patch('nova.core.NovaCore', side_effect=create_core))
            app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'nova_app.py'), default_timeout=10).run()

            def element(group, label):
                return next(x for x in getattr(app, group) if x.label == label)

            def choose(label, value):
                next(x for x in app.get('button_group') if x.label == label).set_value(value).run()

            self.assertEqual(app.sidebar.radio[0].options, ['Chat', 'Voice', 'Projects', 'Memory', 'Settings'])
            app.sidebar.radio[0].set_value('Settings').run()
            element('button', 'Open Tools').click().run()
            choose('Tools view', 'Feature coverage')
            element('text_input', 'Search feature catalog').set_value('Blender').run()
            self.assertFalse(app.exception)
            self.assertTrue(any('3D Scene Optimizer' in x.label and 'NOT_STARTED' in x.label for x in app.expander))
            element('selectbox', 'Feature status').set_value('WORKING').run()
            element('selectbox', 'Catalog type').set_value('feature').run()
            self.assertFalse(any('EXP-' in x.label for x in app.expander))

            app.sidebar.radio[0].set_value('Projects').run()
            choose('Project view', 'Decision memory')
            element('text_input', 'Project label').set_value('Game')
            element('text_area', 'Decision').set_value('Unreal තෝරමු')
            element('text_area', 'Reason').set_value('Rendering tools')
            element('text_area', 'Alternatives considered (optional)').set_value('Godot')
            element('button', 'Save decision').click().run()
            self.assertFalse(app.exception)
            self.assertFalse(app.error)
            self.assertTrue(any('Unreal තෝරමු' in x.label for x in app.expander))
            element('text_area', 'Edit reason').set_value('Recorded updated reason')
            element('button', 'Save changes').click().run()
            self.assertFalse(app.exception)
            self.assertTrue(any('Recorded updated reason' in x.value for x in app.markdown))
            app.sidebar.radio[0].set_value('Settings').run()
            app.selectbox(key='widget_nova_mode').set_value('READ_ONLY').run()
            app.sidebar.radio[0].set_value('Projects').run()
            choose('Project view', 'Decision memory')
            self.assertTrue(element('button', 'Save decision').disabled)
            self.assertTrue(element('button', 'Save changes').disabled)
            app.sidebar.radio[0].set_value('Settings').run()
            app.selectbox(key='widget_nova_mode').set_value('LOCAL_ONLY').run()
            app.sidebar.radio[0].set_value('Projects').run()
            choose('Project view', 'Decision memory')
            self.assertTrue(element('button', 'Forget decision').disabled)
            element('checkbox', 'Delete this decision').check().run()
            element('button', 'Forget decision').click().run()
            self.assertFalse(app.exception)
            self.assertFalse(any('Unreal තෝරමු' in x.label for x in app.expander))
            network.assert_not_called()


if __name__ == '__main__':
    unittest.main()
