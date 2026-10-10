"""Explicit project decisions, never inferred or silently sent to a model."""
import uuid

from .storage import now


class DecisionMemory:
    def __init__(self, store, validate_text):
        self.store = store
        self.validate_text = validate_text

    def save(self, project, decision, reason, alternatives="", *, decision_id=None, revision=None):
        values = [self.validate_text(value, label) for value, label in
                  ((project, "Project"), (decision, "Decision"), (reason, "Reason"))]
        if len(values[0]) > 100:
            raise ValueError("Project labels must be at most 100 characters.")
        if not isinstance(alternatives, str):
            raise ValueError("Alternatives must be text.")
        alternatives = self.validate_text(alternatives, "Alternatives") if alternatives.strip() else ""
        timestamp = now()
        with self.store.connect() as db:
            if decision_id is None:
                decision_id = uuid.uuid4().hex
                db.execute("INSERT INTO decisions VALUES(?,?,?,?,?,?,?,?)",
                           (decision_id, *values, alternatives, 1, timestamp, timestamp))
            else:
                self._revision(revision)
                changed = db.execute(
                    "UPDATE decisions SET project=?,decision=?,reason=?,alternatives=?,revision=revision+1,updated_at=? "
                    "WHERE id=? AND revision=?", (*values, alternatives, timestamp, decision_id, revision)).rowcount
                if not changed:
                    raise ValueError("This decision changed or was removed. Refresh before editing it.")
        self.store.event("DECISION_SAVED", count=1)
        return decision_id

    @staticmethod
    def _revision(revision):
        if type(revision) is not int or revision < 1:
            raise ValueError("Use the current decision revision.")

    def search(self, query="", project=""):
        if any(not isinstance(value, str) or len(value) > 200 for value in (query, project)):
            raise ValueError("Decision searches must be at most 200 characters.")
        # Fetch in batches so Unicode matching does not depend on SQLite's
        # ASCII-only LOWER(), and no unbounded result list is allocated.
        results = []
        with self.store.connect() as db:
            cursor = db.execute("SELECT * FROM decisions ORDER BY updated_at DESC, id")
            for row in cursor:
                if project and project.strip().casefold() != row["project"].casefold():
                    continue
                content = " ".join(row[key] for key in ("project", "decision", "reason", "alternatives"))
                if query.strip().casefold() in content.casefold():
                    results.append(dict(row))
                    if len(results) == 100:
                        break
        return results

    def delete(self, decision_id, revision):
        self._revision(revision)
        with self.store.connect() as db:
            changed = db.execute("DELETE FROM decisions WHERE id=? AND revision=?", (decision_id, revision)).rowcount
            if not changed:
                raise ValueError("This decision changed or was removed. Refresh before deleting it.")
        self.store.event("DECISION_FORGOTTEN", count=1)
        return True
