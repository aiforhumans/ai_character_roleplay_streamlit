import json
import os


def load_memory(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []


def save_memory(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def history_path(persona_label: str) -> str:
    """Return the storage path for a persona's conversation history."""
    os.makedirs("data/chat_history", exist_ok=True)
    base = os.path.splitext(persona_label)[0]
    base = base.replace(" ", "_").lower()
    return os.path.join("data/chat_history", f"{base}_history.json")


def load_persona_history(persona_label: str):
    """Load chat history for a persona if it exists."""
    return load_memory(history_path(persona_label))


def save_persona_history(persona_label: str, data):
    """Persist chat history for a persona."""
    save_memory(history_path(persona_label), data)
