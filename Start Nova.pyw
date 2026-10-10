"""Windows GUI entry point: hidden bootstrap, local logs, visible error dialog."""
import ctypes
import os
from pathlib import Path
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parent
    data = Path(os.environ.get('NOVA_DATA_DIR') or Path(os.environ.get('LOCALAPPDATA', str(root))) / 'NovaAgent')
    logs = data / 'logs'
    logs.mkdir(parents=True, exist_ok=True)
    path = logs / 'startup.log'
    # Bounded rotation; no credentials are passed as command arguments.
    if path.exists() and path.stat().st_size > 1_000_000:
        path.replace(logs / 'startup.previous.log')
    environment = os.environ.copy()
    environment['NOVA_GUI'] = '1'
    environment['PYTHONUTF8'] = '1'
    python = str(Path(sys.executable).with_name('python.exe'))
    try:
        with path.open('a', encoding='utf-8') as output:
            code = subprocess.call([python, str(root / 'scripts/run_nova.py')], cwd=root, env=environment,
                                   stdin=subprocess.DEVNULL, stdout=output, stderr=output,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
        if code:
            ctypes.windll.user32.MessageBoxW(None, 'NOVA could not start. Check your Python installation and internet connection. Startup details are in your NovaAgent logs folder. You can also use Start Nova.bat for diagnostics.', 'NOVA startup', 0x10)
    except OSError:
        ctypes.windll.user32.MessageBoxW(None, 'NOVA needs Python 3.11 or newer and a writable application folder.', 'NOVA startup', 0x10)


if __name__ == '__main__':
    main()
