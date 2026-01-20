# Importe la classe APIRouter
# Elle permet de regrouper des routes (endpoints) dans des fichiers séparés
from fastapi import APIRouter

# Crée un "router" FastAPI
# C’est un mini-ensemble de routes qu’on branchera dans l’app principale
router = APIRouter()

# Déclare un endpoint HTTP GET accessible à l’URL : /health
# Exemple : http://localhost:8000/health
@router.get("/health")
def health():
    """
    Endpoint de test qui permet de vérifier que l’API fonctionne.

    Quand on appelle /health :
    - l’API répond {"status": "ok"}
    - ça prouve que :
        • le serveur FastAPI est bien lancé
        • l’API répond aux requêtes
        • l’architecture Streamlit → API est OK
    """
    return {"status": "ok"}