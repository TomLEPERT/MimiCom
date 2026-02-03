from __future__ import annotations
import streamlit as st
from services.auth_api import auth_login
import time

# GESTION DU TIMEOUT 
DUREE_MAX = 60  # 1 min pour le test

if st.session_state.get("authenticated"):
    temps_ecoule = time.time() - st.session_state.get("time connexion", 0)
    if temps_ecoule > DUREE_MAX:
        st.session_state.clear()  # Supprime les infos de session
        st.warning("Session expirée (30 min). Veuillez vous reconnecter.")
        st.stop()  # Arrête l'exécution ici
    else:
        # Relance le chrono à chaque interaction pour éviter de couper en plein travail
        st.session_state["time connexion"] = time.time()

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