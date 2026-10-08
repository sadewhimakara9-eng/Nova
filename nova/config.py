"""Small, platform-aware configuration with no credentials on disk."""

import os
from pathlib import Path


def data_directory() -> Path:
    configured = os.environ.get("NOVA_DATA_DIR")
    if configured:
        return Path(configured).expanduser().resolve()
    base = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".local" / "share"))
    return base / "NovaAgent"


MAX_TEXT = 20_000
MAX_FILE_BYTES = 1_000_000
MAX_PLAN_STEPS = 8
WORKERS = 3
