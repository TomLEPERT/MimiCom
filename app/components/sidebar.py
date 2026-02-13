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
        st.divider()
        st.write(f"**{st.session_state.get('username', '')}**")
        
        if st.button("Se déconnecter" , key="btn_logout_sidebar"):
            # Logique de déconnexion
            st.session_state["authenticated"] = False
            st.rerun() # Relance l'app pour revenir au formulaire de login

        if st.sidebar.button("⚙️ Settings", key="btn_settings_sidebar"):
            # On définit le mode sur settings
            st.session_state.bdd_mode = "settings"
        
        # SI l'utilisateur est sur main.py, on le redirige vers la page qui sait afficher les settings
        # Si le fichier s'appelle exactement Visualisation_BDD.py :
            try:
                st.switch_page("pages/Visualisation_BDD.py")
            except:
            # Si on est déjà sur la page, le switch_page peut être ignoré ou géré par le rerun
                st.rerun()
