"""Small specialist workers with explicit tool scopes, coordinated by the core."""

from dataclasses import dataclass
from typing import Protocol
import sys

from .tools import ToolError, ToolRegistry


class Agent(Protocol):
    id: str
    tools: frozenset[str]

    def run(self, registry: ToolRegistry, tool: str, args: dict, mission_id: str) -> dict: ...


@dataclass(frozen=True)
class ScopedAgent:
    id: str
    tools: frozenset[str]

    def run(self, registry: ToolRegistry, tool: str, args: dict, mission_id: str) -> dict:
        if tool not in self.tools:
            raise ToolError("This agent does not have permission to use that tool.")
        return registry.validate(tool, args).execute(args, mission_id)


class AgentRegistry:
    def __init__(self):
        self.agents = (
            ScopedAgent("file-agent", frozenset({"files.list", "files.read", "files.create"})),
            ScopedAgent("system-agent", frozenset({"system.info"})),
        )
        if sys.platform == "win32":
            self.agents += (ScopedAgent("desktop-agent", frozenset({"apps.open", "web.open"})),)

    def for_tool(self, tool: str) -> Agent:
        for agent in self.agents:
            if tool in agent.tools:
                return agent
        raise ToolError("No installed agent has permission to use that tool.")
