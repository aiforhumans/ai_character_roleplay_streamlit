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

    st.subheader("Psychological Profile")
    emotional_sensitivity = st.select_slider(
        "Emotional Sensitivity",
        options=["Very Low", "Low", "Medium", "High", "Very High"],
        value="Medium",
    )
    confidence_level = st.select_slider(
        "Confidence Level",
        options=["Insecure", "Low", "Medium", "High", "Confident"],
        value="Medium",
    )
    curiosity_level = st.select_slider(
        "Curiosity Level",
        options=["Uninterested", "Low", "Medium", "High", "Inquisitive"],
        value="Medium",
    )
    moral_compass = st.selectbox(
        "Moral Compass",
        ["Utilitarian", "Deontological", "Situational", "Chaotic Good", "Neutral"],
    )
    conflict_style = st.selectbox(
        "Conflict Resolution Style",
        ["Avoidant", "Assertive", "Aggressive", "Passive-Aggressive"],
    )
    attachment_style = st.selectbox(
        "Attachment Style",
        ["Secure", "Anxious", "Avoidant", "Disorganized"],
    )

    if st.button("Save Persona"):
        persona = Persona(
            who=who,
            how=how,
            why=why,
            relationship=relationship,
            rules=rules,
            emotional_sensitivity=emotional_sensitivity,
            confidence_level=confidence_level,
            curiosity_level=curiosity_level,
            moral_compass=moral_compass,
            conflict_style=conflict_style,
            attachment_style=attachment_style,
        )
        os.makedirs("data/saved_personas", exist_ok=True)
        filename = f"{who.replace(' ', '_').lower()}.json"
        with open(os.path.join("data/saved_personas", filename), "w") as f:
            json.dump(persona.dict(), f, indent=2)
        st.success(f"Saved {filename}")
        return persona

    return None
