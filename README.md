# NOVA — personal agent foundation

A working first release built from the [NOVA v6 master specification](docs/spec/NOVA_MASTER_PROMPT.md). This is **version 0.1**, the foundation for that larger product: a local dashboard, Sinhala-aware commands, persistent memory, concurrent missions, workspace tools, and optional AI chat/planning.

## Start on your Windows PC

1. Install **Python 3.11 or newer** from [python.org](https://www.python.org/downloads/), if it is not already installed.
2. Open this project folder and double-click **Start Nova.bat**.
3. The first launch installs the dashboard automatically. Keep its console window open while using Nova. Open the local address printed by Streamlit if your browser does not open automatically.

You do not need to edit JSON or create a Python environment manually. Internet is needed to install dependencies the first time. Later launches reuse them. The launcher uses port **8502**, listens only on your own computer, and keeps Streamlit's CORS/XSRF protections enabled. The Windows batch wrapper has been reviewed but needs a real Windows machine for execution testing; the Python bootstrap and dashboard have been run on Linux.

On Linux/macOS, run `sh start-nova.sh`. Developers with dependencies installed can run `python -m streamlit run nova_app.py --server.address 127.0.0.1 --server.port 8502 --browser.gatherUsageStats false`.

## Try it now

Open **Chat** and try:

```text
/help
/remember language = Sinhala
/recall
/write notes.txt | අද කළ යුතු වැඩ
/files
/read notes.txt
/status
Nova stop
Nova resume
```

File commands queue real work. Open **Missions** and select **Refresh mission status** to see the verified result. The dashboard shows your workspace location. Files stay in that dedicated folder; Nova cannot select arbitrary folders on your PC in this release.

In **Missions**, enter `/write welcome.txt | ආයුබෝවන්!`, select **Prepare plan**, review it, and select **Run prepared plan**. Preparation never writes a file. Existing files are never overwritten. **Undo file write** moves an unchanged generated file to Nova's local trash; it refuses if you edited the file afterward.

## Connect an AI model

Built-in commands work immediately without an AI connection. Free-form conversation and natural-language planning require a provider:

- **Local Ollama:** install [Ollama](https://ollama.com/), download a model using its app, and keep it running. In Nova **Settings**, select **Ollama (local)** and enter the exact installed model name. Default endpoint: `127.0.0.1:11434`. Sinhala quality depends on your chosen model.
- **Groq:** in **Settings**, select **Groq (cloud)** and enter your own key into the password field. Select **NORMAL** privacy mode and explicitly classify the request **PUBLIC** or **INTERNAL**. Only then can a request leave your computer. Alternatively supply `GROQ_API_KEY` through a secure process environment.

Keys entered in Settings stay in the current Streamlit session, are not written to the database, and can be cleared there. Provider settings are session-local. The `.env.example` is documentation, not an automatically loaded secret file. The old app's embedded key is never used by the new agent.

Cloud requests receive the current prompt and fixed system instructions only. Nova does not automatically send saved memory, mission history, or files to a model. Model answers are conversational text, not executed commands. A generated mission must pass the tool allowlist and be reviewed before execution. Live model inference was not tested in this environment; provider tests use mocked HTTP responses.

## Data and privacy

Windows defaults to `%LOCALAPPDATA%\NovaAgent`; Linux/macOS defaults to `~/.local/share/NovaAgent`. `NOVA_DATA_DIR` can select another local folder. This folder contains SQLite state, the workspace, runtime lock, and rollback trash. Stop Nova before copying the **entire data folder** for a manual backup.

Memory is explicit: you choose what to save and can forget it in **Memory**. New explicit preferences override old ones; inferred preferences cannot replace explicit ones. Memory and mission content are local **unencrypted SQLite data**, so protect your OS account and disk. Forgetting removes a live memory row; this is not forensic secure erasure of backups or SQLite pages. Secure vault, automatic backup/restore, and full privacy redaction are later milestones. Do not store credentials in chat or memory. Common credential formats are rejected, but detection is heuristic.

Emergency stop persists across restarts and pauses queued work. An atomic operation already in progress may finish and record its actual result. Restart retries interrupted read-only missions; interrupted writes are **BLOCKED** for inspection rather than silently repeated. Independently submitted missions run on up to three workers. Steps in one prepared plan run sequentially, and a failed prerequisite blocks its dependents.

## What is available

| Capability | Status |
| --- | --- |
| Local dashboard, chat commands, memory viewer | Working; tested |
| Sinhala text and selected Sinhala/Singlish commands | Working; tested; not general language understanding without a model |
| File listing, UTF-8 reading/creation, system info | Working in Nova's workspace |
| Concurrent missions, durable stop, recovery, verified file receipts | Working; tested |
| File/system specialist workers and reviewed AI plans | Implemented; deterministic tools tested; live AI planning unverified |
| Ollama and Groq adapters | Implemented; mocked HTTP tests; need a running model or your key |
| Voice, wake word, natural Sinhala speech | Not implemented |
| Windows UI control, browser control, Office, email, payments, smart home | Not implemented |
| Self-updates, plugin sandbox, encrypted vault, native installer | Not implemented |

This is a modular monolith, not the complete autonomous operating system in the specification. See [project status](docs/PROJECT_STATUS.md) for the next milestones and [architecture](docs/architecture.md) for design details.

## Development and tests

```sh
python -m pip install -r nova-requirements.txt
python -m unittest discover -s tests -v
```

The suite covers functional tools, concurrency, recovery, permissions, credential handling, mocked providers, and a real-core Streamlit interaction workflow. It uses isolated temporary data folders and no live model calls. Existing `app.py` and `requirements.txt` remain the legacy app; start the new agent through **Start Nova.bat** or `nova_app.py`.
