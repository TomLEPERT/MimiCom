import os
import requests
import streamlit as st
from services.login_api import authentification_user # ticket 1.3
# Récupère l'URL de l'API depuis les variables d'environnement
# Si elle n'existe pas, on utilise "http://localhost:8000" par défaut
# (utile quand on lance l'app sans Docker)
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("MimiCom — UI (Streamlit)")

if st.button("Ping API"):
    try:
        # Envoie une requête GET vers l'endpoint /health de l'API
        # timeout=5 = on attend max 5 secondes avant d'abandonner
        r = requests.get(f"{API_URL}/health", timeout=5)
        # Si tout se passe bien, on affiche la réponse de l'API en vert
        # r.json() contient par exemple : {"status": "ok"}
        st.success(r.json())
    except Exception as e:
        # Si l'API est inaccessible ou renvoie une erreur :
        # on affiche le message d'erreur en rouge dans l'interface
        st.error(str(e))
        

st.sidebar


#------------- LOGIN VALIDE - FONCTION PAGE BDD ------------
if "connected" not in st.session_state:
    st.session_state["connected"] = False
    
def bdd_page():
    st.title("Page BDD")
        
    if st.button("Se déconnecter"):
        st.session_state["connected"] = False
        st.rerun()
        
# --- PAGE LOGIN ---
def login_page():
    st.title("Connexion")
    
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if not email or not password:
            # Texte en rouge si champs vides
            st.write(":red[Veuillez remplir tous les champs obligatoires]")
        else:
            result = authentification_user(email, password)
            
            if result and result.get("status") == "ok":
                st.session_state["connected"] = True
                st.rerun() # Redirection vers la BDD
            else:
                st.write(":red[Login Invalide]")

# --- NAVIGATION ---
if st.session_state["connected"]:
    bdd_page()
else:
    login_page()