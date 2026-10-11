"""Read-only discovery; roadmap entries never grant executable permissions."""
from collections import Counter
from functools import lru_cache
import json
from pathlib import Path
import re


STATUSES = ("NOT_STARTED", "DESIGNING", "IMPLEMENTING", "PARTIAL", "EXPERIMENTAL",
            "WORKING", "STABLE", "BLOCKED", "DISABLED", "DEPRECATED")


@lru_cache(maxsize=1)
def expansion_requirements():
    rows = json.loads(Path(__file__).with_name("feature_catalog.json").read_text(encoding="utf-8"))
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError("Duplicate requirement IDs in the feature catalog.")
    for row in rows:
        if row["status"] not in STATUSES:
            raise ValueError("Unknown feature status in the catalog.")
    return rows


@lru_cache(maxsize=1)
def master_requirements():
    return json.loads(Path(__file__).with_name('omega_requirements.json').read_text(encoding='utf-8'))


def catalog(core, query="", status="ALL", mode="LOCAL_ONLY"):
    if not isinstance(query, str) or len(query) > 200:
        raise ValueError("Capability search must be at most 200 characters.")
    if status != "ALL" and status not in STATUSES:
        raise ValueError("Unknown feature status.")
    core._policy(mode)
    rows = []
    for capability in core.capabilities():
        restricted = (core.stopped or mode == "DRY_RUN" or
                      capability['capability_id'] == 'web.open' and mode != 'NORMAL' or
                      mode in {"READ_ONLY", "SAFE_MODE"} and capability["risk_level"] != "READ_ONLY")
        rows.append(dict(id=capability["capability_id"], title=capability["name"], category="Installed tools",
                         kind="tool", status=capability["status"], scope=capability["description"],
                         availability="PAUSED" if core.stopped else "RESTRICTED" if restricted else "AVAILABLE",
                         dependencies=list(capability["required_permissions"]),
                         implementation=["nova/tools.py", "nova/agents.py"] + (["nova/windows_apps.py"] if capability['status'] == 'EXPERIMENTAL' else []),
                         tests=["tests/test_windows_apps.py"] if capability['status'] == 'EXPERIMENTAL' else ["tests/test_core.py"],
                         release="0.3.0" if capability['status'] == 'EXPERIMENTAL' else "0.1.0", source="Installed runtime registry", phase="Installed",
                         requirements=capability["verification_method"]))
    for agent in core.agents.agents:
        rows.append(dict(id=agent.id, title=agent.id.replace("-", " ").title(), category="Installed agents",
                         kind="agent", status="EXPERIMENTAL" if agent.id == 'desktop-agent' else "WORKING", scope="Scoped worker for " + ", ".join(sorted(agent.tools)),
                         availability="PAUSED" if core.stopped else "MODE_GATED", dependencies=sorted(agent.tools),
                         implementation=["nova/agents.py"], tests=["tests/test_foundation.py"],
                         release="0.3.0" if agent.id == 'desktop-agent' else "0.1.0", source="Installed agent registry", phase="Installed", requirements=""))
    for provider in ("Ollama", "Groq", "OpenAI", "Gemini"):
        rows.append(dict(id="provider." + provider.lower(), title=provider + " model adapter", category="Providers",
                         kind="provider", status="PARTIAL", scope="Adapter implemented; a running model or authorized key is required. Connection has not been checked by this catalog.",
                         availability="RESTRICTED" if provider != "Ollama" and mode != "NORMAL" else "NOT_VERIFIED",
                         dependencies=["Running local model" if provider == "Ollama" else "Owner key, NORMAL mode, PUBLIC or INTERNAL request"],
                         implementation=["nova/providers.py"], tests=["tests/test_providers.py"], release="0.1.0",
                         source="Provider adapter implementation", phase="Installed", requirements="No automatic fallback or connection probing."))
    for source in (*expansion_requirements(), *master_requirements()):
        row = dict(source)
        row["availability"] = "REFERENCE_ONLY"
        if row["id"] == "EXP-017":
            row["availability"] = "READ_ONLY" if core.stopped or mode in {"READ_ONLY", "DRY_RUN", "SAFE_MODE"} else "AVAILABLE_IN_UI"
        elif row["id"] in {"EXP-019", "EXP-020", "EXP-021", "EXP-022"}:
            row["availability"] = "AVAILABLE_IN_UI"
        rows.append(row)
    # Literal, Unicode-aware discovery. No model, network, shell or database
    # writes. Every search term must occur; punctuation is not a query language.
    terms = re.findall(r"[\w]+", query.casefold())
    selected = []
    for row in rows:
        haystack = " ".join(str(row[key]) for key in ("id", "title", "category", "scope", "requirements", "dependencies")).casefold()
        if (status == "ALL" or row["status"] == status) and all(term in haystack for term in terms):
            selected.append(row)
    return selected


def coverage():
    """Count runtime-feature requirements only; governance is not a feature."""
    return dict(Counter(row["status"] for row in expansion_requirements() if row["kind"] == "feature"))


def capability_answer(core, query="", mode="LOCAL_ONLY"):
    rows = catalog(core, query, mode=mode)
    if not rows:
        return "No matching capability is recorded. This does not establish support. Search Tools → Feature coverage or prepare a mission for a capability-gap check."
    answer = ["Catalog evidence; provider connections and external hardware have not been verified:"]
    for row in rows[:12]:
        answer.append(f"• {row['title']} [{row['status']} · {row['availability']}]: {row['scope']}")
    if len(rows) > 12:
        answer.append(f"Showing 12 of {len(rows)} matches. Narrow the search in Tools → Feature coverage.")
    return "\n".join(answer)
