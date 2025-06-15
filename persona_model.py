"""Pydantic schema for persona files."""

from typing import Optional
from pydantic import BaseModel


class Persona(BaseModel):
    """Simplified persona definition used by the builder and chat UI."""

    who: str
    how: str
    why: str
    relationship: str
    rules: str
    emotional_sensitivity: Optional[str] = None
    confidence_level: Optional[str] = None
    curiosity_level: Optional[str] = None
    moral_compass: Optional[str] = None
    conflict_style: Optional[str] = None
    attachment_style: Optional[str] = None

