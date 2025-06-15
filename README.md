# AI Character Roleplay Engine (Streamlit)

A fully local roleplay app powered by LM Studio. Define a character and chat with them using local LLMs.

- Persona builder with fields for defining who the AI is, how it speaks and its rules
- Streamlit-based chat UI
- Local LLM connection via LM Studio (OpenAI-compatible API)
- Multipage navigation with `st.navigation`

## 🚀 How to Run

```bash
pip install -r requirements.txt
streamlit run main.py
```

Make sure LM Studio is running at `http://localhost:1234` with a supported model.

## 📂 Folder Structure

- `main.py`: Streamlit app entry point
- `character_interface.py`: Trait editor
- `chat_engine.py`: Chat logic using local LLM
- `persona_model.py`: Pydantic schema
- `utils.py`: Prompt builder
- `memory_manager.py`: JSON storage
- `data/personas/default.yaml`: Example persona loaded for system prompts
