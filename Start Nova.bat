@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 scripts\run_nova.py
) else (
    python scripts\run_nova.py
)
if errorlevel 1 (
    echo.
    echo Nova needs Python 3.11 or newer. Get Python from https://www.python.org/downloads/
    echo If Python is installed, check the error above and try again.
    pause
)
