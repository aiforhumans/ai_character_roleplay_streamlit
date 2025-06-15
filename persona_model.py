"""Pydantic schema for persona files."""

from pydantic import BaseModel


class Persona(BaseModel):
    """Simplified persona definition used by the builder and chat UI."""

    who: str
    how: str
    why: str
    relationship: str
    rules: str

