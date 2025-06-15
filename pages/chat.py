import os
import streamlit as st
from utils import build_system_prompt
from chat_engine import ChatEngine
from memory_manager import (
    load_persona_history,
    save_persona_history,
)


chat_engine = ChatEngine()


def chat_page():
    """Main chat interface."""
    st.title("\U0001F9E0 Local ChatGPT Clone (LM Studio)")

    st.sidebar.header("\u2699\ufe0f Settings")

    available_models = chat_engine.list_models()

    model_id = st.sidebar.selectbox(
        "Choose your model", available_models, index=0
    )
    st.session_state.setdefault("openai_model", model_id)

    temperature = st.sidebar.slider("\U0001F39B Temperature", 0.0, 1.5, 0.7, 0.1)
    top_p = st.sidebar.slider("\U0001F9E0 Top-p", 0.0, 1.0, 1.0, 0.05)
    max_tokens = st.sidebar.slider("\U0001F4CF Max Tokens", 64, 2048, 512, 64)

    persona_dir = "data/saved_personas"
    options = {"default": "data/personas/default.yaml"}
    if os.path.isdir(persona_dir):
        for fname in os.listdir(persona_dir):
            if fname.endswith((".json", ".yaml", ".yml")):
                options[fname] = os.path.join(persona_dir, fname)

    persona_label = st.sidebar.selectbox("\U0001F916 Persona", list(options.keys()))
    persona_path = options[persona_label]

    if st.session_state.get("persona_label") != persona_label:
        st.session_state["persona_label"] = persona_label
        st.session_state["persona_path"] = persona_path
        st.session_state["messages"] = load_persona_history(persona_label)

    system_prompt = build_system_prompt(persona_path)

    if st.sidebar.button("\U0001F4BE Save Chat"):
        save_persona_history(persona_label, st.session_state.get("messages", []))

    if st.sidebar.button("\U0001F4C2 Load Chat"):
        st.session_state["messages"] = load_persona_history(persona_label)
        st.rerun()

    if st.sidebar.button("\U0001F5D1\ufe0f Clear Chat"):
        st.session_state["messages"] = []
        save_persona_history(persona_label, [])
        st.rerun()

    st.session_state.setdefault("messages", [])

    if not st.session_state["messages"] or st.session_state["messages"][0]["role"] != "system":
        st.session_state["messages"].insert(0, {"role": "system", "content": system_prompt})
    else:
        st.session_state["messages"][0]["content"] = system_prompt

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("What would you like to ask?"):
        st.chat_message("user").markdown(prompt)
        st.session_state["messages"].append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            response_box = st.empty()
            full_response = ""
            try:
                for chunk in chat_engine.stream_chat(
                    st.session_state["messages"],
                    model_id,
                    temperature,
                    top_p,
                    max_tokens,
                ):
                    full_response += chunk
                    response_box.markdown(full_response)
            except Exception as e:
                st.error(f"Error during model response: {e}")
                full_response = "\u26a0\ufe0f Error occurred while generating response."

        st.session_state["messages"].append({"role": "assistant", "content": full_response})
        save_persona_history(persona_label, st.session_state["messages"])
        st.markdown(
            "<script>window.scrollTo(0,document.body.scrollHeight);</script>",
            unsafe_allow_html=True,
        )

    def estimate_tokens(messages):
        return sum(len(msg["content"].split()) for msg in messages) * 1.3

    st.sidebar.markdown(
        f"\U0001F9EE Estimated Tokens: `{int(estimate_tokens(st.session_state['messages']))}`"
    )
