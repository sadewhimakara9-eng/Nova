"""Capabilities are derived from installed tools, never from example phrases."""
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Capability:
    capability_id: str
    name: str
    description: str
    category: str
    supported_inputs: dict
    supported_outputs: tuple[str, ...]
    required_tools: tuple[str, ...]
    required_agents: tuple[str, ...]
    required_integrations: tuple[str, ...]
    required_permissions: tuple[str, ...]
    privacy_level: str
    risk_level: str
    estimated_cost: str
    estimated_latency: str
    verification_method: str
    reliability_score: float | None
    status: str
    version: str


class CapabilityRegistry:
    def __init__(self, tools, agents):
        self.tools = tools
        self.agents = agents

    def describe(self, missions=()) -> list[dict]:
        records = []
        outputs = {"files.list": ("file_paths",), "files.read": ("utf8_text", "sha256"),
                   "files.create": ("file_path", "sha256", "byte_count"),
                   "system.info": ("operating_system", "python_version")}
        verification = {"files.list": "Bounded workspace enumeration",
                        "files.read": "Regular-file validation, UTF-8 decoding, SHA-256",
                        "files.create": "Exclusive creation followed by read-back SHA-256 comparison",
                        "system.info": "Read Python platform runtime information"}
        for descriptor in self.tools.descriptions():
            name = descriptor["name"]
            # A tool is not executable without a specialist authorized for it.
            try:
                agent = self.agents.for_tool(name)
            except ValueError:
                continue
            tool = self.tools._tools[name]
            finished = [m for m in missions if m["tool"] == name and m["status"] in {"COMPLETED", "FAILED"}]
            reliability = sum(m["status"] == "COMPLETED" for m in finished) / len(finished) if finished else None
            capability = Capability(
                capability_id=name, name=name.replace(".", " ").title(), description=descriptor["description"],
                category=name.split(".", 1)[0],
                supported_inputs={"type": "object", "properties": {field: {"type": "string"} for field in tool.fields},
                                  "required": list(tool.fields), "additionalProperties": False},
                supported_outputs=outputs.get(name, ("verified_result",)), required_tools=(name,),
                required_agents=(agent.id,), required_integrations=(),
                required_permissions=("workspace.create" if tool.mutating else "workspace.read",) if name.startswith("files.") else ("system.info",),
                privacy_level="LOCAL", risk_level="INTERNAL_REVERSIBLE" if tool.mutating else "READ_ONLY",
                estimated_cost="No external service charge", estimated_latency="Not benchmarked",
                verification_method=verification.get(name, "Tool-specific result verification"),
                reliability_score=reliability, status="WORKING", version="1.0",
            )
            records.append(asdict(capability))
        return records
