# Feuille de route MimiCom

## Vue d’ensemble

> **MimiCom est composé de 4 briques principales :**
- Streamlit → l’interface (ce que l’utilisateur voit)
- FastAPI → le cerveau (les règles métier, la base de données)
- Celery → le moteur de fond (les tâches longues)
- MongoDB → la mémoire (où sont stockées les données)

Docker sert juste à tout lancer facilement.

## À quoi sert chaque techno

> **Streamlit = l’écran**
Affiche :
- tableaux de prospects
- formulaires
- dashboards KPI
- pages campagne

Ne touche pas directement à la base de données
Envoie des demandes à l’API :
- “Donne-moi les prospects”
- “Ajoute ce prospect”
- “Lance un clustering”

> **FastAPI = le cerveau**
C’est une API qui fait toute la logique métier.
Elle sert à :
- vérifier que les données sont valides
- lire / écrire dans la base
- calculer les KPIs
- lancer des tâches longues (via Celery)

“Streamlit pose la question, FastAPI donne la réponse.”

> **Celery = le travailleur de fond**
Pour les tâches longues ou lourdes.
Il s’en occupe quand :
- on importe un gros CSV
- on lance un clustering
- on génère des mails
- on fait des exports lourds

“Ça évite que l’interface freeze.”

> **MongoDB = la base de données**
Là où sont stockés :
- prospects
- campagnes
- clusters
- tâches
- logs

“C’est l’équivalent des DataFrame Pandas, mais persistant et partagé.”

> **Docker = le bouton magique**
Pas une techno métier.
Il sert juste à :
- tout lancer en 1 commande
- éviter les problèmes d’installation
- avoir la même config pour tout le monde

“Au lieu de 10 installations, on fait : docker compose up.”

## Comment le projet est structuré (qui fait quoi)
mimicom/
    app/        → Streamlit (interface utilisateur)
    api/        → FastAPI (logique + base de données)
    worker/     → Celery (tâches longues)
    docker/     → fichiers Docker
    .env        → variables secrètes (mots de passe, URL)
    docker-compose.yml → lance tout

## Détail dossier par dossier

### app/ → Streamlit**
app/
    main.py          → page principale Streamlit
    pages/           → pages secondaires (BDD, KPIs, Campagnes…)
    services/        → appels à l’API (requests)
    components/      → formulaires, tableaux, widgets réutilisables

> **Rôle :**
- afficher des données
- appeler l’API
- gérer la navigation
- zéro logique métier complexe

### api/ → FastAPI
api/
    app/
        main.py        → démarre l’API
        routers/       → endpoints (prospects, campagnes, kpis)
        services/      → règles métier
        models/        → validation des données (Pydantic)
        db/            → connexion MongoDB

> **Rôle :**
- vérifier les données
- lire / écrire dans MongoDB
- calculer les KPIs
- déclencher Celery

### worker/ → Celery
worker/
    tasks_import.py      → import CSV
    tasks_clustering.py  → clustering ML
    tasks_mailing.py     → génération mails

> **Rôle :**
- faire les gros calculs
- ne touche pas à l’interface
- écrit les résultats dans MongoDB

### docker/
docker/
    Dockerfile.app   → comment lancer Streamlit
    Dockerfile.api   → comment lancer FastAPI
docker-compose.yml  → décrit tous les services :
- app (Streamlit)
- api (FastAPI)
- worker (Celery)
- mongodb
- redis

> **Rôle :**
dire à Docker :
- quoi lancer
- dans quel ordre
- avec quelles connexions

## Comment tout communique
Utilisateur
   ↓
Streamlit (app)
   ↓ HTTP
FastAPI (api)
   ↓
MongoDB (base)

FastAPI → Redis → Celery (worker) → MongoDB



