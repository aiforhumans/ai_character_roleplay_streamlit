import json
import os

from memory_models import ChatHistory, ChatMessage


def load_memory(filename: str) -> ChatHistory:
    """Load chat history from a JSON file."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            messages = [ChatMessage(**m) for m in data]
            return ChatHistory(messages=messages)
    return ChatHistory()


def save_memory(filename: str, history: ChatHistory):
    """Save chat history to disk."""
    with open(filename, "w") as f:
        json.dump([m.model_dump() for m in history.messages], f, indent=2)


def history_path(persona_label: str) -> str:
    """Return the storage path for a persona's conversation history."""
    os.makedirs("data/chat_history", exist_ok=True)
    base = os.path.splitext(persona_label)[0]
    base = base.replace(" ", "_").lower()
    return os.path.join("data/chat_history", f"{base}_history.json")


def load_persona_history(persona_label: str) -> ChatHistory:
    """Load chat history for a persona if it exists."""
    return load_memory(history_path(persona_label))


def save_persona_history(persona_label: str, history: ChatHistory):
    """Persist chat history for a persona."""
    save_memory(history_path(persona_label), history)
