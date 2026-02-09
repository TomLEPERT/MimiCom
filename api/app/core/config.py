import os
from dotenv import load_dotenv

# URL de connexion à la base de données MongoDB
# On essaie d'abord de la lire depuis la variable d'environnement MONGODB_URI
# Si elle n'existe pas, on utilise cette valeur par défaut :
# mongodb://mongodb:27017/mimicom
#
# Explication :
# - mongodb        → nom du service MongoDB dans docker-compose
# - 27017          → port par défaut de MongoDB
# - mimicom        → nom de la base de données utilisée
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://mongodb:27017/mimicom")
MONGODB_DB = os.getenv("MONGODB_DB", "mimicom")

# URL du "broker" Celery (la boîte aux lettres des tâches)
# Ici, on utilise Redis comme broker
# 0 = numéro de base Redis utilisée pour stocker les messages
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")

# URL du "backend de résultats" Celery
# Sert à stocker le résultat des tâches Celery (ex: statut terminé, valeur de retour)
# 1 = numéro de base Redis utilisée pour stocker les résultats
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

def reload_env() -> None:
    load_dotenv(ENV_PATH, override=True)

# -------------------------------
# Geocoding (lat/lon)
# -------------------------------
# Provider par défaut :
# - "ban" => https://api-adresse.data.gouv.fr (France, gratuit, sans clé)
# - "nominatim" => OpenStreetMap (attention aux limites d'usage)
GEOCODING_PROVIDER = os.getenv("GEOCODING_PROVIDER", "ban")
GEOCODING_API_KEY = os.getenv("GEOCODING_API_KEY", "")
GEOCODING_TIMEOUT_SECONDS = float(os.getenv("GEOCODING_TIMEOUT_SECONDS", "8"))
GEOCODING_USER_AGENT = os.getenv("GEOCODING_USER_AGENT", "mimicom/1.0 (contact: you@example.com)")
GEOCODING_CONCURRENCY = int(os.getenv("GEOCODING_CONCURRENCY", "5"))
