"""Nova's local-first dashboard. Run with: streamlit run nova_app.py."""

from __future__ import annotations

import json
import os
import re

import streamlit as st

from nova.core import NovaCore
from nova.providers import BLOCKED_CLASSIFICATIONS, ModelProvider, contains_credentials


st.set_page_config(page_title="NOVA · Personal AI", page_icon="✦", layout="wide")


@st.cache_resource
def get_core(data_dir: str) -> NovaCore:
    # The environment variable is part of the cache key, including in isolated tests.
    return NovaCore(data_dir=data_dir or None)


def initialize_state() -> None:
    defaults = {
        "nova_provider": "Built-in commands",
        "nova_ollama_model": "llama3.2",
        "nova_groq_model": "llama-3.3-70b-versatile",
        "nova_api_key": "",
        "nova_mode": "LOCAL_ONLY",
        "nova_classification": "PERSONAL",
        "nova_language": "si",
        "nova_messages": [],
        "nova_prepared_plan": None,
        "nova_notice": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def show_error(exc: Exception) -> None:
    message = str(exc) or type(exc).__name__
    secret = st.session_state.get("nova_api_key", "")
    if secret:
        message = message.replace(secret, "[redacted]")
    st.error(message[:600])


def selected_provider() -> ModelProvider | None:
    choice = st.session_state.nova_provider
    if choice == "Built-in commands":
        return None
    if choice == "Ollama (local)":
        return ModelProvider(provider="ollama", model=st.session_state.nova_ollama_model)
    if st.session_state.nova_mode != "NORMAL":
        raise ValueError("Groq needs NORMAL mode. Choose it explicitly in the sidebar.")
    if st.session_state.nova_classification not in {"PUBLIC", "INTERNAL"}:
        raise ValueError("Groq only accepts PUBLIC or INTERNAL requests. PERSONAL and SECRET stay local.")
    if not st.session_state.nova_api_key and not os.environ.get("GROQ_API_KEY"):
        raise ValueError("Add your Groq API key in Settings before using the cloud model.")
    return ModelProvider(
        provider="groq",
        model=st.session_state.nova_groq_model,
        api_key=st.session_state.nova_api_key or None,
    )


def is_control_command(text: str) -> bool:
    command = re.sub(r"^nova[\s,]+", "", text.strip(), flags=re.I).strip().casefold().rstrip(".! ")
    return command in {
        "stop", "emergency stop", "/stop", "නවත්වන්න", "නවතින්න",
        "resume", "/resume", "continue", "දිගටම කරගෙන යන්න",
    }


def request_options(text: str = "") -> dict:
    return {
        "provider": None if text.lstrip().startswith("/") or is_control_command(text) else selected_provider(),
        "mode": st.session_state.nova_mode,
        "classification": st.session_state.nova_classification,
        "language": st.session_state.nova_language,
    }


def sidebar(core: NovaCore) -> str:
    with st.sidebar:
        st.markdown("## ✦ NOVA")
        st.caption("ඔබේ පුද්ගලික සහායකයා · Personal AI")
        page = st.radio("Workspace", ["Dashboard", "Chat", "Missions", "Memory", "Settings"])
        st.divider()
        st.selectbox(
            "Operating mode", ["LOCAL_ONLY", "NORMAL", "OFFLINE", "PRIVATE", "READ_ONLY", "DRY_RUN", "SAFE_MODE"],
            key="nova_mode",
        )
        st.caption({
            "LOCAL_ONLY": "Local tools and local models only.",
            "NORMAL": "Cloud models allowed only for PUBLIC or INTERNAL requests.",
            "OFFLINE": "No cloud calls; local Ollama inference remains available.",
            "PRIVATE": "Local inference and tools only.",
            "READ_ONLY": "Read local information without changing data.",
            "DRY_RUN": "Prepare and inspect plans without running tools.",
            "SAFE_MODE": "Read-only local tools; file changes are blocked.",
        }[st.session_state.nova_mode])
        st.selectbox(
            "Request classification", ["PERSONAL", "SECRET", "INTERNAL", "PUBLIC"],
            key="nova_classification",
        )
        st.selectbox(
            "Response language", ["si", "en"], key="nova_language",
            format_func=lambda language: "සිංහල · Sinhala" if language == "si" else "English",
        )
        st.caption("Mode and classification apply to your next chat or planning request.")
        st.divider()
        if core.stopped:
            st.error("Stopped · නවත්වා ඇත")
            if st.button("Resume agent", use_container_width=True):
                core.resume()
                st.rerun()
        else:
            st.success("Agent ready · සූදානම්")
            if st.button("⏹ Emergency stop", type="primary", use_container_width=True):
                core.stop()
                st.rerun()
        st.caption("Stop blocks new work and pauses the queue. A file operation already in progress may finish safely.")
        st.caption("NOVA · Local-first workspace")
    return page


def dashboard(core: NovaCore) -> None:
    st.title("හෙලෝ, මම NOVA ✦")
    st.markdown("Your personal workspace for **conversation, useful tasks, and lasting memory**.")
    missions = core.missions()
    memories = core.memories()
    one, two, three = st.columns(3)
    one.metric("Missions", len(missions))
    two.metric("Saved memories", len(memories))
    three.metric("Privacy mode", st.session_state.nova_mode)
    left, right = st.columns([3, 2])
    with left:
        with st.container(border=True):
            st.subheader("Start with one useful thing")
            st.write("Open Chat to use a command, or prepare a task in Missions and review its steps before running it.")
            st.code("/help\n/files\n/write notes.txt | අද කළ යුතු වැඩ\n/remember preferred_language = Sinhala", language="text")
            st.caption("Built-in commands work without a model. Natural-language conversation needs a configured model in Settings.")
        st.subheader("Recent activity")
        events = core.events()
        if not events:
            st.info("Your workspace is ready. Activity will appear as you use Nova.")
        for event in events[:8]:
            with st.expander(f"{event.get('kind', 'Event')} · {event.get('created_at', '')}"):
                st.json(event)
    with right:
        with st.container(border=True):
            st.subheader("Available now")
            st.write("✓ Workspace file tools\n\n✓ Reviewed mission plans\n\n✓ Persistent explicit memory\n\n✓ Activity history and emergency stop")
            st.caption("A configured local Ollama server or a Groq API key enables model responses. Voice, browser control, and external account integrations are not connected in this release.")
        with st.expander("Runtime health"):
            st.json(core.health())
            st.caption(f"Workspace: {core.workspace}")
        with st.expander("Registered tools"):
            for tool in core.tools():
                st.write(f"**{tool['name']}** — {tool.get('description', '')}")
                if tool.get("mutating"):
                    st.caption("Changes local data")


def chat(core: NovaCore) -> None:
    st.title("කතා කරමු · Chat")
    st.caption(f"{st.session_state.nova_provider} · {st.session_state.nova_mode} · {st.session_state.nova_classification}")
    with st.expander("Command guide"):
        st.code(
            "/help\n/files\n/read notes.txt\n/write notes.txt | Text to save\n"
            "/remember name = Your name\n/recall\n/status\n/stop\n/resume",
            language="text",
        )
        st.caption("File-writing commands request a real local action. For a multi-step task, review a plan in Missions first.")
    if st.button("Clear this conversation"):
        st.session_state.nova_messages = []
        st.rerun()
    st.caption("Conversation display lasts for this browser session. Save lasting facts explicitly in Memory.")
    for message in st.session_state.nova_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    text = st.chat_input("Type /resume to continue" if core.stopped else "ඔබට අවශ්‍ය දේ කියන්න… /help")
    if text:
        if contains_credentials(text) or (st.session_state.nova_classification in BLOCKED_CLASSIFICATIONS and not is_control_command(text)):
            st.warning("This request was withheld because it contains credential-like data or has a protected classification. It was not added to conversation history.")
            return
        if core.stopped and not is_control_command(text):
            st.info("The agent is stopped. Type /resume or use Resume agent to continue.")
            return
        st.session_state.nova_messages.append({"role": "user", "content": text})
        with st.chat_message("user"):
            st.write(text)
        with st.chat_message("assistant"):
            try:
                with st.spinner("NOVA is thinking…"):
                    was_stopped = core.stopped
                    answer = core.chat(text, **request_options(text))
                st.write(answer)
                st.session_state.nova_messages.append({"role": "assistant", "content": answer})
                if was_stopped != core.stopped:
                    st.rerun()
            except Exception as exc:
                show_error(exc)


def mission_planner(core: NovaCore) -> None:
    with st.container(border=True):
        st.subheader("Prepare a mission")
        st.caption("Describe a goal, inspect the proposed tools and arguments, then choose whether to run it.")
        with st.form("prepare_mission"):
            goal = st.text_area("What should Nova do?", placeholder="/write welcome.txt | ආයුබෝවන්!")
            prepare = st.form_submit_button("Prepare plan", disabled=core.stopped)
        if prepare:
            st.session_state.nova_prepared_plan = None
            try:
                if not goal.strip():
                    raise ValueError("Enter a goal or a built-in command first.")
                with st.spinner("Preparing steps…"):
                    steps = core.plan(goal, **request_options(goal))
                st.session_state.nova_prepared_plan = steps
            except Exception as exc:
                show_error(exc)
        steps = st.session_state.nova_prepared_plan
        if steps:
            st.markdown("**Review your plan**")
            for index, step in enumerate(steps, 1):
                st.write(f"{index}. **{step.get('tool', 'Unknown tool')}**")
                st.code(json.dumps(step.get("args", {}), ensure_ascii=False, indent=2), language="json")
            st.caption("Running this plan submits the displayed steps to the local mission queue.")
            run, discard = st.columns(2)
            if run.button("Run prepared plan", type="primary", disabled=core.stopped or st.session_state.nova_mode == "DRY_RUN"):
                try:
                    ids = core.submit_plan(steps, mode=st.session_state.nova_mode)
                    st.session_state.nova_prepared_plan = None
                    st.session_state.nova_notice = f"Queued {len(ids)} mission step(s). Refresh to see progress."
                    st.rerun()
                except Exception as exc:
                    show_error(exc)
            if discard.button("Discard plan"):
                st.session_state.nova_prepared_plan = None
                st.rerun()


def missions(core: NovaCore) -> None:
    st.title("මෙහෙයුම් · Missions")
    mission_planner(core)
    st.subheader("Mission history")
    if st.button("Refresh mission status"):
        st.rerun()
    rows = core.missions()
    if not rows:
        st.info("No missions yet. Prepare your first task above.")
    for mission in rows:
        label = f"{mission.get('status', 'unknown').upper()} · {mission.get('tool', '')} · {mission.get('id', '')[:8]}"
        with st.expander(label):
            st.write(mission.get("goal", ""))
            st.caption(f"Created: {mission.get('created_at', '')}")
            st.json(mission.get("args", {}))
            if mission.get("result") is not None:
                st.markdown("**Result**")
                st.write(mission["result"])
            if mission.get("error"):
                st.error(mission["error"])
            if mission.get("tool") in {"files.create", "write_file"} and mission.get("status", "").lower() in {"completed", "succeeded", "done"}:
                st.caption("Undo removes a created file only if it has not changed since the mission.")
                if st.button("Undo file write", key=f"undo_{mission['id']}", disabled=(
                    core.stopped or st.session_state.nova_mode in {"READ_ONLY", "DRY_RUN", "SAFE_MODE"}
                )):
                    try:
                        st.success(core.undo(mission["id"], mode=st.session_state.nova_mode))
                    except Exception as exc:
                        show_error(exc)


def memory(core: NovaCore) -> None:
    st.title("මතකය · Memory")
    st.caption("Keep facts you explicitly choose to save. Memory persists locally across restarts.")
    with st.form("remember"):
        key = st.text_input("Memory name", placeholder="preferred_language")
        value = st.text_area("Value", placeholder="Sinhala")
        scope = st.selectbox("Memory scope", ["PERSONAL", "GLOBAL", "PROJECT"])
        st.caption("All memories stay in local storage. Do not save passwords or API keys here.")
        save = st.form_submit_button(
            "Save memory", disabled=core.stopped or st.session_state.nova_mode in {"READ_ONLY", "DRY_RUN", "SAFE_MODE"},
        )
    if save:
        try:
            if not key.strip() or not value.strip():
                raise ValueError("Provide both a memory name and a value.")
            core.remember(key.strip(), value.strip(), scope=scope, mode=st.session_state.nova_mode)
            st.success("Memory saved locally.")
        except Exception as exc:
            show_error(exc)
    query = st.text_input("Search memories")
    rows = core.memories(query=query)
    if not rows:
        st.info("No matching memories.")
    for item in rows:
        with st.expander(f"{item['key']} · {item.get('scope', 'PERSONAL')}"):
            st.write(item["value"])
            st.caption(f"Source: {item.get('source', 'explicit')} · Updated: {item.get('updated_at', '')}")
            confirm = st.checkbox("Delete this saved fact", key=f"confirm_{item['id']}")
            if st.button("Forget", key=f"forget_{item['id']}", disabled=(
                not confirm or core.stopped or st.session_state.nova_mode in {"READ_ONLY", "DRY_RUN", "SAFE_MODE"}
            )):
                try:
                    core.forget(item["id"], mode=st.session_state.nova_mode)
                    st.rerun()
                except Exception as exc:
                    show_error(exc)


def settings(core: NovaCore) -> None:
    st.title("සැකසුම් · Settings")
    st.subheader("Model connection")
    # Keep configuration separate from widget state: Streamlit discards widgets
    # when their page is hidden, but the chosen provider must survive navigation.
    def preserve(key: str) -> None:
        st.session_state[key] = st.session_state[f"widget_{key}"]

    def widget_options(key: str) -> dict:
        st.session_state[f"widget_{key}"] = st.session_state[key]
        return {"key": f"widget_{key}", "on_change": preserve, "args": (key,)}

    st.selectbox("Assistant provider", ["Built-in commands", "Ollama (local)", "Groq (cloud)"], **widget_options("nova_provider"))
    choice = st.session_state.nova_provider
    if choice == "Built-in commands":
        st.info("Ready without credentials. Use the documented slash commands; general model conversation is disabled.")
    elif choice == "Ollama (local)":
        st.text_input("Installed Ollama model", **widget_options("nova_ollama_model"))
        st.info("Ollama must be running locally with this model installed. A model request verifies the connection.")
    else:
        st.text_input("Groq model", **widget_options("nova_groq_model"))
        st.text_input("Groq API key", type="password", **widget_options("nova_api_key"))
        if os.environ.get("GROQ_API_KEY"):
            st.caption("A GROQ_API_KEY environment binding is available. Leave the field empty to use it.")
        st.warning("Groq sends your request to a cloud provider. Enable NORMAL mode and explicitly classify the request PUBLIC or INTERNAL before using it.")
        st.caption("This key stays in the running browser session state; Nova does not save it to its database or files.")
        if st.button("Clear API key"):
            # A widget's value cannot be changed after it has been instantiated.
            st.session_state.nova_clear_key = True
            st.rerun()
    st.divider()
    st.subheader("Local workspace")
    st.code(str(core.workspace), language="text")
    st.caption("File tools are confined to this workspace. Set NOVA_DATA_DIR before startup to choose a different data location.")
    st.subheader("Connection status")
    st.json(core.health())
    st.caption("Provider selection does not establish a connection. Model availability is checked when you send a request.")


def main() -> None:
    initialize_state()
    if st.session_state.pop("nova_clear_key", False):
        st.session_state.nova_api_key = ""
    st.markdown(
        """<style>
        .stApp { background: #0c111b; color: #e7eaf3; }
        [data-testid="stSidebar"] { background: #111827; }
        [data-testid="stMetric"] { background: #151e2e; border: 1px solid #273246;
          border-radius: 14px; padding: 18px; }
        h1, h2, h3 { letter-spacing: -0.025em; }
        .block-container { max-width: 1220px; padding-top: 2.4rem; }
        [data-testid="stCaptionContainer"] { color: #a8b3c7; }
        [data-testid="stChatMessage"] { background: #151e2e; }
        </style>""",
        unsafe_allow_html=True,
    )
    try:
        core = get_core(os.environ.get("NOVA_DATA_DIR", ""))
        page = sidebar(core)
        if st.session_state.nova_notice:
            st.success(st.session_state.nova_notice)
            st.session_state.nova_notice = ""
        {"Dashboard": dashboard, "Chat": chat, "Missions": missions, "Memory": memory, "Settings": settings}[page](core)
    except Exception as exc:
        show_error(exc)


if __name__ == "__main__":
    main()
