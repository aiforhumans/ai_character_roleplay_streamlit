import streamlit as st
from character_interface import show_character_editor

def edit_page():
    """Page for editing character traits."""
    st.title("\U0001F4DD Persona Builder")
    show_character_editor()
