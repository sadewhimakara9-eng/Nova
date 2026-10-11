# Memory model

Memory is explicit local SQLite data. Owner preferences have precedence over inferred writes. Decisions store project, decision, reason, alternatives, timestamps and revision; edits/deletes reject stale revisions. Search is literal Unicode-aware text search.

Saved memory/decisions are not automatically model context. Deletion is logical, not forensic erasure; SQLite and backups are unencrypted. No vector index, automatic consolidation, visual memory or world model is installed. Credentials belong only in provider setup.
