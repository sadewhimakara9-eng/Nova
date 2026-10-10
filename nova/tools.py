"""Allowlisted tools. No shell, arbitrary network requests, or plugin execution."""

import hashlib
import os
import platform
import stat
import sys
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import Callable

from .config import MAX_FILE_BYTES, MAX_TEXT


class ToolError(ValueError):
    """Safe, user-facing tool failure."""


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    fields: tuple[str, ...]
    mutating: bool
    execute: Callable


class ToolRegistry:
    def __init__(self, workspace: Path):
        self.workspace = workspace.resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self._tools = {
            "files.list": Tool("files.list", "List files in the Nova workspace. args: {}", (), False, self.list_files),
            "files.read": Tool("files.read", "Read a UTF-8 file. args: {path}", ("path",), False, self.read_file),
            "files.create": Tool("files.create", "Create a new UTF-8 file, never overwrite. args: {path, content}", ("path", "content"), True, self.create_file),
            "system.info": Tool("system.info", "Read OS and Python version. args: {}", (), False, self.system_info),
        }
        if sys.platform == "win32":
            self._tools.update({
                "apps.open": Tool("apps.open", "Open a discovered Windows app by name; verify a visible window. args: {name}", ("name",), True, self.open_app),
                "web.open": Tool("web.open", "Open Gemini or YouTube via installed app or official browser destination. Browser page loading requires owner verification. args: {site}", ("site",), True, self.open_site),
            })

    def open_app(self, args, mission_id):
        from .windows_apps import AppError, WindowsApps
        try:
            return WindowsApps().open(args["name"])
        except AppError as exc:
            raise ToolError(str(exc)) from None

    def open_site(self, args, mission_id):
        from .windows_apps import AppError, WindowsApps
        try:
            return WindowsApps().open_site(args["site"])
        except AppError as exc:
            raise ToolError(str(exc)) from None

    def descriptions(self) -> list[dict]:
        return [{"name": t.name, "description": t.description, "mutating": t.mutating} for t in self._tools.values()]

    def validate(self, name: str, args: dict) -> Tool:
        if name not in self._tools:
            raise ToolError("This tool is not installed or permitted.")
        tool = self._tools[name]
        if not isinstance(args, dict) or set(args) != set(tool.fields):
            raise ToolError("Tool arguments do not match its declared fields.")
        if any(not isinstance(v, str) or not v or len(v) > MAX_TEXT for v in args.values()):
            raise ToolError("Tool fields must be nonempty text of at most 20,000 characters.")
        if "path" in args:
            self.safe_path(args["path"])
        return tool

    def safe_path(self, name: str) -> Path:
        # Both separator styles are checked even when developing on Linux.
        win = PureWindowsPath(name)
        parts = name.replace("\\", "/").split("/")
        if (not name or len(name) > 240 or Path(name).is_absolute() or win.drive
                or any(p in ("", ".", "..") or p.startswith(".") for p in parts)
                or any(any(c in p for c in ':<>"|?*\x00') or p.endswith((" ", ".")) for p in parts)
                or any(PureWindowsPath(p).is_reserved() for p in parts)):
            raise ToolError("Use a relative file path inside the Nova workspace, without hidden or parent folders.")
        candidate = self.workspace
        for part in parts:
            candidate = candidate / part
            if candidate.is_symlink():
                raise ToolError("Symbolic links are outside the allowed file scope.")
        if not candidate.resolve().is_relative_to(self.workspace):
            raise ToolError("That path is outside the Nova workspace.")
        return candidate

    @staticmethod
    def digest(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def list_files(self, args: dict, mission_id: str) -> dict:
        paths = []
        # Bounded traversal; do not follow symbolic-link directories.
        visited = 0
        truncated = False
        for root, dirs, names in os.walk(self.workspace, followlinks=False):
            dirs[:] = sorted(d for d in dirs if not d.startswith(".") and not (Path(root) / d).is_symlink())
            visited += 1
            for name in sorted(names):
                path = Path(root) / name
                if not name.startswith(".") and not path.is_symlink():
                    paths.append(path.relative_to(self.workspace).as_posix())
                    if len(paths) == 500:
                        truncated = True
                        break
            if truncated or visited >= 500:
                truncated = True
                break
        return {"files": paths, "truncated": truncated, "verified": True}

    def read_file(self, args: dict, mission_id: str) -> dict:
        path = self.safe_path(args["path"])
        try:
            flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
            fd = os.open(path, flags)
            with os.fdopen(fd, "rb") as stream:
                info = os.fstat(stream.fileno())
                if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                    raise ToolError("Only regular, unlinked workspace files can be read.")
                data = stream.read(MAX_FILE_BYTES + 1)
            if len(data) > MAX_FILE_BYTES:
                raise ToolError("This file exceeds the 1 MB reading limit.")
            return {"path": args["path"], "content": data.decode("utf-8"), "sha256": self.digest(data), "verified": True}
        except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError, PermissionError):
            raise ToolError("The file is missing, inaccessible, or not UTF-8 text.") from None

    def create_file(self, args: dict, mission_id: str) -> dict:
        path = self.safe_path(args["path"])
        path.parent.mkdir(parents=True, exist_ok=True)
        self.safe_path(args["path"])
        data = args["content"].encode("utf-8")
        try:
            with path.open("xb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
        except FileExistsError:
            raise ToolError("A file already exists at this path. Choose a new name; Nova never overwrites it.") from None
        actual = self.read_file({"path": args["path"]}, mission_id)
        if actual["sha256"] != self.digest(data):
            raise ToolError("The created file could not be verified.")
        return {"path": args["path"], "bytes": len(data), "sha256": actual["sha256"], "verified": True}

    def system_info(self, args: dict, mission_id: str) -> dict:
        return {"os": platform.system(), "release": platform.release(), "python": platform.python_version(), "verified": True}
