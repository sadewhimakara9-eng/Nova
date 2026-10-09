"""Read-only view models and validated display preferences over the existing core."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

APPEARANCE_DEFAULTS = {"glass": 65, "transparency": 60, "blur": 16, "animation": True,
                       "orb_effects": True, "scale": 100, "performance": False}
PAGES = ("Home", "Chat", "Voice", "Missions", "Projects", "Agents", "Memory",
         "Automations", "Tools", "Integrations", "Devices", "Privacy", "Settings")
ORB_STATES = ("idle", "listening", "thinking", "speaking", "working", "success",
              "warning", "error", "privacy", "offline")
ACTIVE = {"RUNNING", "VERIFYING"}
WAITING = {"BLOCKED", "PAUSED", "WAITING_FOR_USER"}


def appearance_settings(values) -> dict:
    result = dict(APPEARANCE_DEFAULTS)
    if not isinstance(values, dict):
        return result
    for key in ("animation", "orb_effects", "performance"):
        if isinstance(values.get(key), bool):
            result[key] = values[key]
    for key, low, high in (("glass", 20, 90), ("transparency", 20, 90), ("blur", 0, 24), ("scale", 85, 120)):
        value = values.get(key)
        if type(value) in (int, float) and low <= value <= high:
            result[key] = int(value)
    return result


@dataclass(frozen=True)
class AssistantState:
    orb: str
    label: str
    running: int
    queued: int
    waiting: int


def assistant_state(missions, stopped=False, mode="LOCAL_ONLY") -> AssistantState:
    running = sum(m["status"] in ACTIVE for m in missions)
    queued = sum(m["status"] in {"QUEUED", "READY"} for m in missions)
    waiting = sum(m["status"] in WAITING for m in missions)
    if stopped:
        orb, label = "warning", "Automation paused"
    elif running:
        orb, label = "working", "Working on your missions"
    elif mode == "OFFLINE":
        orb, label = "offline", "Offline · local tools ready"
    elif mode in {"PRIVATE", "LOCAL_ONLY"}:
        orb, label = "privacy", "Ready · staying local"
    else:
        orb, label = "idle", "Ready when you are"
    return AssistantState(orb, label, running, queued, waiting)


def greeting(language="si", hour=None):
    if hour is None:
        try:
            hour = datetime.now(ZoneInfo("Asia/Colombo")).hour
        except ZoneInfoNotFoundError:
            hour = datetime.now().hour
    if language == "si":
        return "සුභ උදෑසනක්." if 5 <= hour < 12 else "සුභ දවසක්." if 12 <= hour < 17 else "සුභ සන්ධ්‍යාවක්."
    return "Good morning." if 5 <= hour < 12 else "Good afternoon." if 12 <= hour < 17 else "Good evening."


def mission_group(status):
    if status in ACTIVE:
        return "Running"
    if status in {"QUEUED", "READY"}:
        return "Queued"
    if status in WAITING or status == "FAILED":
        return "Waiting for You"
    return "Completed"


def elapsed_label(mission):
    try:
        start = datetime.fromisoformat(mission["created_at"])
        end = datetime.fromisoformat(mission["updated_at"]) if mission["status"] not in ACTIVE else datetime.now(start.tzinfo)
        seconds = max(0, int((end - start).total_seconds()))
        return f"{seconds // 60}m {seconds % 60}s" if seconds >= 60 else f"{seconds}s"
    except (KeyError, TypeError, ValueError):
        return "—"


class UIController:
    def __init__(self, core):
        self.core = core

    def appearance(self):
        try:
            raw = json.loads(self.core.store.setting("ui.appearance", "{}"))
        except (TypeError, ValueError):
            raw = {}
        return appearance_settings(raw)

    def save_appearance(self, values):
        settings = appearance_settings(values)
        self.core.store.set_setting("ui.appearance", json.dumps(settings))
        return settings

    def agents(self):
        missions = self.core.missions()
        output = []
        for agent in self.core.agents.agents:
            jobs = [m for m in missions if m["tool"] in agent.tools]
            complete = sum(m["status"] == "COMPLETED" for m in jobs)
            failed = sum(m["status"] == "FAILED" for m in jobs)
            active = next((m for m in jobs if m["status"] in ACTIVE), None)
            output.append({"id": agent.id, "name": agent.id.replace("-", " ").title(),
                           "tools": sorted(agent.tools), "active": active,
                           "completed": complete, "failed": failed,
                           "reliability": f"{round(100 * complete / (complete + failed))}%" if complete + failed else "Not measured yet"})
        return output

    def external_activity(self):
        # Historical core events only track successful model responses, not a
        # full request/byte ledger. Never manufacture a zero-egress guarantee.
        activity = []
        for event in self.core.events():
            if event["kind"] == "MODEL_RESPONSE":
                try:
                    metadata = json.loads(event["detail"])
                except (TypeError, ValueError):
                    continue
                if metadata.get("provider") == "groq":
                    activity.append(event)
        return activity
