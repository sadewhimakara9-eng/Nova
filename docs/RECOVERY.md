# Recovery

A process lock prevents two schedulers from owning one data folder. Startup requeues interrupted files.list/files.read/system.info missions only. Interrupted writes/app actions become BLOCKED for inspection because a side effect may already have happened. Persisted stop remains active after restart.

Rollback deletes only unchanged files created by the mission; user edits are preserved. Before a manual backup, stop NOVA and copy the entire data folder. Automatic backup/restore, distributed recovery and restore drills are not implemented.
