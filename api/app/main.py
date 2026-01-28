from fastapi import FastAPI

# Importe le "router" défini dans le fichier health.py
# On le renomme en health_router pour plus de clarté
from .routers.health import router as health_router
from .db.indexes import ensure_prospects_indexes
from .routers.prospects import router as prospects_router

# Crée une instance de l'application FastAPI
# title = nom affiché dans la documentation automatique (/docs)
app = FastAPI(title="MimiCom API")

# Ajoute les routes définies dans health_router à l'application principale
# Cela permet de brancher l'endpoint /health dans l'API
app.include_router(health_router)
app.include_router(prospects_router)

# Startup : création des index
@app.on_event("startup")
async def startup():
    """
    Actions exécutées au démarrage de l'API.
    """
    await ensure_prospects_indexes()