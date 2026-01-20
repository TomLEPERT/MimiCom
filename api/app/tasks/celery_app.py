# Importe la classe Celery, qui permet de créer un "worker" de tâches asynchrones
from celery import Celery

# Importe les URLs de configuration depuis le fichier config.py
# - CELERY_BROKER_URL  → adresse de Redis pour envoyer les tâches
# - CELERY_RESULT_BACKEND → adresse de Redis pour stocker les résultats
from app.core.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

# Crée une instance Celery pour le projet MimiCom
# "mimicom" = nom logique de l'application Celery
# broker = où les tâches sont envoyées (Redis)
# backend = où les résultats des tâches sont stockés (Redis)
celery = Celery(
    "mimicom",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

# Met à jour la configuration de Celery
celery.conf.update(
    # Format de sérialisation des tâches envoyées au worker
    # JSON est simple, lisible et compatible partout
    task_serializer="json",
    
    # Format de sérialisation des résultats retournés par le worker
    result_serializer="json",
    
    # Liste des formats acceptés par le worker
    # Ici, on n'accepte que du JSON pour éviter des problèmes de sécurité
    accept_content=["json"],
    
    # Fuseau horaire utilisé par Celery pour les timestamps
    timezone="Europe/Paris",
    
    # Active l'utilisation du temps UTC en interne
    # (recommandé pour éviter les bugs liés aux fuseaux horaires)
    enable_utc=True,
)
