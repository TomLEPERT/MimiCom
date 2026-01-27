import streamlit as st

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
if __name__ == "__main__":
    login_page()