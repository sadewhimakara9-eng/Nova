# Testing

Run `.venv-nova/bin/python -m unittest discover -s tests -v` after setup. The release suite covers core workflows, catalogs, UI AppTests, provider privacy/errors/health, mocked DPAPI/Windows APIs, and real local OCR when Tesseract is installed. Skips must be reported separately if the optional engine is missing.

Start an isolated loopback Streamlit instance with a temporary NOVA_DATA_DIR, then run `python scripts/check_ui_browser.py --url http://127.0.0.1:PORT --output /tmp/nova-browser-evidence`. Playwright/Chromium are development tools only. Browser checks exercise actual navigation, chat commands, privacy, emergency stop and decision CRUD without cloud calls.

Windows and live cloud acceptance remain unrun. Tests using mocked HTTP/DPAPI cannot establish account connectivity, model quality or actual Windows encryption. Build and scan the source ZIP using `python scripts/package_release.py`; validate its CRC and downloaded checksum before distributing.

## Release 0.4.0 evidence

103 tests passed on Python 3.12/Linux, zero failures/skips. Real Chromium verified all 13 retained pages, four viewport sizes, local chat, unavailable voice state, privacy, stop/resume, capability search and decision CRUD. Provider network and DPAPI checks are mocked. Dependency check and requirement generation check passed.

An additional real browser check uploaded an English PNG and extracted NOVA LOCAL TEST 123 with local Tesseract, without inserting it into conversation history.
