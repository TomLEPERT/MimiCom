import streamlit as st
from components.login import render_login
from components.sidebar import show_sidebar

st.set_page_config(page_title="Mimicom", layout="centered")



# Session state init
st.session_state.setdefault("time_out", None)
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("username", "")

if not st.session_state["authenticated"]:
    render_login()
    st.stop()

# appel de la sidebar

show_sidebar()

st.title(f"Bienvenue {st.session_state['username']}")

#deconnexion
def logout():
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.rerun() 



