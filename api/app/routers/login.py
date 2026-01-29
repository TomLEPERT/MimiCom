import os
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

# --- fonction intelligente qui recupere ce qu'il y a dans le env.example ---
load_dotenv()

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