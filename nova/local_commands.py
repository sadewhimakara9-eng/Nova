"""Local intent grammar extracts arbitrary app names before provider fallback."""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class LocalIntent:
    action: str
    target: str


def local_intent(text):
    value = re.sub(r"^nova[\s,]+", "", text.strip(), flags=re.I).strip().rstrip(".! ")
    value = re.sub(r"^please\s+", "", value, flags=re.I)
    patterns = (
        r"^(?:/open|open|launch|start)\s+(.+?)(?:\s+please)?$",
        r"^(.+?)(?:\s+eka)?\s+(?:open(?:\s+karanna)?|arinna|විවෘත කරන්න)$",
        r"^(.+?)\s+yanna$",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, value, re.I)
        if match:
            target = match[1].strip()
            if len(target) > 100 or not re.fullmatch(r"[\w .+()\-]+", target) or target.startswith("."):
                raise ValueError("Use an application name, not a path, URL, script or command arguments.")
            return LocalIntent("OPEN_APP", target)
    # Recognize unsupported local operations so they never become fabricated
    # model actions. These action classes can gain adapters incrementally.
    if re.match(r"^(close|focus|minimize|maximize)\s+", value, re.I):
        return LocalIntent("UNSUPPORTED_WINDOW_ACTION", value)
    return None
