import os
import requests
import streamlit as st

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
        

