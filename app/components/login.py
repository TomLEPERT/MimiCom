from __future__ import annotations
import streamlit as st
from services.auth_api import auth_login

def render_login() -> None:
    st.title("Connexion")
    
    with st.form("login_form"):
        username = st.text_input("Identifiant")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter")
    
    if not submitted:
        return
    
    data, error = auth_login(username, password)
    
    if error:
        st.error(error["message"])
        return
    
    st.session_state["authenticated"] = True
    st.session_state["username"] = username
    
    st.success("Connecté")
    st.switch_page("pages/Visualisation_BDD.py")