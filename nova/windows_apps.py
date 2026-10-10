"""Windows application discovery and launch with visible-window verification.

Only locally discovered executables/AUMIDs may launch. No owner text enters
PowerShell, shell=True, command arguments, registry writes or package installs.
"""
from dataclasses import dataclass
from difflib import SequenceMatcher
import base64
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


class AppError(ValueError):
    pass


@dataclass(frozen=True)
class App:
    name: str
    target: str
    kind: str = "exe"
    aliases: tuple[str, ...] = ()


# This script is fixed source. It reads Start Menu shortcuts and packaged app
# registrations; it never contains interpolated owner input or executes links.
DISCOVERY_SCRIPT = r"""
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$ErrorActionPreference='Stop'; $apps=@(); $w=New-Object -ComObject WScript.Shell
foreach($folder in @([Environment]::GetFolderPath('StartMenu'),[Environment]::GetFolderPath('CommonStartMenu'))) {
 if(Test-Path -LiteralPath $folder) {
  Get-ChildItem -LiteralPath $folder -Filter '*.lnk' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1000 | ForEach-Object {
   try { $s=$w.CreateShortcut($_.FullName)
    if($s.TargetPath -and -not $s.Arguments) { $apps += @{name=$_.BaseName; target=$s.TargetPath; kind='exe'} }
   } catch {}
  }
 }
}
Get-StartApps | Select-Object -First 1000 | ForEach-Object { if($_.AppID -match '^[A-Za-z0-9._-]+![A-Za-z0-9._-]+$') { $apps += @{name=$_.Name; target=$_.AppID; kind='package'} } }
ConvertTo-Json -InputObject @($apps) -Compress
"""

BLOCKED_EXECUTABLES = {"cmd", "powershell", "pwsh", "wscript", "cscript", "mshta", "rundll32",
                       "regsvr32", "reg", "msiexec", "schtasks", "shutdown", "format", "diskpart",
                       "python", "pythonw", "py", "node", "bash", "wsl", "wt", "conhost"}


def normalized(value):
    return " ".join(re.findall(r"\w+", value.casefold()))


def resolve(query, candidates):
    key = normalized(query)
    def names(app):
        return {normalized(app.name), normalized(Path(app.target).stem), *(normalized(alias) for alias in app.aliases)}
    exact = [a for a in candidates if key in names(a) or key == normalized(f'{a.name} ({a.kind})')]
    if len(exact) == 1:
        return exact[0]
    ranked = sorted(((max(SequenceMatcher(None, key, name).ratio() for name in names(a)), a)
                     for a in candidates), key=lambda pair: pair[0], reverse=True)
    if not exact and ranked and ranked[0][0] >= .84 and (len(ranked) == 1 or ranked[0][0] - ranked[1][0] >= .12):
        return ranked[0][1]
    options = exact or [a for score, a in ranked[:5] if score >= .55]
    if options:
        raise AppError("Application name is ambiguous. Use a more specific installed name: " + ", ".join(f'{a.name} ({a.kind})' for a in options[:5]))
    raise AppError("No matching launchable app was discovered. Check its installed name. Shortcuts requiring arguments and some portable apps are not supported yet.")


class WindowsApps:
    def __init__(self):
        self.platform = sys.platform

    def _windows(self):
        if self.platform != "win32":
            raise AppError("Local app control needs Windows. No application was launched on this computer.")

    @staticmethod
    def safe_candidate(app):
        if not app.name or len(app.name) > 200 or any(ord(c) < 32 for c in app.name):
            return False
        if app.kind == "package":
            return bool(re.fullmatch(r"[A-Za-z0-9._-]+![A-Za-z0-9._-]+", app.target)) and not any(
                term in app.target.casefold() for term in ("windowsterminal", "powershell"))
        path = Path(app.target)
        stem = path.stem.casefold()
        return (app.kind == "exe" and path.is_absolute() and not str(path).startswith(("\\\\", "//"))
                and path.suffix.casefold() == ".exe" and path.is_file() and not path.is_symlink()
                and stem not in BLOCKED_EXECUTABLES and not stem.startswith(("python", "powershell")))

    def discover(self):
        self._windows()
        import winreg
        candidates = []
        for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
            for view in (winreg.KEY_WOW64_64KEY, winreg.KEY_WOW64_32KEY):
                try:
                    with winreg.OpenKey(hive, r"Software\Microsoft\Windows\CurrentVersion\App Paths", 0, winreg.KEY_READ | view) as key:
                        for index in range(min(winreg.QueryInfoKey(key)[0], 2000)):
                            try:
                                name = winreg.EnumKey(key, index)
                                with winreg.OpenKey(key, name) as sub:
                                    target = winreg.QueryValueEx(sub, None)[0]
                                if isinstance(target, str):
                                    candidates.append(App(Path(name).stem, os.path.expandvars(target.strip('"'))))
                            except OSError:
                                continue
                except OSError:
                    continue
        powershell = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32/WindowsPowerShell/v1.0/powershell.exe"
        try:
            result = subprocess.run([str(powershell), "-NoProfile", "-NonInteractive", "-EncodedCommand",
                                     base64.b64encode(DISCOVERY_SCRIPT.encode('utf-16-le')).decode('ascii')],
                                    capture_output=True, timeout=20, creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode == 0 and len(result.stdout) <= 2_000_000:
                raw = json.loads(result.stdout.decode('utf-8-sig'))
                if isinstance(raw, list):
                    candidates.extend(App(str(r['name']), str(r['target']), str(r['kind'])) for r in raw if isinstance(r, dict) and {'name','target','kind'} <= r.keys())
        except (OSError, subprocess.TimeoutExpired, ValueError, KeyError):
            pass
        # Current visible executable windows also make portable apps discoverable.
        for path, package, title in self.visible_windows():
            if path:
                candidates.append(App(Path(path).stem, path))
        unique = {}
        for app in candidates:
            if self.safe_candidate(app):
                key = (app.kind, app.target.casefold())
                old = unique.get(key)
                unique[key] = App(old.name, old.target, old.kind, tuple(dict.fromkeys((*old.aliases, app.name)))) if old else app
        return list(unique.values())

    def visible_windows(self):
        self._windows()
        import ctypes
        from ctypes import wintypes
        user = ctypes.WinDLL('user32', use_last_error=True)
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
        kernel.GetApplicationUserModelId.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.UINT), wintypes.LPWSTR]
        user.IsWindowVisible.argtypes = [wintypes.HWND]
        user.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
        user.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
        rows = []
        callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

        @callback_type
        def collect(hwnd, _):
            if not user.IsWindowVisible(hwnd):
                return True
            title = ctypes.create_unicode_buffer(1024)
            user.GetWindowTextW(hwnd, title, len(title))
            if not title.value:
                return True
            pid = wintypes.DWORD()
            user.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            handle = kernel.OpenProcess(0x1000, False, pid.value)
            if handle:
                try:
                    path = ctypes.create_unicode_buffer(32768); size = wintypes.DWORD(len(path))
                    valid = kernel.QueryFullProcessImageNameW(handle, 0, path, ctypes.byref(size))
                    package = ctypes.create_unicode_buffer(512); length = wintypes.UINT(len(package))
                    identified = kernel.GetApplicationUserModelId(handle, ctypes.byref(length), package) == 0
                    rows.append((path.value if valid else '', package.value if identified else '', title.value))
                finally:
                    kernel.CloseHandle(handle)
            return True
        user.EnumWindows.argtypes = [callback_type, wintypes.LPARAM]
        user.EnumWindows(collect, 0)
        return rows

    def launch(self, app):
        if not self.safe_candidate(app):
            raise AppError("This application target is not eligible for direct launch.")
        if app.kind == 'package':
            explorer = Path(os.environ.get('SystemRoot', r'C:\Windows')) / 'explorer.exe'
            subprocess.Popen([str(explorer), 'shell:AppsFolder\\' + app.target], shell=False,
                             creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.Popen([app.target], shell=False, cwd=str(Path(app.target).parent),
                             creationflags=subprocess.CREATE_NO_WINDOW)

    def open(self, query):
        self._windows()
        if not isinstance(query, str) or not re.fullmatch(r'[\w .+()\-]{1,100}', query) or query.startswith('.'):
            raise AppError("Use an installed application name, not command arguments or a path.")
        app = resolve(query, self.discover())
        def visible():
            return any((app.kind == 'exe' and path.casefold() == app.target.casefold()) or
                       (app.kind == 'package' and package.casefold() == app.target.casefold())
                       for path, package, _ in self.visible_windows())
        if visible():
            return {'application': app.name, 'state': 'ALREADY_VISIBLE', 'verified': True,
                    'verification': 'Visible window matched executable path or application identity; focus was not changed.'}
        try:
            self.launch(app)
        except OSError:
            raise AppError("Windows could not launch the resolved application.") from None
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if visible():
                return {'application': app.name, 'state': 'WINDOW_VISIBLE', 'verified': True,
                        'verification': 'Visible window matched executable path or application identity.'}
            time.sleep(.25)
        raise AppError("Launch was requested but a matching visible window was not verified. Check Windows before trying again; Nova will not automatically repeat this action.")

    def open_site(self, site):
        self._windows()
        destinations = {'gemini': 'https://gemini.google.com/', 'youtube': 'https://www.youtube.com/'}
        key = site.casefold().strip()
        if key not in destinations:
            raise AppError("Only configured official web destinations are available in this release.")
        candidates = self.discover()
        # Prefer an exact installed native/PWA identity, never an uncertain
        # fuzzy match when choosing a destination with external effects.
        exact = [app for app in candidates if normalized(app.name) == key]
        if exact:
            return self.open(site)
        try:
            os.startfile(destinations[key])
        except OSError:
            raise AppError("The default browser could not accept this website request.") from None
        return {'site': key, 'url': destinations[key], 'verified': False,
                'verification': 'OS_HANDOFF_ONLY', 'state': 'CHECK_BROWSER'}
