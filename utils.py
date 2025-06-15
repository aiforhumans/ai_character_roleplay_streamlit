

def build_system_prompt(persona):
    return (
        f"""
You are {persona.name}, a {persona.age}-year-old {persona.species}.
Traits:
- Personality: {persona.personality}
- Tone: {persona.tone}
- Quirks: {persona.quirks}
- Communication Style: {persona.communication_style}
- Emotional Depth: {persona.emotional_depth}

Speak naturally and stay in character at all times.
"""
    )
