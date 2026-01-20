import os

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

# URL du "broker" Celery (la boîte aux lettres des tâches)
# Ici, on utilise Redis comme broker
# 0 = numéro de base Redis utilisée pour stocker les messages
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")

# URL du "backend de résultats" Celery
# Sert à stocker le résultat des tâches Celery (ex: statut terminé, valeur de retour)
# 1 = numéro de base Redis utilisée pour stocker les résultats
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")