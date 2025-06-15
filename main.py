import streamlit as st
from pages import landing_page, chat_page, edit_page


st.set_page_config(page_title="AI Character Roleplay", page_icon="\U0001F916")

pg = st.navigation(
    [
        st.Page(landing_page, title="Home", icon="\U0001F3E0", default=True),
        st.Page(chat_page, title="Chat", icon="\U0001F4AC"),
        st.Page(edit_page, title="Persona Builder", icon="\U0001F4DD"),
    ]
)

pg.run()
