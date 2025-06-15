import os
import json
import streamlit as st
from persona_model import Persona


def show_character_editor():
    """UI for creating and saving personas."""

    st.header("Define Persona")

    who = st.text_input("Who to be (role or character)", "Aiden the Mentor")
    how = st.text_area("How to speak (tone, style)", "Wise and encouraging")
    why = st.text_area(
        "Why it's here (purpose or objective)",
        "Provide thoughtful advice and encourage personal growth",
    )
    relationship = st.text_input(
        "Relationship to the user (friend, family, etc.)",
        "mentor",
    )
    rules = st.text_area(
        "Rules (behaviour guidelines for the AI)",
        "Stay positive and support the user at all times.",
    )

    if st.button("Save Persona"):
        persona = Persona(
            who=who,
            how=how,
            why=why,
            relationship=relationship,
            rules=rules,
        )
        os.makedirs("data/saved_personas", exist_ok=True)
        filename = f"{who.replace(' ', '_').lower()}.json"
        with open(os.path.join("data/saved_personas", filename), "w") as f:
            json.dump(persona.dict(), f, indent=2)
        st.success(f"Saved {filename}")
        return persona

    return None
