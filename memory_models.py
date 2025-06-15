from typing import List, Literal
from pydantic import BaseModel

class ChatMessage(BaseModel):
    """Single message in a conversation."""

    role: Literal["system", "user", "assistant"]
    content: str

class ChatHistory(BaseModel):
    """List of chat messages."""

    messages: List[ChatMessage] = []

    def add_message(self, message: ChatMessage):
        self.messages.append(message)

    def to_openai(self) -> List[dict]:
        """Return list of messages formatted for OpenAI API."""
        return [m.model_dump() for m in self.messages]
