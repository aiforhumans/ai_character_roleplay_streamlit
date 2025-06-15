import streamlit as st
from persona_model import Persona
import json
import os

def show_character_editor():
    st.header("Character Traits")

    name = st.text_input("Name", "Laura")
    age = st.slider("Age", 18, 100, 50)
    gender = st.selectbox("Gender", ["Female", "Male", "Other"])
    species = st.text_input("Species", "Human")
    personality = st.text_area("Personality", "Empathetic and warm")
    tone = st.selectbox("Tone", ["Formal", "Casual", "Playful"])
    quirks = st.text_area("Quirks", "Taps fingers when thinking")
    communication_style = st.selectbox("Communication Style", ["Direct", "Subtle", "Flowery"])
    emotional_depth = st.slider("Emotional Depth", 1, 10, 7)

    if st.button("Save Persona"):
        persona = Persona(
            name=name,
            age=age,
            gender=gender,
            species=species,
            personality=personality,
            tone=tone,
            quirks=quirks,
            communication_style=communication_style,
            emotional_depth=emotional_depth
        )
        os.makedirs("data/saved_personas", exist_ok=True)
        with open(f"data/saved_personas/{name}.json", "w") as f:
            json.dump(persona.dict(), f, indent=2)
        st.success(f"Saved {name}.json")
        return persona

    return None