"""Transactional local state. Event history deliberately omits user content."""

import json
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Store:
    def __init__(self, path: Path):
        self.path = path
        self.lock = threading.RLock()
        self._subscribers = []
        path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.executescript("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY, value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS missions (
                    id TEXT PRIMARY KEY, goal TEXT NOT NULL, tool TEXT NOT NULL,
                    args TEXT NOT NULL, status TEXT NOT NULL, result TEXT,
                    error TEXT, dependency TEXT, idempotency_key TEXT UNIQUE,
                    created_at TEXT NOT NULL, updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY, key TEXT NOT NULL, value TEXT NOT NULL,
                    scope TEXT NOT NULL, source TEXT NOT NULL,
                    confidence REAL NOT NULL, updated_at TEXT NOT NULL,
                    UNIQUE(key, scope)
                );
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kind TEXT NOT NULL, mission_id TEXT,
                    detail TEXT NOT NULL, created_at TEXT NOT NULL
                );
            """)

    @contextmanager
    def connect(self):
        with self.lock:
            db = sqlite3.connect(self.path, timeout=10)
            db.row_factory = sqlite3.Row
            try:
                with db:
                    yield db
            finally:
                db.close()

    def event(self, kind: str, mission_id: str | None = None, **metadata):
        # Callers supply fixed labels and numeric counts, never prompt/file content.
        with self.connect() as db:
            db.execute("INSERT INTO events(kind,mission_id,detail,created_at) VALUES(?,?,?,?)",
                       (kind, mission_id, json.dumps(metadata), now()))
        # Observers cannot veto persisted state or take down a worker. This is
        # in-process notification; durable state remains the source of truth.
        for callback in tuple(self._subscribers):
            try:
                callback({"kind": kind, "mission_id": mission_id, "detail": dict(metadata)})
            except Exception:
                continue

    def subscribe(self, callback):
        """Register a trusted in-process observer; return an unsubscribe function."""
        with self.lock:
            self._subscribers.append(callback)

        def unsubscribe():
            with self.lock:
                if callback in self._subscribers:
                    self._subscribers.remove(callback)
        return unsubscribe

    def setting(self, key: str, default: str = "") -> str:
        with self.connect() as db:
            row = db.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
            return row[0] if row else default

    def set_setting(self, key: str, value: str):
        with self.connect() as db:
            db.execute("INSERT INTO settings VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                       (key, value))

    def rows(self, query: str, values=()) -> list[dict]:
        with self.connect() as db:
            return [dict(row) for row in db.execute(query, values)]
