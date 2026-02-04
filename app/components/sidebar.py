import streamlit as st
from components.login import time_out

def show_sidebar():
    time_out()
    # Vérification de l'authentification
    if not st.session_state.get("authenticated", False):
            if st.button("Aller à la page de connexion"):
                st.switch_page("main.py") # Remplace par le nom de ton fichier principal
            st.stop()

    # Contenu de la sidebar si connecté
    with st.sidebar:
        st.write(f"{st.session_state.get('username', '')}")
        
        if st.button("Se déconnecter"):
            # Logique de déconnexion
            st.session_state["authenticated"] = False
            st.rerun() # Relance l'app pour revenir au formulaire de login