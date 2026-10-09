"""NOVA Glass: a local desktop-style interface around the existing Nova core."""
from __future__ import annotations

import json
import os
import re
from html import escape

import streamlit as st

from nova.core import NovaCore, NovaError
from nova.providers import BLOCKED_CLASSIFICATIONS, ModelProvider, contains_credentials
from nova.ui.controller import (APPEARANCE_DEFAULTS, PAGES, ORB_STATES, UIController,
                                assistant_state, greeting, mission_group, elapsed_label)
from nova.ui.glass import apply_theme, orb, header, badge, empty_state, icon

st.set_page_config(page_title="NOVA · Glass", page_icon="✦", layout="wide", initial_sidebar_state="expanded")


@st.cache_resource
def get_core(data_dir: str) -> NovaCore:
    return NovaCore(data_dir=data_dir or None)


def initialize_state(controller):
    defaults = {
        "nova_page": "Home", "nova_nav_expanded": False,
        "nova_provider": "Built-in commands", "nova_ollama_model": "llama3.2",
        "nova_groq_model": "llama-3.3-70b-versatile", "nova_api_key": "",
        "nova_mode": "LOCAL_ONLY", "nova_classification": "PERSONAL", "nova_language": "si",
        "nova_messages": [], "nova_prepared_plan": None, "nova_notice": "",
        "nova_show_approval": False,
        "nova_voice_preview": False, "nova_voice_demo_state": "listening",
        "nova_project_open": False, "nova_appearance": controller.appearance(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if st.session_state.get("nova_next_page"):
        st.session_state.nova_page = st.session_state.pop("nova_next_page")
    if st.session_state.pop("nova_clear_key", False):
        st.session_state.nova_api_key = ""
    if st.session_state.pop("nova_end_preview", False):
        st.session_state.nova_voice_preview = False
    if st.session_state.get("nova_pending_mode"):
        st.session_state.nova_mode = st.session_state.pop("nova_pending_mode")


def go(page):
    st.session_state.nova_next_page = page
    st.rerun()


def show_error(exc):
    if isinstance(exc, (ValueError, RuntimeError)):
        message = str(exc)[:600] or "That action could not be completed."
    else:
        message = "That action could not be completed. Please check Settings and try again."
    secret = st.session_state.get("nova_api_key", "")
    if secret:
        message = message.replace(secret, "[redacted]")
    if contains_credentials(message):
        message = "The action was stopped because sensitive information was detected."
    st.error(message)


def selected_provider():
    choice = st.session_state.nova_provider
    if choice == "Built-in commands":
        return None
    if choice == "Ollama (local)":
        return ModelProvider("ollama", st.session_state.nova_ollama_model)
    if st.session_state.nova_mode != "NORMAL":
        raise NovaError("Groq needs NORMAL mode. Choose it explicitly in Privacy.")
    if st.session_state.nova_classification not in {"PUBLIC", "INTERNAL"}:
        raise NovaError("Cloud requests need PUBLIC or INTERNAL classification. Personal content stays local.")
    if not st.session_state.nova_api_key and not os.environ.get("GROQ_API_KEY"):
        raise NovaError("Add your Groq API key in Settings before using the cloud model.")
    return ModelProvider("groq", st.session_state.nova_groq_model, st.session_state.nova_api_key or None)


def is_control_command(text):
    value = re.sub(r"^nova[\s,]+", "", text.strip(), flags=re.I).strip().casefold().rstrip(".! ")
    return value in {"stop", "emergency stop", "/stop", "නවත්වන්න", "නවතින්න",
                     "resume", "/resume", "continue", "දිගටම කරගෙන යන්න"}


def request_options(text=""):
    return {"provider": None if text.lstrip().startswith("/") or is_control_command(text) else selected_provider(),
            "mode": st.session_state.nova_mode, "classification": st.session_state.nova_classification,
            "language": st.session_state.nova_language}


def changes_allowed(core):
    return not core.stopped and st.session_state.nova_mode not in {"READ_ONLY", "DRY_RUN", "SAFE_MODE"}


def sidebar(core):
    with st.sidebar:
        st.html('<div class="nova-brand">' + icon("sparkles", 28) + '<span>NOVA<small>PERSONAL INTELLIGENCE</small></span></div>')
        page = st.radio("Workspace", PAGES, key="nova_page", label_visibility="collapsed")
        st.toggle("Expand navigation", key="nova_nav_expanded")
        with st.popover("Privacy & language", icon=":material/shield:", use_container_width=True):
            st.selectbox("Operating mode", ["LOCAL_ONLY", "NORMAL", "OFFLINE", "PRIVATE", "READ_ONLY", "DRY_RUN", "SAFE_MODE"], key="nova_mode")
            st.selectbox("Request classification", ["PERSONAL", "SECRET", "PRIVATE", "INTERNAL", "PUBLIC"], key="nova_classification")
            st.selectbox("Response language", ["si", "en"], key="nova_language", format_func=lambda v: "සිංහල · Sinhala" if v == "si" else "English")
            st.caption("These choices apply to new requests. Running missions keep their approved scope.")
        if core.stopped:
            if st.button("Resume agent", icon=":material/play_arrow:", use_container_width=True):
                core.resume()
                st.rerun()
        elif st.button("Emergency stop", icon=":material/stop_circle:", use_container_width=True, help="Pause new work. An atomic file operation already running may finish safely."):
            core.stop()
            st.rerun()
        st.html('<div class="nova-sidebar-foot">' + icon("shield", 14) + ' Local workspace · v0.2</div>')
    return page


@st.fragment(run_every="3s")
def live_indicator(core):
    state = assistant_state(core.missions(), core.stopped, st.session_state.nova_mode)
    label = f"{state.running} missions running" if state.running else "Automation paused" if core.stopped else "Local tools ready"
    with st.popover(label, icon=":material/activity_zone:", use_container_width=True):
        st.write(f"{state.running} running · {state.queued} queued · {state.waiting} waiting")
        st.caption("Live mission status · updates every three seconds")
        if st.button("Open mission details", key="live-missions"):
            go("Missions")
    events = core.events()
    newest = max((e["id"] for e in events), default=0)
    previous = st.session_state.get("nova_last_event", newest)
    for event in reversed(events):
        if event["id"] > previous and event["kind"] in {"MISSION_COMPLETED", "MISSION_FAILED"}:
            st.toast("Mission completed and verified." if event["kind"] == "MISSION_COMPLETED" else "A mission needs attention.")
    st.session_state.nova_last_event = newest


def shell_header(core, page):
    with st.container(key="shell-header"):
        left, right = st.columns([3, 1.35], vertical_alignment="center")
        with left:
            st.html('<div class="nova-kicker">YOUR SPACE, INTELLIGENTLY CONNECTED</div><div class="nova-breadcrumb">NOVA <span>/</span> ' + escape(page) + '</div>')
        with right:
            activity, stop = st.columns([3, 1])
            with activity: live_indicator(core)
            with stop:
                if st.button("Resume" if core.stopped else "Stop", key="header-stop", help="Emergency stop pauses new automation; resume restarts paused missions."):
                    core.resume() if core.stopped else core.stop()
                    st.rerun()


def switch_assistant(page):
    st.session_state.nova_assistant_mode = "Voice" if page == "Voice" else "Chat"
    def changed():
        st.session_state.nova_next_page = st.session_state.nova_assistant_mode
    left, center, right = st.columns([1, 1, 1])
    with center:
        st.segmented_control("Assistant mode", ["Chat", "Voice"], key="nova_assistant_mode", on_change=changed,
                             required=True, label_visibility="collapsed", width="stretch")


def feature(title, value, description, symbol):
    st.html('<div class="nova-feature-card"><div class="nova-feature-icon">' + icon(symbol, 20) +
            '</div><div class="nova-muted">' + escape(title) + '</div><div class="nova-feature-value">' +
            escape(str(value)) + '</div><div class="nova-feature-description">' + escape(description) + '</div></div>')


def home(core):
    switch_assistant("Home")
    state = assistant_state(core.missions(), core.stopped, st.session_state.nova_mode)
    with st.container(key="home-hero"):
        orb(state.orb, 210, state.label)
        st.html('<div class="nova-hero"><div class="nova-eyebrow">YOUR WORLD. A LITTLE LIGHTER.</div><h1>' + escape(greeting(st.session_state.nova_language)) +
                '</h1><p>' + ('ඔබට අද මොන වැඩේ කරගන්න ඕනද?' if st.session_state.nova_language == 'si' else 'A clear mind. A little help. What shall we do today?') + '</p></div>')
    a, b, c = st.columns(3)
    with a:
        feature("Missions", str(state.running + state.queued), "Active in your workspace", "missions")
        if st.button("View missions", key="home-missions", use_container_width=True): go("Missions")
    with b:
        feature("Memory", str(len(core.memories())), "Things you asked me to remember", "memory")
        if st.button("Explore memory", use_container_width=True): go("Memory")
    with c:
        feature("Your privacy", "Staying local" if st.session_state.nova_mode != "NORMAL" else "You decide", "Your permissions. Your control.", "shield")
        if st.button("Privacy controls", use_container_width=True): go("Privacy")
    composer(core)


def receive_message(core, text):
    if contains_credentials(text) or (st.session_state.nova_classification in BLOCKED_CLASSIFICATIONS and not is_control_command(text)):
        st.warning("This request was withheld because it contains credential-like data or has a protected classification. It was not added to conversation history.")
        return
    if core.stopped and not is_control_command(text):
        st.info("The agent is stopped. Type /resume or use Resume agent to continue.")
        return
    st.session_state.nova_messages.append({"role": "user", "content": text})
    try:
        with st.status("NOVA is thinking…", expanded=False):
            answer = core.chat(text, **request_options(text))
        st.session_state.nova_messages.append({"role": "assistant", "content": answer})
        go("Chat")
    except Exception as exc:
        show_error(exc)


def attachment_menu(core):
    with st.popover("Attach", icon=":material/add:", help="Import a text file into your local workspace"):
        st.write("Add to your workspace")
        upload = st.file_uploader("Text file", type=["txt", "md", "csv"], max_upload_size=1, key="nova_attachment")
        st.caption("Import only. File contents are not sent to a model. Review the local file action before saving.")
        if st.button("Prepare import", disabled=upload is None or not changes_allowed(core)):
            try:
                raw = upload.getvalue()
                if len(raw) > 60_000:
                    raise NovaError("Choose a text file under 60 KB and 20,000 characters.")
                content = raw.decode("utf-8")
                step = {"tool": "files.create", "args": {"path": upload.name, "content": content}, "goal": "Import an owner-selected text file"}
                core._validate_plan([step])
                st.session_state.nova_prepared_plan = [step]
                go("Missions")
            except UnicodeError:
                st.error("Please choose a UTF-8 text file.")
            except Exception as exc:
                show_error(exc)
        for name in ("Image", "Document / PDF", "Screenshot", "Folder", "Clipboard"):
            st.button(name + " · coming soon", disabled=True, key="attachment_" + name)


def composer(core):
    with st.bottom:
        with st.container(key="floating-composer"):
            attach, message, microphone = st.columns([1.1, 7, 1], vertical_alignment="center")
            with attach: attachment_menu(core)
            with message:
                text = st.chat_input("Type /resume to continue" if core.stopped else "Ask NOVA anything… /help", key="nova_composer", max_chars=20_000)
            with microphone:
                if st.button("Voice", icon=":material/mic:", help="Open voice workspace; speech engine not connected", key="composer_voice"):
                    go("Voice")
            if text: receive_message(core, text)
            st.html('<div class="nova-composer-note">' + icon("shield", 12) + ' ' + escape(st.session_state.nova_mode.replace("_", " ").title()) + ' · ' + escape(st.session_state.nova_provider) + '</div>')


def chat(core):
    switch_assistant("Chat")
    with st.expander("Conversation options"):
        left, right = st.columns(2)
        with left:
            if st.button("Clear this conversation"):
                st.session_state.nova_messages = []
                st.rerun()
        with right:
            st.caption("Conversation is session-only. Save lasting facts in Memory.")
        st.code("/help    /files    /read notes.txt\n/write notes.txt | Text to save\n/remember language = Sinhala    /recall", language="text")
    if not st.session_state.nova_messages:
        orb("privacy" if st.session_state.nova_mode != "NORMAL" else "idle", 230, "Ready when you are")
        header("කියන්න, මම ඒක බලන්නම්." if st.session_state.nova_language == "si" else "A little help, a conversation away.", "Start with /help, or connect your preferred model in Settings.")
    for message in st.session_state.nova_messages:
        with st.chat_message(message["role"], avatar=":material/person:" if message["role"] == "user" else ":material/auto_awesome:"):
            st.write(message["content"])
    composer(core)


def voice(core):
    switch_assistant("Voice")
    preview = st.session_state.nova_voice_preview
    state = st.session_state.nova_voice_demo_state if preview else "offline"
    orb(state, 300, (state.title() + " · visual preview") if preview else "Voice engine not connected")
    with st.container(border=True, key="voice-panel"):
        st.html('<div class="nova-voice-label">' + icon("voice", 22) + ' ' + badge("VISUAL PREVIEW" if preview else "DISCONNECTED", "amber" if preview else "neutral") + '</div>')
        st.subheader(state.title() + "…" if preview else "Your voice, when you’re ready.")
        if preview:
            st.caption("Simulated animation only. No microphone is open, no transcription is running, and no command is executed.")
            st.write('“Nova, මගේ project එක දිගටම කරගෙන යන්න.”')
            st.caption("Example transcript · not recorded audio")
        else:
            st.write("හඬ සේවාව තවම සම්බන්ධ කර නැහැ. Chat හරහා NOVA භාවිත කරන්න පුළුවන්.")
            st.caption("Live transcription will appear here when a speech engine is connected.")
        st.button("Microphone unavailable", icon=":material/mic_off:", disabled=True, help="STT and audio capture are not implemented")
    st.toggle("Visual preview only", key="nova_voice_preview", help="Try the orb states without accessing your microphone or backend")
    if st.session_state.nova_voice_preview:
        st.selectbox("Preview orb state", ORB_STATES, key="nova_voice_demo_state")
        if st.button("Stop preview", icon=":material/stop:"):
            st.session_state.nova_end_preview = True
            st.rerun()
    if st.button("Continue in Chat", icon=":material/chat_bubble:"): go("Chat")


def plan_details(steps):
    for index, step in enumerate(steps, 1):
        st.markdown(f"**{index}. {step['goal']}**")
        path = step["args"].get("path")
        if path: st.write("File: " + path)
        st.caption(step["tool"].replace(".", " → "))
        if "content" in step["args"]:
            with st.expander("View file contents", expanded=False): st.text(step["args"]["content"])


@st.dialog("Review mission", width="medium")
def approval_dialog(core):
    steps = st.session_state.nova_prepared_plan
    if not steps:
        st.info("No plan is waiting for approval.")
        return
    plan_details(steps)
    st.divider()
    st.write("**Target:** your local Nova workspace")
    st.write("**Data leaving this device:** none during tool execution")
    st.write("**Cost:** no API call or payment during execution")
    st.write("**Reversibility:** new files can be undone while their contents remain unchanged. Existing files are never overwritten.")
    cancel, approve = st.columns(2)
    if cancel.button("Cancel", use_container_width=True):
        st.session_state.nova_show_approval = False
        st.rerun()
    if approve.button("Approve once", type="primary", use_container_width=True, disabled=core.stopped or st.session_state.nova_mode == "DRY_RUN"):
        try:
            ids = core.submit_plan(steps, mode=st.session_state.nova_mode)
            st.session_state.nova_prepared_plan = None
            st.session_state.nova_show_approval = False
            st.session_state.nova_notice = f"{len(ids)} mission step(s) queued."
            st.rerun()
        except Exception as exc: show_error(exc)


def mission_planner(core):
    with st.expander("Prepare a mission", expanded=not core.missions() or bool(st.session_state.nova_prepared_plan)):
        with st.form("prepare_mission"):
            goal = st.text_area("What should Nova do?", placeholder="/write welcome.txt | ආයුබෝවන්!")
            prepare = st.form_submit_button("Prepare plan", disabled=core.stopped)
        if prepare:
            st.session_state.nova_prepared_plan = None
            try:
                with st.spinner("Preparing your steps…"):
                    st.session_state.nova_prepared_plan = core.plan(goal, **request_options(goal))
            except Exception as exc: show_error(exc)
        if st.session_state.nova_prepared_plan:
            plan_details(st.session_state.nova_prepared_plan)
            run, discard = st.columns(2)
            if run.button("Run prepared plan", type="primary", disabled=core.stopped or st.session_state.nova_mode == "DRY_RUN"):
                st.session_state.nova_show_approval = True
            if discard.button("Discard plan"):
                st.session_state.nova_prepared_plan = None
                st.session_state.nova_show_approval = False
                st.rerun()
        if st.session_state.nova_show_approval and st.session_state.nova_prepared_plan:
            approval_dialog(core)


def result_view(result):
    if not result: return
    if result.get("verified"): st.caption("Verified by Nova")
    if "content" in result: st.text(result["content"])
    if "files" in result:
        if result["files"]:
            for path in result["files"]: st.write(path)
        else: st.caption("The workspace has no files yet.")
        if result.get("truncated"): st.caption("Showing the first 500 entries.")
    if "path" in result: st.write("Saved file: " + result["path"])
    if "bytes" in result: st.caption(f"{result['bytes']:,} bytes · content hash checked")
    if "os" in result: st.write(f"{result['os']} · Python {result['python']}")
    if "trash" in result: st.caption("Retained in Nova's local trash.")


@st.fragment(run_every="3s")
def mission_history(core):
    rows = core.missions()
    chosen = st.segmented_control("Mission status", ["All", "Running", "Queued", "Waiting for You", "Completed"], default="All", required=True, key="nova_mission_filter")
    if st.button("Refresh mission status", icon=":material/refresh:"): st.rerun()
    visible = [m for m in rows if chosen == "All" or mission_group(m["status"]) == chosen]
    if not visible: empty_state("A little space for your next goal.", "No missions in this view. Give NOVA something to work on.", "missions")
    for mission in visible:
        with st.expander(f"{mission['status']} · {mission['goal']} · {mission['id'][:8]}"):
            st.caption(f"{mission['tool'].split('.')[0].title()} agent · {elapsed_label(mission)} · {mission['created_at'][:16].replace('T', ' ')} UTC")
            if mission["dependency"]: st.caption("Starts after its preceding plan step completes.")
            if "path" in mission["args"]: st.write("Target: " + mission["args"]["path"])
            result_view(mission["result"])
            if mission["error"]: st.error(mission["error"])
            if mission["tool"] == "files.create" and mission["status"] == "COMPLETED":
                if st.button("Undo file write", key=f"undo_{mission['id']}", disabled=not changes_allowed(core)):
                    try:
                        st.success(core.undo(mission["id"], mode=st.session_state.nova_mode))
                    except Exception as exc: show_error(exc)


def missions(core):
    header("A clear path from idea to done.", "Your missions, their progress, and the details that matter.", "MISSIONS")
    mission_planner(core)
    mission_history(core)


def projects(core):
    header("Room for your next big idea.", "A calm home for the work you want to continue.", "PROJECTS")
    if not st.session_state.nova_project_open:
        with st.container(border=True):
            st.html(badge("LOCAL WORKSPACE", "blue"))
            st.subheader("Your Nova workspace")
            st.write("Files you create and missions you run, together in one place.")
            if st.button("Open workspace", icon=":material/folder_open:"):
                st.session_state.nova_project_open = True
                st.rerun()
        st.caption("Named projects and milestones are coming soon. This card opens your existing local workspace.")
        st.button("New project · coming soon", disabled=True, icon=":material/add:")
        return
    if st.button("All projects", icon=":material/arrow_back:"):
        st.session_state.nova_project_open = False
        st.rerun()
    st.subheader("Your Nova workspace")
    with st.expander("Workspace location"): st.text(str(core.workspace))
    left, right = st.columns(2)
    with left:
        st.markdown("**Recent files**")
        artifacts = [m for m in core.missions() if m["tool"] == "files.create" and m["status"] == "COMPLETED"]
        for m in artifacts[:6]: st.write(m["result"]["path"])
        if not artifacts: st.caption("Your verified file creations will appear here.")
    with right:
        st.markdown("**Project memory**")
        memories = [m for m in core.memories() if m["scope"] == "PROJECT"]
        for m in memories[:6]: st.write(f"{m['key']}: {m['value']}")
        if not memories: st.caption("No project notes saved yet.")
    if st.button("Prepare your next mission", type="primary"): go("Missions")


def agents(core):
    header("A small team. A shared purpose.", "Specialists with clear responsibilities and bounded permissions.", "YOUR AGENTS")
    cards = UIController(core).agents()
    for column, agent in zip(st.columns(2), cards):
        with column, st.container(border=True):
            st.html(icon("agents", 28) + " " + badge("WORKING" if agent["active"] else "LOCAL", "blue"))
            st.subheader(agent["name"])
            st.write(agent["active"]["goal"] if agent["active"] else "Ready for your next mission.")
            st.caption(f"{agent['completed']} verified · {agent['failed']} failed · reliability: {agent['reliability']}")
            with st.expander("Permissions"):
                for tool in agent["tools"]: st.write(tool.replace(".", " · "))
    st.caption("The director, planner and verifier run inside Nova Core. These are scoped local workers; they are not independently connected AI models.")
    with st.expander("Future specialists"):
        st.write("Voice · Browser · Coding · Research · Office · Smart home")
        st.caption("Coming soon. No tools or external permissions have been granted to these roles.")


def memory(core):
    header("The little things, remembered.", "Useful preferences and notes, saved only when you ask.", "MEMORY")
    with st.expander("Remember something", expanded=not core.memories()):
        with st.form("remember"):
            key = st.text_input("Memory name", placeholder="preferred_language")
            value = st.text_area("Value", placeholder="සිංහල")
            scope = st.selectbox("Memory scope", ["PERSONAL", "GLOBAL", "PROJECT"])
            st.caption("Local memory is not an encrypted vault. Do not save passwords or API keys.")
            save = st.form_submit_button("Save memory", disabled=not changes_allowed(core))
        if save:
            try:
                core.remember(key.strip(), value.strip(), scope=scope, mode=st.session_state.nova_mode)
                st.success("Memory saved locally.")
            except Exception as exc: show_error(exc)
    query = st.text_input("Search memories", placeholder="Find a preference or a note…")
    category = st.segmented_control("Memory collection", ["All", "Preferences", "Projects", "Shared notes"], default="All", required=True)
    scope = {"Preferences": "PERSONAL", "Projects": "PROJECT", "Shared notes": "GLOBAL"}.get(category)
    rows = [m for m in core.memories(query) if not scope or m["scope"] == scope]
    if not rows: empty_state("A fresh start.", "Save a preference, a useful detail, or a note for later.", "memory")
    for item in rows:
        with st.expander(f"{item['key']} · {item['scope']}"):
            st.write(item["value"])
            st.caption(f"Source: {item['source']} · Updated: {item['updated_at'][:16].replace('T', ' ')} UTC")
            confirm = st.checkbox("Delete this saved fact", key=f"confirm_{item['id']}")
            if st.button("Forget", key=f"forget_{item['id']}", disabled=not confirm or not changes_allowed(core)):
                core.forget(item["id"], mode=st.session_state.nova_mode)
                st.rerun()
    st.caption("People, device and workflow collections will appear when their memory services are available.")


def unavailable(title, description, symbol, action):
    header(title, description)
    empty_state("Not connected yet", "This workspace is ready for a future integration. No background actions are enabled.", symbol)
    st.button(action + " · coming soon", disabled=True)


def tools_page(core):
    header("A few good tools.", "Real capabilities, with a clear scope and a verified result.", "TOOLS")
    query = st.text_input("Find a capability", placeholder="Files, text, system information…")
    capabilities = {item["capability_id"]: item for item in core.capabilities()}
    names = {"files.list": ("Browse your files", "List the files in your Nova workspace.", {}),
             "files.read": ("Read text", "Read a UTF-8 file from your workspace.", None),
             "files.create": ("Create a file", "Write a new file without overwriting existing work.", None),
             "system.info": ("System information", "Check your OS and Python runtime.", {})}
    for tool in core.tools():
        title, description, args = names[tool["name"]]
        if query.casefold() not in (title + " " + description + " " + tool["name"]).casefold():
            continue
        with st.container(border=True):
            st.html(badge("LOCAL", "blue"))
            st.subheader(title)
            st.write(description)
            capability = capabilities[tool["name"]]
            with st.expander("Scope & verification"):
                st.write("Agent: " + capability["required_agents"][0].replace("-", " ").title())
                st.write(capability["verification_method"])
                st.caption("Local only · " + capability["risk_level"].replace("_", " ").lower())
            if args is not None:
                if st.button("Run " + title.lower(), key="tool_" + tool["name"], disabled=core.stopped or st.session_state.nova_mode == "DRY_RUN"):
                    core.enqueue(tool["name"], args, title, mode=st.session_state.nova_mode)
                    go("Missions")
            elif st.button("Prepare " + title.lower(), key="tool_" + tool["name"]): go("Missions")


def integrations(core):
    header("Connected, on your terms.", "Choose what NOVA can use. Nothing connects without your setup.", "INTEGRATIONS")
    left, right = st.columns(2)
    for column, name, desc in ((left, "Ollama", "Local AI on your computer"), (right, "Groq", "Optional cloud language models")):
        with column, st.container(border=True):
            st.html(badge("NOT VERIFIED", "neutral"))
            st.subheader(name)
            st.write(desc)
            st.caption("Availability is checked when you send a request. A saved choice is not proof of connection.")
            if st.button("Configure " + name): go("Settings")
    st.markdown("**On the horizon**")
    for name in ("Browser", "GitHub", "Email & calendar", "WhatsApp", "Blender & Unreal", "Smart home"):
        st.html('<div class="nova-integration-row"><span>' + escape(name) + '</span>' + badge("DISCONNECTED", "neutral") + '</div>')


def privacy(core):
    header("Your space. Your rules.", "Simple controls for what stays local and what can leave.", "PRIVACY")
    is_local = st.session_state.nova_mode != "NORMAL"
    st.html(badge("CLOUD DISABLED" if is_local else "CLOUD REQUIRES PUBLIC / INTERNAL", "blue"))
    enabled = st.toggle("Local-only protection", value=is_local, help="Disables cloud model requests. Local tools and local Ollama remain available.")
    if enabled != is_local:
        st.session_state.nova_pending_mode = "LOCAL_ONLY" if enabled else "NORMAL"
        st.rerun()
    st.write("**Current mode:** " + st.session_state.nova_mode.replace("_", " ").title())
    st.caption("Normal mode still requires a configured cloud provider and PUBLIC or INTERNAL classification for each request.")
    with st.container(border=True):
        st.subheader("Recent external data activity")
        activity = UIController(core).external_activity()
        if activity:
            for event in activity[:10]: st.write("Groq response received · " + event["created_at"][:16].replace("T", " ") + " UTC")
        else: st.write("No successful cloud responses recorded in the recent activity window.")
        st.caption("This history covers the last 200 Nova events. It does not record every attempted request or monitor other apps on your computer.")
    a, b = st.columns(2)
    with a:
        st.subheader("Protected files")
        st.write("File tools stay inside your dedicated Nova workspace. Existing files are never overwritten.")
    with b:
        st.subheader("Private by default")
        st.write("Memory and file history are not automatically sent to a model. Sensitive classifications and common credential patterns are blocked.")
    st.caption("Per-app protection, custom folder policies, a full network ledger and an encrypted secrets vault are coming soon.")


def widget_options(key):
    def preserve(): st.session_state[key] = st.session_state["widget_" + key]
    st.session_state["widget_" + key] = st.session_state[key]
    return {"key": "widget_" + key, "on_change": preserve}


def settings(core):
    header("Make a little space for you.", "Your preferences, your models, your way of working.", "SETTINGS")
    general, appearance, models, advanced = st.tabs(["General", "Appearance", "Models & APIs", "Advanced"])
    with general:
        st.subheader("NOVA Glass White")
        st.write("A quiet, light workspace for your personal AI.")
        st.caption("Change response language and request privacy using Privacy & language in the navigation.")
        st.info("Voice, notification schedules, personality presets, OS permissions, system tray and global overlay are coming soon.")
    with appearance:
        current = st.session_state.nova_appearance
        def update_appearance():
            values = {k: st.session_state.get("appearance_" + k, current[k]) for k in APPEARANCE_DEFAULTS}
            st.session_state.nova_appearance = UIController(core).save_appearance(values)
        for name, label, low, high in (("glass", "Glass intensity", 20, 90), ("transparency", "Transparency", 20, 90), ("blur", "Blur strength", 0, 24), ("scale", "UI scale", 85, 120)):
            st.slider(label, low, high, value=current[name], key="appearance_" + name, on_change=update_appearance)
        for name, label in (("animation", "Calm animations"), ("orb_effects", "Orb light effects"), ("performance", "Performance mode")):
            st.toggle(label, value=current[name], key="appearance_" + name, on_change=update_appearance)
        st.caption("Preferences are saved locally. Performance mode removes blur and motion. Your system's reduced-motion preference is always respected.")
    with models:
        st.selectbox("Assistant provider", ["Built-in commands", "Ollama (local)", "Groq (cloud)"], **widget_options("nova_provider"))
        choice = st.session_state.nova_provider
        if choice == "Built-in commands": st.info("Local commands are ready. Choose a model for free-form conversation and planning.")
        elif choice == "Ollama (local)":
            st.text_input("Installed Ollama model", **widget_options("nova_ollama_model"))
            st.caption("Keep Ollama running locally with this model installed. No connection is assumed until a request succeeds.")
        else:
            st.text_input("Groq model", **widget_options("nova_groq_model"))
            st.text_input("Groq API key", type="password", **widget_options("nova_api_key"))
            if os.environ.get("GROQ_API_KEY"): st.caption("An environment key is available; leave the field empty to use it.")
            st.caption("The key stays in this running session and is not saved to the database. Cloud requests need NORMAL mode and PUBLIC or INTERNAL classification.")
            if st.button("Clear API key"):
                st.session_state.nova_clear_key = True
                st.rerun()
    with advanced:
        st.caption("Developer information · optional")
        with st.expander("Runtime details"):
            st.json(core.health())
            st.text(str(core.workspace))
        with st.expander("Recent diagnostic events"):
            st.json(core.events()[:20])
        st.caption("Release 0.2 · automatic updates are not enabled. This interface uses the existing Nova core.")


def palette():
    with st.popover("Quick find", icon=":material/search:"):
        query = st.text_input("Find a workspace", placeholder="Memory, missions, privacy…")
        for page in PAGES:
            if query.casefold() in page.casefold() and st.button(page, key="find_" + page): go(page)
        st.caption("Use Tab to navigate and Enter to open.")


def main():
    try:
        core = get_core(os.environ.get("NOVA_DATA_DIR", ""))
        controller = UIController(core)
        initialize_state(controller)
        apply_theme(st.session_state.nova_appearance, compact=not st.session_state.nova_nav_expanded)
        page = sidebar(core)
        shell_header(core, page)
        if st.session_state.nova_notice:
            st.toast(st.session_state.nova_notice)
            st.session_state.nova_notice = ""
        pages = {"Home": home, "Chat": chat, "Voice": voice, "Missions": missions, "Projects": projects,
                 "Agents": agents, "Memory": memory, "Tools": tools_page, "Integrations": integrations,
                 "Privacy": privacy, "Settings": settings,
                 "Automations": lambda c: unavailable("A little less on your list.", "Routines that will make room for what matters.", "automations", "Create automation"),
                 "Devices": lambda c: unavailable("Your world, connected.", "Your trusted devices will have a home here.", "devices", "Connect a device")}
        pages[page](core)
        if page not in {"Home", "Chat"}: palette()
    except Exception as exc: show_error(exc)


if __name__ == "__main__":
    main()
