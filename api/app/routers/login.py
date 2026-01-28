import os
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

# --- fonction intelligente qui recupere ce qu'il y a dans le env.example ---
load_dotenv()

# ---  Modèle de données ---
class LoginRequest(BaseModel):
    email: str
    password: str

# --- fonction Login ---
router = APIRouter()
@router.post("/login")

def login(credentials: LoginRequest):
    
    # Récupération du .env
    env_email = os.getenv("EMAIL")
    env_password = os.getenv("PASSWORD")

    # Vérification (Debug : on affiche ce qu'on compare)
    print(f"DEBUG -> Reçu: {credentials.email} / Attendu: {env_email}")

    if credentials.email == env_email and credentials.password == env_password:
        return { 
            "status": "ok",
            "user": {
                "email": credentials.email,
                "role": "admin"
            }
        }
    else:
        # Si ça rate, FastAPI lève une "Exception" (une erreur qui arrête le code)
        raise HTTPException(status_code=401, detail="Identifiants invalides")


# --- 4. TEST DIRECT (Sans serveur) ---
if __name__ == "_main_":
    print("--- DÉBUT DU TEST ---")

    # ÉTAPE 1 : On prépare les fausses données envoyées par l'utilisateur
    test_email = "loulou@exemple.com" 
    test_password = "cava"

    # On transforme ces données en objet "LoginRequest" comme le ferait FastAPI
    donnees_utilisateur = LoginRequest(email=test_email, password=test_password)

    # ÉTAPE 2 : On appelle la fonction login directement
    try:
        resultat = login(donnees_utilisateur)
        print("Connexion réussie.")
        print("Réponse du code :", resultat)
        
    except HTTPException as e:
        print("Erreur 401.")
        print("Détail de l'erreur :", e.detail)

    print("--- FIN DU TEST ---")