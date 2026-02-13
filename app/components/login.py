from __future__ import annotations
import streamlit as st
from services.auth_api import auth_login
import time

# GESTION DU TIMEOUT 

def time_out():
    DUREE_MAX = 60 * 60 # 1h 
    
    # On vérifie d'abord si l'utilisateur est connecté
    if st.session_state.get("authenticated"):
        last_login = st.session_state.get("time connexion")
        
        # Sécurité au cas où la clé n'existe pas encore
        if last_login is None:
            st.session_state["time connexion"] = time.time()
            return

        temps_ecoule = time.time() - last_login
        
        if temps_ecoule > DUREE_MAX:
            st.session_state.clear()
            st.warning("Session expirée. Veuillez vous reconnecter.")
            st.stop()
        else:
            # On rafraîchit le chrono à chaque interaction réussie
            st.session_state["time connexion"] = time.time()

def render_login() -> None:
    
    st.markdown("<h1 style='display:none;'>Connexion à MimiCom</h1>", unsafe_allow_html=True)
    st.set_page_config(
        page_title="Mimicom - Connexion",
        layout="wide"
    )
    col_left, col_center, col_right = st.columns([2, 2, 2])
    with col_center:
        with st.container(width='stretch', horizontal_alignment="center", vertical_alignment="center"):
            st.markdown("<h2 style='text-align: center;'>Connexion à MimiCom</h2>", unsafe_allow_html=True)
            with st.container(width='stretch', height='stretch', horizontal_alignment="center"):
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
                
                else:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.session_state["time_out"] = time.time()
                    
                    st.success("Connecté")
                    st.rerun()