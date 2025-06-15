import streamlit as st
from openai import OpenAI
import json
import os

# --- Initialize OpenAI client for LM Studio ---
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# --- Streamlit App Config ---
st.set_page_config(page_title="Local ChatGPT Clone")
st.title("🧠 Local ChatGPT Clone (LM Studio)")

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Settings")

# Load available models from LM Studio
try:
    models = client.models.list()
    available_models = [m.id for m in models.data]
except Exception:
    available_models = ["gpt-3.5-turbo"]
    st.sidebar.warning("Could not fetch models dynamically. Using fallback.")

model_id = st.sidebar.selectbox("Choose your model", available_models, index=0)
st.session_state.setdefault("openai_model", model_id)

# Generation Parameters
temperature = st.sidebar.slider("🎛 Temperature", 0.0, 1.5, 0.7, 0.1)
top_p = st.sidebar.slider("🧠 Top-p", 0.0, 1.0, 1.0, 0.05)
max_tokens = st.sidebar.slider("📏 Max Tokens", 64, 2048, 512, 64)

# Personality Presets
persona = st.sidebar.selectbox("🤖 Personality", ["Default", "Sassy", "Wise Mentor"])
prompts = {
    "Default": "You are a helpful assistant.",
    "Sassy": "You're witty, sarcastic, and have a sharp tongue.",
    "Wise Mentor": "You are wise and calm, guiding the user with experience."
}
system_prompt = prompts[persona]

# Save/Load Chat
if st.sidebar.button("💾 Save Chat"):
    with open("chat_history.json", "w") as f:
        json.dump(st.session_state.get("messages", []), f)

if st.sidebar.button("📂 Load Chat") and os.path.exists("chat_history.json"):
    with open("chat_history.json", "r") as f:
        st.session_state["messages"] = json.load(f)
        st.rerun()

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state["messages"] = []
    st.rerun()

# --- Session State Init ---
st.session_state.setdefault("messages", [])

# Insert system prompt if not already present
if not any(m["role"] == "system" for m in st.session_state["messages"]):
    st.session_state["messages"].insert(0, {"role": "system", "content": system_prompt})

# --- Chat History Display ---
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User Input ---
if prompt := st.chat_input("What would you like to ask?"):
    st.chat_message("user").markdown(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response_box = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model=model_id,
                messages=st.session_state["messages"],
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta
                content = getattr(delta, "content", None)
                if content is not None:
                    full_response += content
                    response_box.markdown(full_response)
        except Exception as e:
            st.error(f"Error during model response: {e}")
            full_response = "⚠️ Error occurred while generating response."

    st.session_state["messages"].append({"role": "assistant", "content": full_response})

    # Auto-scroll to bottom (visual aid)
    st.markdown("<script>window.scrollTo(0,document.body.scrollHeight);</script>", unsafe_allow_html=True)

# --- Token Estimate ---
def estimate_tokens(messages):
    return sum(len(msg["content"].split()) for msg in messages) * 1.3

st.sidebar.markdown(f"🧮 Estimated Tokens: `{int(estimate_tokens(st.session_state['messages']))}`")
