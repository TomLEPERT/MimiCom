import streamlit as st
from components.login import render_login

st.set_page_config(page_title="Mimicom", layout="centered")

# Session state init
st.session_state.setdefault("time_out", None)
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("username", "")

if not st.session_state["authenticated"]:
    render_login()
    st.stop()

# deconnexion
def logout():
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.rerun() 

# sidebar
if st.session_state["authenticated"] == False:
    render_login()
    
else:
    with st.sidebar:
        if st.button("Se déconnecter"):
            logout()

