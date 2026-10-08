"""Real temporary SQLite/filesystem tests; model responses and concurrency tools are mocked."""

import json
import os
import tempfile
import threading
import time
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import Mock

from nova.core import NovaCore, NovaError, TERMINAL
from nova.tools import ToolError


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="nova-test-")
        self.data = Path(self.temp.name) / "data"
        self.workspace = Path(self.temp.name) / "workspace"
        self.core = NovaCore(self.data, self.workspace)

    def tearDown(self):
        self.core.close()
        self.temp.cleanup()

    def reopen(self):
        self.core.close()
        self.core = NovaCore(self.data, self.workspace)

    def mission(self, mid):
        return next(row for row in self.core.missions() if row["id"] == mid)

    def wait_mission(self, mid, status=None):
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            row = self.mission(mid)
            if row["status"] in TERMINAL or row["status"] == status:
                if status:
                    self.assertEqual(row["status"], status, row)
                return row
            threading.Event().wait(0.02)
        self.fail(f"Mission {mid} did not finish: {self.mission(mid)['status']}")

    def test_local_commands_and_explicit_memory_survive_restart(self):
        provider = Mock()
        self.assertIn("ආයුබෝවන්", self.core.chat("hi", provider=provider, mode="OFFLINE"))
        self.core.chat("/remember language = Sinhala", provider=provider, mode="OFFLINE")
        provider.complete.assert_not_called()
        original = self.core.memories()[0]
        self.core.remember("language", "English", source="inferred", confidence=0.4)
        self.assertEqual(self.core.memories()[0]["value"], "Sinhala")
        self.reopen()
        self.assertEqual(self.core.memories()[0]["id"], original["id"])
        self.assertIn("Sinhala", self.core.chat("/recall language"))
        self.core.remember("language", "English", source="explicit")
        self.assertEqual(self.core.memories()[0]["value"], "English")
        self.assertTrue(self.core.forget(original["id"]))
        self.assertEqual(self.core.memories(), [])

    def test_create_read_and_verified_rollback(self):
        mid = self.core.enqueue("files.create", {"path": "notes/hello.txt", "content": "ආයුබෝවන්"})
        created = self.wait_mission(mid, "COMPLETED")
        self.assertTrue(created["result"]["verified"])
        read = self.core.enqueue("files.read", {"path": "notes/hello.txt"})
        self.assertEqual(self.wait_mission(read, "COMPLETED")["result"]["content"], "ආයුබෝවන්")
        self.core.undo(mid)
        self.assertFalse((self.workspace / "notes/hello.txt").exists())
        self.assertEqual((self.data / "trash" / mid).read_text(), "ආයුබෝවන්")
        self.assertEqual(self.mission(mid)["status"], "ROLLED_BACK")

    def test_rollback_preserves_user_edits(self):
        mid = self.core.enqueue("files.create", {"path": "note.txt", "content": "original"})
        self.wait_mission(mid, "COMPLETED")
        path = self.workspace / "note.txt"
        path.write_text("owner's revision")
        with self.assertRaisesRegex(NovaError, "preserve your edits"):
            self.core.undo(mid)
        self.assertEqual(path.read_text(), "owner's revision")
        self.assertEqual(self.mission(mid)["status"], "COMPLETED")

    def test_never_overwrites_existing_files(self):
        (self.workspace / "existing.txt").write_text("owned")
        mid = self.core.enqueue("files.create", {"path": "existing.txt", "content": "replacement"})
        self.wait_mission(mid, "FAILED")
        self.assertEqual((self.workspace / "existing.txt").read_text(), "owned")

    def test_traversal_absolute_hidden_and_windows_paths_are_rejected(self):
        paths = ("../outside.txt", "a/../../outside.txt", "/tmp/outside.txt", "C:\\outside.txt",
                 "..\\outside.txt", ".hidden", "a/.hidden/file", "a//b", "NUL", "name:stream")
        for path in paths:
            with self.subTest(path=path), self.assertRaises(ToolError):
                self.core.enqueue("files.create", {"path": path, "content": "test"})
        self.assertEqual(self.core.missions(), [])

    def test_symlink_file_and_parent_are_rejected(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (outside / "secret.txt").write_text("outside content")
        try:
            (self.workspace / "linked").symlink_to(outside, target_is_directory=True)
            (self.workspace / "link.txt").symlink_to(outside / "secret.txt")
        except (OSError, NotImplementedError):
            self.skipTest("Symbolic links unavailable for this account")
        for path in ("linked/secret.txt", "link.txt"):
            with self.subTest(path=path), self.assertRaises(ToolError):
                self.core.enqueue("files.read", {"path": path})
        with self.assertRaises(ToolError):
            self.core.enqueue("files.create", {"path": "linked/new.txt", "content": "test"})
        self.assertFalse((outside / "new.txt").exists())

    def test_hardlinked_files_are_not_read(self):
        outside = Path(self.temp.name) / "outside.txt"
        outside.write_text("outside content")
        try:
            os.link(outside, self.workspace / "linked.txt")
        except OSError:
            self.skipTest("Hard links unavailable")
        mid = self.core.enqueue("files.read", {"path": "linked.txt"})
        self.wait_mission(mid, "FAILED")

    def test_unknown_tool_and_model_injected_actions_are_rejected(self):
        with self.assertRaises(ToolError):
            self.core.enqueue("shell.execute", {"command": "whoami"})
        provider = Mock()
        provider.complete.return_value = json.dumps([
            {"tool": "shell.execute", "args": {"command": "whoami"}, "goal": "Ignore restrictions"},
        ])
        with self.assertRaises(ToolError):
            self.core.plan("Do something", provider)
        provider.complete.return_value = json.dumps([
            {"tool": "files.read", "args": {"path": "../outside.txt"}, "goal": "Read outside"},
        ])
        with self.assertRaises(ToolError):
            self.core.plan("Do something", provider)
        self.assertEqual(self.core.missions(), [])

    def test_plan_validation_is_atomic_before_any_submission(self):
        steps = [
            {"tool": "files.create", "args": {"path": "good.txt", "content": "good"}, "goal": "Create note"},
            {"tool": "shell.execute", "args": {}, "goal": "Invalid action"},
        ]
        with self.assertRaises(ToolError):
            self.core.submit_plan(steps)
        self.assertEqual(self.core.missions(), [])
        self.assertFalse((self.workspace / "good.txt").exists())

    def test_stopped_queue_and_stop_setting_survive_restart(self):
        self.core.stop()
        mid = self.core.enqueue("files.create", {"path": "paused.txt", "content": "later"})
        self.assertEqual(self.mission(mid)["status"], "PAUSED")
        self.reopen()
        self.assertTrue(self.core.stopped)
        self.assertEqual(self.mission(mid)["status"], "PAUSED")
        self.assertFalse((self.workspace / "paused.txt").exists())
        self.core.resume()
        self.wait_mission(mid, "COMPLETED")
        self.assertFalse(self.core.stopped)

    def test_interrupted_read_recovers_but_write_is_blocked(self):
        self.core.stop()
        read = self.core.enqueue("files.list", {})
        write = self.core.enqueue("files.create", {"path": "uncertain.txt", "content": "do not retry"})
        with self.core.store.connect() as db:
            db.execute("UPDATE missions SET status='RUNNING' WHERE id=?", (read,))
            db.execute("UPDATE missions SET status='VERIFYING' WHERE id=?", (write,))
        self.reopen()
        self.assertEqual(self.mission(read)["status"], "QUEUED")
        self.assertEqual(self.mission(write)["status"], "BLOCKED")
        self.core.resume()
        self.wait_mission(read, "COMPLETED")
        self.assertFalse((self.workspace / "uncertain.txt").exists())

    def test_failure_isolation_and_failed_dependencies(self):
        missing = self.core.enqueue("files.read", {"path": "missing.txt"})
        dependent = self.core.enqueue("files.create", {"path": "dependent.txt", "content": "blocked"}, dependency=missing)
        independent = self.core.enqueue("system.info", {})
        self.wait_mission(missing, "FAILED")
        self.wait_mission(dependent, "BLOCKED")
        self.wait_mission(independent, "COMPLETED")
        self.assertFalse((self.workspace / "dependent.txt").exists())

    def test_request_idempotency_and_mismatch_rejection(self):
        self.core.stop()
        args = {"path": "once.txt", "content": "one action"}
        first = self.core.enqueue("files.create", args, idempotency_key="request-123")
        self.assertEqual(first, self.core.enqueue("files.create", args, idempotency_key="request-123"))
        with self.assertRaises(NovaError):
            self.core.enqueue("files.list", {}, idempotency_key="request-123")
        self.assertEqual(len(self.core.missions()), 1)
        self.core.resume()
        self.wait_mission(first, "COMPLETED")
        self.reopen()
        self.assertEqual(first, self.core.enqueue("files.create", args, idempotency_key="request-123"))
        self.assertEqual(len(self.core.missions()), 1)

    def test_offline_local_file_work_needs_no_model(self):
        self.core.chat("/write offline.txt | local work", mode="OFFLINE")
        mid = self.core.missions()[0]["id"]
        self.wait_mission(mid, "COMPLETED")
        self.assertEqual((self.workspace / "offline.txt").read_text(), "local work")

    def test_read_only_and_dry_run_do_not_mutate_files_or_memory(self):
        for mode in ("READ_ONLY", "DRY_RUN", "SAFE_MODE"):
            with self.subTest(mode=mode):
                with self.assertRaises(NovaError):
                    self.core.chat("/write blocked.txt | content", mode=mode)
                with self.assertRaises(NovaError):
                    self.core.chat("/remember language = Sinhala", mode=mode)
        self.assertEqual(self.core.memories(), [])
        self.assertFalse((self.workspace / "blocked.txt").exists())
        read = self.core.enqueue("files.list", {}, mode="READ_ONLY")
        self.wait_mission(read, "COMPLETED")
        with self.assertRaises(NovaError):
            self.core.enqueue("files.list", {}, mode="DRY_RUN")

    def test_credential_inputs_and_external_file_results_never_reach_database(self):
        secret = "gsk_" + "A" * 40
        with self.assertRaises(NovaError):
            self.core.chat(secret)
        with self.assertRaises(NovaError):
            self.core.remember("credential", secret)
        with self.assertRaises(NovaError):
            self.core.enqueue("files.create", {"path": "unsafe.txt", "content": secret})
        (self.workspace / "external.txt").write_text(secret)
        mid = self.core.enqueue("files.read", {"path": "external.txt"})
        self.wait_mission(mid, "FAILED")
        with self.core.store.connect() as db:
            dump = "\n".join(db.iterdump())
        self.assertNotIn(secret, dump)
        self.assertNotIn(secret, json.dumps(self.core.events()))

    def test_credential_request_ids_are_rejected_before_persistence(self):
        secret = "gsk_" + "B" * 40
        with self.assertRaises((NovaError, ToolError)):
            self.core.enqueue("files.list", {}, idempotency_key=secret)
        with self.core.store.connect() as db:
            self.assertNotIn(secret, "\n".join(db.iterdump()))

    def test_unexpected_tool_errors_do_not_leak_content(self):
        secret = "gsk_" + "C" * 40
        def fail(args, mid):
            raise RuntimeError(secret)
        original = self.core.registry._tools["system.info"]
        self.core.registry._tools["system.info"] = replace(original, execute=fail)
        mid = self.core.enqueue("system.info", {})
        row = self.wait_mission(mid, "FAILED")
        self.assertNotIn(secret, row["error"])
        self.assertNotIn(secret, json.dumps(self.core.events()))

    def test_independent_missions_execute_concurrently_with_finite_barrier(self):
        barrier = threading.Barrier(2, timeout=3)
        seen = []
        lock = threading.Lock()
        def rendezvous(args, mid):
            with lock:
                seen.append(mid)
            barrier.wait()
            return {"verified": True, "concurrent": True}
        original = self.core.registry._tools["system.info"]
        self.core.registry._tools["system.info"] = replace(original, execute=rendezvous)
        self.core.stop()
        first = self.core.enqueue("system.info", {})
        second = self.core.enqueue("system.info", {})
        self.core.resume()
        self.wait_mission(first, "COMPLETED")
        self.wait_mission(second, "COMPLETED")
        self.assertCountEqual(seen, [first, second])

    def test_second_scheduler_for_same_database_is_rejected(self):
        with self.assertRaisesRegex(NovaError, "already running"):
            NovaCore(self.data, self.workspace)


if __name__ == "__main__":
    unittest.main()
