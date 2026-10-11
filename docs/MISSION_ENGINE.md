# Mission engine

SQLite persists mission identity, tool, validated inputs, state, dependency and verified result. Three bounded workers execute registered tools. Prepared plans are schema-checked before enqueue; steps are sequential and failure blocks dependents. Idempotency keys reject conflicting reuses.

Emergency stop persists and pauses future dispatch; atomic work already running can finish. File creation is exclusive with hash verification and guarded rollback. Browser OS handoff remains unverified/BLOCKED. Dynamic replanning, distributed goals, overnight autonomy and arbitrary tool creation are not implemented.
