# Importe le client MongoDB asynchrone (non bloquant)
# Motor est une version "async" de PyMongo, parfaite avec FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

# Importe l'URL de connexion à MongoDB depuis la config centrale
from app.core.config import MONGODB_URI

# Crée un client MongoDB à partir de l'URI
# Cette connexion est créée une seule fois au démarrage de l'API
client = AsyncIOMotorClient(MONGODB_URI)

def get_db():
    """
    Retourne la base de données MongoDB par défaut définie dans l'URI.
    
    Exemple avec :
    MONGODB_URI = "mongodb://mongodb:27017/mimicom"
    
    → la base retournée sera "mimicom"
    
    Cette fonction permet de récupérer la base facilement
    dans n'importe quel fichier de l'API.
    """
    return client.get_default_database()