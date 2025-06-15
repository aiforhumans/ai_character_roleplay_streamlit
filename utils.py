

import json
import yaml
from jinja2 import Template
from persona_model import Persona


def load_persona(file_path: str) -> Persona:
    """Load persona data from a YAML or JSON file."""
    with open(file_path, "r") as f:
        if file_path.endswith(".json"):
            data = json.load(f)
        else:
            data = yaml.safe_load(f)
    return Persona(**data)


SYSTEM_TEMPLATE = Template(
    """
You are {{ who }}.
Relationship to user: {{ relationship }}
Speak in this style: {{ how }}
Your purpose: {{ why }}
Emotional Sensitivity: {{ emotional_sensitivity | default('') }}
Confidence Level: {{ confidence_level | default('') }}
Curiosity Level: {{ curiosity_level | default('') }}
Moral Compass: {{ moral_compass | default('') }}
Conflict Style: {{ conflict_style | default('') }}
Attachment Style: {{ attachment_style | default('') }}
Rules:\n{{ rules }}

Stay in character and respond accordingly.
"""
)


def build_system_prompt(file_path: str) -> str:
    """Build a system prompt from a persona file using Jinja."""
    persona = load_persona(file_path)
    return SYSTEM_TEMPLATE.render(**persona.model_dump())
