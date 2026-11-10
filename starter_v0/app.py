
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import streamlit as st

from chat import (
    ARTIFACTS_DIR,
    ROOT,
    artifact_version_dict,
    build_artifact_version,
    load_tool_declarations,
    make_provider,
    now_iso,
    to_openai_tools,
    run_model_tool_loop,
    safe_slug,
    trim_history,
    write_transcript,
)

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Research Agent Platform",
    page_icon="🔎",
    layout="wide",
)

TRANSCRIPTS_DIR = ROOT / "transcripts"
SYSTEM_PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"

PROVIDERS = ["openrouter", "openai", "anthropic", "gemini", "ollama"]


# --------------------------------------------------
# Backend initialization
# --------------------------------------------------

@st.cache_resource
def get_provider(provider_name: str):
    return make_provider(provider_name)


def initialize_chat(provider_name: str, model: str, version: str,
                    history_window: int, max_tool_rounds: int):

    artifact_version = build_artifact_version(
        version,
        SYSTEM_PROMPT_PATH,
        TOOLS_PATH,
    )

    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join([
        safe_slug(version),
        safe_slug(provider_name),
        timestamp,
    ])

    transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": model,
        "system_prompt": str(SYSTEM_PROMPT_PATH),
        "tools": str(TOOLS_PATH),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }

    return {
        "history": [],
        "transcript": transcript,
        "transcript_path": TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json",
        "turn_index": 0,
    }


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("🔎 Research Agent")
st.sidebar.caption("Agent Tool Evaluation Platform")

provider_name = st.sidebar.selectbox(
    "Provider",
    PROVIDERS,
    index=0,
)

provider = get_provider(provider_name)
default_model = getattr(provider, "default_model", "") or ""

model = st.sidebar.text_input(
    "Model",
    value=default_model,
    help="Để trống nếu muốn provider sử dụng model mặc định.",
)

version = st.sidebar.text_input("Artifact version", value="v3")

history_window = st.sidebar.slider(
    "History window",
    min_value=1,
    max_value=20,
    value=5,
)

max_tool_rounds = st.sidebar.slider(
    "Maximum tool rounds",
    min_value=1,
    max_value=10,
    value=4,
)

st.sidebar.divider()

if st.sidebar.button("🆕 New conversation", use_container_width=True):
    st.session_state.pop("chat_session", None)
    st.rerun()


# --------------------------------------------------
# Session initialization / configuration changes
# --------------------------------------------------

config_signature = (
    provider_name,
    model,
    version,
    history_window,
    max_tool_rounds,
)

if (
    "chat_session" not in st.session_state
    or st.session_state.get("config_signature") != config_signature
):
    st.session_state.chat_session = initialize_chat(
        provider_name,
        model,
        version,
        history_window,
        max_tool_rounds,
    )
    st.session_state.config_signature = config_signature


session = st.session_state.chat_session
transcript = session["transcript"]


# --------------------------------------------------
# Load agent artifacts
# --------------------------------------------------

try:
    system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    tool_declarations = load_tool_declarations(TOOLS_PATH)
    openai_tools = to_openai_tools(tool_declarations)
except Exception as exc:
    st.error(f"Cannot load agent configuration: {type(exc).__name__}: {exc}")
    st.stop()


# --------------------------------------------------
# Main header
# --------------------------------------------------

st.title("Research Agent Chat")
st.caption(
    f"Provider: {provider_name}  |  "
    f"Model: {model or default_model or 'Provider default'}  |  "
    f"Version: {version}"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Conversation turns", len(transcript["turns"]))

with col2:
    st.metric("Tool calls", sum(
        len(turn.get("tool_events", []))
        for turn in transcript["turns"]
    ))

with col3:
    st.metric("History window", history_window)


# --------------------------------------------------
# Display previous conversation
# --------------------------------------------------

for turn in transcript["turns"]:
    with st.chat_message("user"):
        st.markdown(turn.get("user", ""))

    with st.chat_message("assistant"):
        status = turn.get("status", "unknown")

        if status == "provider_error":
            st.error(turn.get("error", "Provider error"))
        else:
            st.markdown(turn.get("assistant_text") or "No response.")

        if turn.get("tool_events"):
            with st.expander(
                f"🔧 Tool calls ({len(turn['tool_events'])})"
            ):
                for event in turn["tool_events"]:
                    st.markdown(f"**Tool:** `{event.get('tool')}`")
                    st.markdown("Arguments")
                    st.json(event.get("args", {}))
                    st.markdown("Result")
                    st.json(event.get("result", {}))

        if status == "waiting_for_user":
            st.info("Agent is waiting for additional information.")


# --------------------------------------------------
# Chat input and execution
# --------------------------------------------------

user_text = st.chat_input("Ask your research agent...")

if user_text:
    with st.chat_message("user"):
        st.markdown(user_text)

    session["turn_index"] += 1

    turn_record = {
        "turn_index": session["turn_index"],
        "started_at": now_iso(),
        "user": user_text,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }

    messages = [
        *trim_history(session["history"], history_window),
        {"role": "user", "content": user_text},
    ]

    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking..."):
            try:
                result = run_model_tool_loop(
                    provider=provider,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *messages,
                    ],
                    tools=openai_tools,
                    model=model or None,
                    max_tool_rounds=max_tool_rounds,
                )

                turn_record.update(result)
                assistant_text = result.get("assistant_text", "")

                if result.get("status") == "waiting_for_user":
                    st.info("Agent needs more information.")
                elif result.get("status") == "max_tool_rounds":
                    st.warning("Maximum tool rounds reached.")
                else:
                    st.success("Response completed.")

                st.markdown(assistant_text or "No response.")

                if result.get("tool_events"):
                    with st.expander(
                        f"🔧 Tool calls ({len(result['tool_events'])})",
                        expanded=True,
                    ):
                        for event in result["tool_events"]:
                            st.markdown(f"**Tool:** `{event.get('tool')}`")
                            st.markdown("Arguments")
                            st.json(event.get("args", {}))
                            st.markdown("Result")
                            st.json(event.get("result", {}))

                # Keep clarification question in history so the next
                # user message can answer it.
                session["history"].append({
                    "role": "user",
                    "content": user_text,
                })
                session["history"].append({
                    "role": "assistant",
                    "content": assistant_text,
                })

            except Exception as exc:
                turn_record.update({
                    "status": "provider_error",
                    "error": f"{type(exc).__name__}: {exc}",
                })
                st.error(turn_record["error"])

    turn_record["ended_at"] = now_iso()
    transcript["turns"].append(turn_record)

    write_transcript(session["transcript_path"], transcript)

    st.rerun()


# --------------------------------------------------
# Transcript controls
# --------------------------------------------------

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.caption(f"Transcript: `{session['transcript_path'].name}`")

with col2:
    transcript_json = json.dumps(
        transcript,
        ensure_ascii=False,
        indent=2,
        default=str,
    )

    st.download_button(
        "⬇️ Download transcript JSON",
        data=transcript_json,
        file_name=session["transcript_path"].name,
        mime="application/json",
        use_container_width=True,
    )
