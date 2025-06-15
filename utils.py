

import json
import yaml
from jinja2 import Template


def load_persona(file_path):
    """Load persona data from a YAML or JSON file."""
    with open(file_path, "r") as f:
        if file_path.endswith(".json"):
            return json.load(f)
        return yaml.safe_load(f)


SYSTEM_TEMPLATE = Template(
    """
You are {{ who }}.
Relationship to user: {{ relationship }}
Speak in this style: {{ how }}
Your purpose: {{ why }}
Rules:\n{{ rules }}

Stay in character and respond accordingly.
"""
)


def build_system_prompt(file_path):
    """Build a system prompt from a persona file using Jinja."""
    data = load_persona(file_path)
    return SYSTEM_TEMPLATE.render(**data)
