import tempfile
import unittest
from pathlib import Path

from nova.agents import AgentRegistry
from nova.storage import Store
from nova.tools import ToolError, ToolRegistry


class FoundationTests(unittest.TestCase):
    def test_specialists_cannot_use_another_agents_tools(self):
        with tempfile.TemporaryDirectory() as directory:
            registry = ToolRegistry(Path(directory))
            agents = AgentRegistry()
            file_agent = agents.for_tool("files.create")
            with self.assertRaises(ToolError):
                file_agent.run(registry, "system.info", {}, "mission")
            result = agents.for_tool("system.info").run(registry, "system.info", {}, "mission")
            self.assertTrue(result["verified"])

    def test_durable_events_survive_bad_subscriber_and_unsubscribe(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Store(Path(directory) / "events.sqlite3")
            received = []
            def broken(event):
                raise RuntimeError("broken observer")
            store.subscribe(broken)
            unsubscribe = store.subscribe(received.append)
            store.event("MISSION_COMPLETED", "mission", tool="files.create")
            unsubscribe()
            store.event("MISSION_COMPLETED", "second")
            self.assertEqual(len(received), 1)
            self.assertEqual(len(store.rows("SELECT * FROM events")), 2)
            self.assertEqual(received[0]["mission_id"], "mission")


if __name__ == "__main__":
    unittest.main()
