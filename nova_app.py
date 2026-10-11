"""NOVA Glass: a local desktop-style interface around the existing Nova core."""
from __future__ import annotations

import json
import os
import re
from html import escape

import streamlit as st

from nova import __version__
from nova.core import NovaCore, NovaError
from nova.catalog import STATUSES, coverage
from nova.local_commands import local_intent
from nova.providers import BLOCKED_CLASSIFICATIONS, ModelProvider, contains_credentials
from nova.ui.controller import (APPEARANCE_DEFAULTS, ACCENTS, PAGES, PRIMARY_PAGES, ORB_STATES, UIController,
                                assistant_state, greeting, mission_group, elapsed_label)
from nova.ui.glass import apply_theme, orb, header, badge, empty_state, icon

st.set_page_config(page_title="NOVA · Glass", page_icon="✦", layout="wide", initial_sidebar_state="expanded")


@st.cache_resource
def get_core(data_dir: str) -> NovaCore:
    return NovaCore(data_dir=data_dir or None)


def initialize_state(controller):
    defaults = {
        "nova_page": "Chat", "nova_primary_page": "Chat", "nova_nav_expanded": False,
        "nova_provider": "Built-in commands", "nova_ollama_model": "llama3.2",
        "nova_groq_model": "llama-3.3-70b-versatile",
        "nova_mode": "LOCAL_ONLY", "nova_classification": "PERSONAL", "nova_language": "auto",
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
        st.session_state.nova_primary_page = st.session_state.nova_page if st.session_state.nova_page in PRIMARY_PAGES else "Settings"
    # Discard any legacy session credential when upgrading a running UI.
    st.session_state.pop("nova_api_key", None)
    st.session_state.pop("widget_nova_api_key", None)
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
    if contains_credentials(message):
        message = "The action was stopped because sensitive information was detected."
    st.error(message)


PROVIDER_CHOICES = {"Built-in commands": None, "OpenAI / GPT": "openai", "Google Gemini": "gemini",
                    "Ollama (local)": "ollama", "Groq (cloud)": "groq"}
PROVIDER_MODELS = {"openai": "gpt-4.1-mini", "gemini": "gemini-2.5-flash", "ollama": "llama3.2", "groq": "llama-3.3-70b-versatile"}


def selected_provider():
    provider = PROVIDER_CHOICES[st.session_state.nova_provider]
    if provider is None:
        return None
    if provider != "ollama" and st.session_state.nova_mode != "NORMAL":
        raise NovaError("Cloud AI needs NORMAL mode. Choose it explicitly in Settings → General.")
    if provider != "ollama" and st.session_state.nova_classification not in {"PUBLIC", "INTERNAL"}:
        raise NovaError("Cloud requests need PUBLIC or INTERNAL classification. Personal content stays local.")
    return get_core(os.environ.get("NOVA_DATA_DIR", "")).provider_hub.client(provider)


def is_control_command(text):
    value = re.sub(r"^nova[\s,]+", "", text.strip(), flags=re.I).strip().casefold().rstrip(".! ")
    return value in {"stop", "emergency stop", "/stop", "නවත්වන්න", "නවතින්න",
                     "resume", "/resume", "continue", "දිගටම කරගෙන යන්න"}


def request_options(text=""):
    return {"provider": None if text.lstrip().startswith("/") or is_control_command(text) or local_intent(text) else selected_provider(),
            "mode": st.session_state.nova_mode, "classification": st.session_state.nova_classification,
            "language": st.session_state.nova_language}


def changes_allowed(core):
    return not core.stopped and st.session_state.nova_mode not in {"READ_ONLY", "DRY_RUN", "SAFE_MODE"}


def sidebar(core):
    with st.sidebar:
        st.html('<div class="nova-brand">' + icon("sparkles", 28) + '<span>NOVA<small>PERSONAL INTELLIGENCE</small></span></div>')
        def select_primary():
            st.session_state.nova_page = st.session_state.nova_primary_page
        st.radio("Workspace", PRIMARY_PAGES, key="nova_primary_page", on_change=select_primary, label_visibility="collapsed")
        page = st.session_state.nova_page
        with st.popover("Appearance", icon=":material/palette:"):
            current = st.session_state.nova_appearance
            accent = st.selectbox("Accent colour", list(ACCENTS), index=list(ACCENTS).index(current["accent"]))
            if accent != current["accent"]:
                st.session_state.nova_appearance = UIController(core).save_appearance({**current, "accent": accent})
                st.rerun()
        if core.stopped:
            if st.button("Resume agent", icon=":material/play_arrow:", use_container_width=True):
                core.resume()
                st.rerun()
        elif st.button("Emergency stop", icon=":material/stop_circle:", use_container_width=True, help="Pause new work. An atomic file operation already running may finish safely."):
            core.stop()
            st.rerun()
        st.html('<div class="nova-sidebar-foot">' + icon("shield", 14) + ' Local workspace · v' + __version__ + '</div>')
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
            if page not in {"Chat", "Voice"}: st.html('<div class="nova-kicker">YOUR SPACE, INTELLIGENTLY CONNECTED</div><div class="nova-breadcrumb">NOVA <span>/</span> ' + escape(page) + '</div>')
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
        st.divider()
        st.write("Read image text")
        health = core.vision.health()
        st.caption("Local OCR only. This does not interpret images or capture your screen. Extracted text is not saved to conversation history.")
        if not health["available"]: st.caption(health["detail"])
        image_upload = st.file_uploader("Image for local OCR", type=["png", "jpg", "jpeg"], max_upload_size=8, key="nova_ocr_upload")
        languages = health.get("languages") or ["eng"]
        language = st.selectbox("OCR language", languages)
        if st.button("Read image text", disabled=image_upload is None or not health["available"] or core.stopped):
            try:
                receipt = core.inspect_image(image_upload.getvalue(), language=language, mode=st.session_state.nova_mode, classification=st.session_state.nova_classification)
                st.caption("Local OCR · " + receipt["engine"])
                st.text(receipt["text"] or "No text found in this image.")
            except Exception as exc: show_error(exc)
        for name in ("Document / PDF", "Screenshot", "Folder", "Clipboard"):
            st.button(name + " · coming soon", disabled=True, key="attachment_" + name)


def composer(core):
    with st.bottom:
        with st.container(key="floating-composer"):
            attach, message, microphone = st.columns([1.1, 7, 1], vertical_alignment="center")
            with attach: attachment_menu(core)
            with message:
                text = st.chat_input("Resume NOVA to continue" if core.stopped else "Message NOVA…", key="nova_composer", max_chars=20_000)
            with microphone:
                if st.button("Voice", icon=":material/mic:", help="Open voice workspace; speech engine not connected", key="composer_voice"):
                    go("Voice")
            if text: receive_message(core, text)



def chat(core):
    switch_assistant("Chat")
    if st.session_state.nova_messages:
        with st.popover("Conversation options"):
            if st.button("Clear this conversation"):
                st.session_state.nova_messages = []
                st.rerun()
            st.caption("Conversation is session-only. Save lasting facts in Memory.")
    else:
        with st.container(key="chat-welcome"):
            orb("privacy" if st.session_state.nova_mode != "NORMAL" else "idle", 230, "Ready when you are")
            header(greeting(st.session_state.nova_language), "අද මම ඔබට උදව් කරන්නේ කොහොමද?" if st.session_state.nova_language == "si" else "What can I help you with today?")
    for message in st.session_state.nova_messages:
        with st.chat_message(message["role"], avatar=":material/person:" if message["role"] == "user" else ":material/auto_awesome:"):
            st.write(message["content"])
    composer(core)


def voice(core):
    switch_assistant("Voice")
    orb("offline", 300, "Voice unavailable")
    st.markdown('<p class="nova-voice-unavailable">Voice unavailable</p>', unsafe_allow_html=True)
    left, center, right = st.columns([1, 1, 1])
    with center:
        if st.button("Voice setup", icon=":material/settings_voice:", use_container_width=True): go("Settings")
        if st.button("Continue in Chat", icon=":material/chat_bubble:", use_container_width=True): go("Chat")


def plan_details(steps):
    for index, step in enumerate(steps, 1):
        st.markdown(f"**{index}. {step['goal']}**")
        path = step["args"].get("path")
        if path: st.write("File: " + path)
        if 'name' in step['args']: st.write('Application: ' + step['args']['name'])
        if 'site' in step['args']: st.write('Official website: ' + step['args']['site'])
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
    desktop_action = any(s['tool'] in {'apps.open', 'web.open'} for s in steps)
    st.write("**Target:** installed Windows application / official website" if desktop_action else "**Target:** your local Nova workspace")
    st.write("**Data leaving this device:** launched apps and browsers use their own network settings; NOVA does not control their traffic." if desktop_action else "**Data leaving this device:** none during tool execution")
    st.write("**Cost:** no API call or payment during execution")
    st.write("**Reversibility:** app launches and website handoffs have no automatic undo. Browser page loading is not verified by the launcher." if desktop_action else "**Reversibility:** new files can be undone while their contents remain unchanged. Existing files are never overwritten.")
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
    if "application" in result: st.write("Application: " + result['application'])
    if "verification" in result: st.caption(result['verification'])
    if result.get('state') == 'CHECK_BROWSER': st.write("Website request handed to your browser. Check that the correct page loaded.")


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
    view = st.segmented_control("Project view", ["Workspace", "Decision memory"], default="Workspace", required=True)
    if view == "Decision memory":
        decision_panel(core)
        return
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


def decision_panel(core):
    st.subheader("Remember why you chose it.")
    st.caption("Owner-entered decisions stay local. Project names are labels; they do not create or link folders. Records are never automatically sent to a model.")
    with st.expander("Record a decision"):
        with st.form("new_decision", clear_on_submit=True):
            project = st.text_input("Project label", max_chars=100)
            decision = st.text_area("Decision", max_chars=20000)
            reason = st.text_area("Reason", max_chars=20000)
            alternatives = st.text_area("Alternatives considered (optional)", max_chars=20000)
            st.caption("Local SQLite is not an encrypted vault. Do not enter credentials.")
            save = st.form_submit_button("Save decision", disabled=not changes_allowed(core))
        if save:
            try:
                core.save_decision(project, decision, reason, alternatives, mode=st.session_state.nova_mode)
                st.success("Decision saved locally.")
            except Exception as exc: show_error(exc)
    query = st.text_input("Search decisions", max_chars=200, placeholder="Project, decision, reason or alternative…")
    project_filter = st.text_input("Exact project label (optional)", max_chars=100)
    records = core.decisions(query, project_filter)
    if not records:
        empty_state("No recorded decisions.", "Save the reason behind an important choice. NOVA will retrieve that record instead of inventing an explanation.", "memory")
    st.caption("Up to 100 matching decisions, newest first. Dates are UTC. Deletion is logical, not secure erasure.")
    for item in records:
        with st.expander(f"{item['project']} · {item['decision'][:90]}"):
            st.write(item["decision"])
            st.markdown("**Recorded reason**")
            st.write(item["reason"])
            st.markdown("**Alternatives considered**")
            st.write(item["alternatives"] or "Not recorded")
            st.caption(f"Owner-entered · Created {item['created_at'][:19]} UTC · Updated {item['updated_at'][:19]} UTC · Revision {item['revision']}")
            key = f"decision_{item['id']}_{item['revision']}"
            with st.form("edit_" + key):
                project = st.text_input("Edit project label", item["project"], max_chars=100)
                decision = st.text_area("Edit decision", item["decision"], max_chars=20000)
                reason = st.text_area("Edit reason", item["reason"], max_chars=20000)
                alternatives = st.text_area("Edit alternatives", item["alternatives"], max_chars=20000)
                edit = st.form_submit_button("Save changes", disabled=not changes_allowed(core))
            if edit:
                try:
                    core.save_decision(project, decision, reason, alternatives, decision_id=item["id"], revision=item["revision"], mode=st.session_state.nova_mode)
                    st.session_state.nova_notice = "Decision updated."
                    st.rerun()
                except Exception as exc: show_error(exc)
            confirm = st.checkbox("Delete this decision", key="confirm_" + key)
            if st.button("Forget decision", key="delete_" + key, disabled=not confirm or not changes_allowed(core)):
                try:
                    core.forget_decision(item["id"], item["revision"], mode=st.session_state.nova_mode)
                    st.session_state.nova_notice = "Decision removed from local records."
                    st.rerun()
                except Exception as exc: show_error(exc)


def agents(core):
    header("A small team. A shared purpose.", "Specialists with clear responsibilities and bounded permissions.", "YOUR AGENTS")
    cards = UIController(core).agents()
    columns = st.columns(2)
    for index, agent in enumerate(cards):
        column = columns[index % 2]
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
    view = st.segmented_control("Tools view", ["Installed tools", "Feature coverage"], default="Installed tools", required=True)
    if view == "Feature coverage":
        coverage_panel(core)
        return
    query = st.text_input("Find a capability", placeholder="Files, text, system information…")
    capabilities = {item["capability_id"]: item for item in core.capabilities()}
    names = {"files.list": ("Browse your files", "List the files in your Nova workspace.", {}),
             "files.read": ("Read text", "Read a UTF-8 file from your workspace.", None),
             "files.create": ("Create a file", "Write a new file without overwriting existing work.", None),
             "system.info": ("System information", "Check your OS and Python runtime.", {})}
    for tool in core.tools():
        title, description, args = names.get(tool['name'], (tool['name'].replace('.', ' ').title(), tool['description'], None))
        if query.casefold() not in (title + " " + description + " " + tool["name"]).casefold():
            continue
        with st.container(border=True):
            st.html(badge("EXTERNAL WEBSITE" if tool['name'] == 'web.open' else "LOCAL", "blue"))
            st.subheader(title)
            st.write(description)
            capability = capabilities[tool["name"]]
            with st.expander("Scope & verification"):
                st.write("Agent: " + capability["required_agents"][0].replace("-", " ").title())
                st.write(capability["verification_method"])
                st.caption(capability['privacy_level'].replace('_', ' ').title() + " · " + capability["risk_level"].replace("_", " ").lower())
            if args is not None:
                if st.button("Run " + title.lower(), key="tool_" + tool["name"], disabled=core.stopped or st.session_state.nova_mode == "DRY_RUN"):
                    core.enqueue(tool["name"], args, title, mode=st.session_state.nova_mode)
                    go("Missions")
            elif st.button("Prepare " + title.lower(), key="tool_" + tool["name"]): go("Missions")


def coverage_panel(core):
    st.subheader("What works. What comes next.")
    counts = coverage()
    a, b, c = st.columns(3)
    a.metric("Working expansion features", counts.get("WORKING", 0))
    b.metric("Partial expansion features", counts.get("PARTIAL", 0))
    c.metric("Not started", counts.get("NOT_STARTED", 0))
    st.caption("Counts cover 128 expansion features. Four governance requirements and existing runtime tools are listed separately. Partial scope is stated for each record; evidence references are not live test runs.")
    query = st.text_input("Search feature catalog", max_chars=200, placeholder="WhatsApp, Blender, decision, EXP-017…")
    left, right = st.columns(2)
    status = left.selectbox("Feature status", ["ALL", *STATUSES])
    kind = right.selectbox("Catalog type", ["All", "tool", "agent", "provider", "feature", "guidance"])
    records = [r for r in core.feature_catalog(query, status, st.session_state.nova_mode) if kind == "All" or r["kind"] == kind]
    st.caption(f"{len(records)} matches · Showing up to 25; narrow your search for more. No connection checks or installations run during search.")
    if not records: st.info("No recorded match. Missing evidence does not establish support.")
    for item in records[:25]:
        with st.expander(f"{item['title']} · {item['status']} · {item['id']}"):
            st.html(badge(item["availability"], "blue" if item["availability"] in {"AVAILABLE", "AVAILABLE_IN_UI"} else "neutral"))
            st.write(item["scope"])
            st.caption(f"{item['category']} · {item['kind']} · Roadmap phase {item['phase']}")
            st.write("Dependencies / permissions: " + ", ".join(item["dependencies"]))
            st.write("Implementation: " + (", ".join(item["implementation"]) or "Not implemented"))
            st.write("Test references: " + (", ".join(item["tests"]) or "No implementation tests yet"))
            st.caption(f"Source: {item['source']} · Documented in release: {item['release'] or 'Future'}")
    st.info("Auto-reply: OFF. Messaging transports are not installed. Catalog records cannot enable tools, integrations or permissions.")


def integrations(core):
    header("Connected, on your terms.", "Choose what NOVA can use. Nothing connects without your setup.", "INTEGRATIONS")
    for item in core.provider_hub.providers():
        with st.container(border=True):
            health = item["health"]
            st.subheader(next(label for label, name in PROVIDER_CHOICES.items() if name == item["provider"]))
            st.html(badge(health["status"], "blue" if health["status"] == "CONNECTED" else "neutral"))
            st.caption(health["detail"])
            if st.button("Configure", key="integration_" + item["provider"]): go("Settings")
    st.markdown("**On the horizon**")
    for name in ("Browser", "GitHub", "Email & calendar", "WhatsApp", "Blender & Unreal", "Smart home"):
        st.html('<div class="nova-integration-row"><span>' + escape(name) + '</span>' + badge("DISCONNECTED", "neutral") + '</div>')
    st.caption("Auto-reply is OFF. OFF, DRAFT_ONLY, ASK_BEFORE_SEND, TRUSTED_CONTACTS, AWAY_MODE and SMART_AUTO are roadmap modes; none can send messages in this release.")


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
            for event in activity[:10]: st.write("Cloud response received · " + event["created_at"][:16].replace("T", " ") + " UTC")
        else: st.write("No successful cloud responses recorded in the recent activity window.")
        st.caption("This history covers the last 200 Nova events. It does not record every attempted request or monitor other apps on your computer.")
    a, b = st.columns(2)
    with a:
        st.subheader("Protected files")
        st.write("File tools stay inside your dedicated Nova workspace. Existing files are never overwritten.")
    with b:
        st.subheader("Private by default")
        st.write("Memory and file history are not automatically sent to a model. Sensitive classifications and common credential patterns are blocked.")
    st.caption("Per-app protection, custom folder policies, a full network ledger and cross-platform secret storage are coming soon. Windows provider keys use the OS-backed vault.")


def widget_options(key):
    def preserve(): st.session_state[key] = st.session_state["widget_" + key]
    st.session_state["widget_" + key] = st.session_state[key]
    return {"key": "widget_" + key, "on_change": preserve}


def provider_settings(core):
    hub = core.provider_hub
    st.subheader("AI providers")
    st.selectbox("Assistant provider", list(PROVIDER_CHOICES), **widget_options("nova_provider"))
    st.caption("Local commands work without an AI provider. Cloud AI requires your explicit privacy choices in General.")
    if not hub.vault_available:
        st.info("Secure key storage is unavailable on this platform. Cloud keys can only be saved with the Windows-backed vault. Local AI remains available.")
    for label, provider in PROVIDER_CHOICES.items():
        if provider is None: continue
        with st.container(border=True):
            st.subheader(label)
            status = hub.status(provider)
            st.html(badge(status.get("status", "DISCONNECTED"), "blue" if status.get("status") == "CONNECTED" else "neutral"))
            if status.get("detail"): st.caption(status["detail"])
            if status.get("checked_at"): st.caption("Last check: " + str(status["checked_at"]))
            model_key = "provider_model_" + provider
            secret_key = "provider_secret_" + provider
            def save_provider(provider=provider, model_key=model_key, secret_key=secret_key):
                # Widget data is consumed only by this callback and cleared before rerender.
                secret = st.session_state.pop(secret_key, None)
                try:
                    hub.configure(provider, st.session_state[model_key], key=secret or None)
                    st.session_state.nova_notice = "Provider saved. Use Check connection to verify it."
                except Exception:
                    st.session_state.nova_notice = "Provider could not be saved. Check the model and secure storage availability."
                finally:
                    secret = None
            with st.form("provider_setup_" + provider, clear_on_submit=True):
                st.text_input("Model", value=next((item["model"] for item in hub.providers() if item["provider"] == provider), None) or PROVIDER_MODELS[provider], key=model_key)
                if provider != "ollama":
                    st.text_input("New API key", type="password", key=secret_key, disabled=not hub.vault_available,
                                  help="Enter only here on your local computer. The field is cleared when you save.")
                st.form_submit_button("Save provider", key="save_" + provider, on_click=save_provider,
                                      disabled=provider != "ollama" and not hub.vault_available)
            check, forget = st.columns(2)
            if check.button("Check connection", key="check_" + provider, disabled=core.stopped or (provider != "ollama" and st.session_state.nova_mode != "NORMAL")):
                try:
                    hub.check(provider, mode=st.session_state.nova_mode)
                    st.rerun()
                except Exception as exc: show_error(exc)
            def forget_provider(provider=provider, secret_key=secret_key):
                st.session_state.pop(secret_key, None)
                try:
                    hub.forget(provider)
                    st.session_state.nova_notice = "Provider credential forgotten."
                except Exception:
                    st.session_state.nova_notice = "Provider credential could not be removed."
            forget.button("Forget provider", key="forget_" + provider, on_click=forget_provider)
            st.caption("Connection checks contact this provider only when you press Check connection. A saved configuration is not a verified connection.")


def settings(core):
    header("Make a little space for you.", "Your preferences, your models, your way of working.", "SETTINGS")
    general, appearance, models, advanced = st.tabs(["General", "Appearance", "AI", "Advanced"])
    with general:
        st.subheader("NOVA Glass White")
        st.write("A quiet, light workspace for your personal AI.")
        st.selectbox("Operating mode", ["LOCAL_ONLY", "NORMAL", "OFFLINE", "PRIVATE", "READ_ONLY", "DRY_RUN", "SAFE_MODE"], **widget_options("nova_mode"))
        st.selectbox("Request classification", ["PERSONAL", "SECRET", "PRIVATE", "INTERNAL", "PUBLIC"], **widget_options("nova_classification"))
        st.selectbox("Response language", ["auto", "si", "en", "singlish"], **widget_options("nova_language"), format_func=lambda v: {"auto": "Match my message", "si": "සිංහල · Sinhala", "en": "English", "singlish": "Singlish"}[v])
        st.caption("These choices apply to new requests. Running missions keep their approved scope.")
        st.info("Voice unavailable. Microphone capture and speech are not implemented. Notification schedules, system tray and global overlay are coming soon.")
    with appearance:
        current = st.session_state.nova_appearance
        def update_appearance():
            values = {k: st.session_state.get("appearance_" + k, current[k]) for k in APPEARANCE_DEFAULTS}
            st.session_state.nova_appearance = UIController(core).save_appearance(values)
        st.selectbox('Accent', list(ACCENTS), index=list(ACCENTS).index(current['accent']), key='appearance_accent', on_change=update_appearance)
        for name, label, low, high in (("glass", "Glass intensity", 20, 90), ("transparency", "Transparency", 20, 90), ("blur", "Blur strength", 0, 24), ("scale", "UI scale", 85, 120)):
            st.slider(label, low, high, value=current[name], key="appearance_" + name, on_change=update_appearance)
        for name, label in (("animation", "Calm animations"), ("orb_effects", "Orb light effects"), ("performance", "Performance mode")):
            st.toggle(label, value=current[name], key="appearance_" + name, on_change=update_appearance)
        st.caption("Preferences are saved locally. Performance mode removes blur and motion. Your system's reduced-motion preference is always respected.")
    with models:
        provider_settings(core)
    with advanced:
        st.subheader("Advanced workspaces")
        st.caption("The full mission, tool and privacy workspaces remain available here.")
        columns = st.columns(2)
        for index, page in enumerate(p for p in PAGES if p not in PRIMARY_PAGES):
            if columns[index % 2].button("Open " + page, key="advanced_" + page, use_container_width=True): go(page)
        st.caption("Developer information · optional")
        with st.expander("Runtime details"):
            st.json(core.health())
            st.text(str(core.workspace))
        with st.expander("Recent diagnostic events"):
            st.json(core.events()[:20])
        st.caption("Release 0.3 · automatic updates are not enabled. This interface uses the existing Nova core.")


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
        apply_theme(st.session_state.nova_appearance, compact=True)
        page = sidebar(core)
        shell_header(core, page)
        if page not in PRIMARY_PAGES:
            if st.button("Back to Settings", icon=":material/arrow_back:"): go("Settings")
        if st.session_state.nova_notice:
            st.toast(st.session_state.nova_notice)
            st.session_state.nova_notice = ""
        pages = {"Home": home, "Chat": chat, "Voice": voice, "Missions": missions, "Projects": projects,
                 "Agents": agents, "Memory": memory, "Tools": tools_page, "Integrations": integrations,
                 "Privacy": privacy, "Settings": settings,
                 "Automations": lambda c: unavailable("A little less on your list.", "Routines that will make room for what matters.", "automations", "Create automation"),
                 "Devices": lambda c: unavailable("Your world, connected.", "Your trusted devices will have a home here.", "devices", "Connect a device")}
        pages[page](core)
        if page not in {"Home", "Chat", "Voice"}: palette()
    except Exception as exc: show_error(exc)


if __name__ == "__main__":
    main()
