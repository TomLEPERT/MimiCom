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
        
#-------- LOGIN -----------------
def login_page():
    st.title("Connexion")
    st.write("Identifiant")

    # saisie de l'utilisateur
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    # si l'utilisateur clique sur le bouton
    if st.button("Se connecter"):
        
        # verif si champ vide
        if not email or not password:
            st.error("Veuillez remplir les champs obligatoires")
        else:
            # si champs ok ouvrir la connexion
            st.success(f"Connexion pour : {email}")

            # AJOUT DES DEUX BOUTONS
            st.write("---") # Une ligne de séparation
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Acces prospect"):
                    st.write("Action : Ajouter un prospect")
            
            with col2:
                if st.button("Acces BDD"):
                    st.write("Action : Acceder a la BDD")

if __name__ == "__main__":
    login_page()