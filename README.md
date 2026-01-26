# MimiCom

Outil intelligent de visualisation et d’analyse de campagnes de mailing

MimiCom est une application web dédiée à l’analyse, au pilotage et à l’optimisation de campagnes de mailing.
Elle permet de centraliser les prospects, de suivre l’engagement, de mesurer l’efficacité des campagnes et d’exploiter des indicateurs clés (KPIs), tout en intégrant progressivement des outils de Machine Learning pour améliorer la prise de décision.

## Objectifs du projet

- Centraliser les données prospects dans une base unique
- Faciliter la création et la gestion de campagnes mailing
- Visualiser les performances et KPIs clés
- Automatiser l’analyse grâce au Machine Learning
- Aider à concevoir des campagnes plus pertinentes et ciblées
- Offrir un outil simple d’usage pour des utilisateurs non techniques

## Fonctionnalités principales
### Authentification

- Système de connexion sécurisé
- Accès restreint aux pages sensibles

### Gestion & visualisation des prospects

- Dataset global des prospects
- Fiche détaillée par prospect
- Ajout, modification et consultation contrôlée
- Filtrage et segmentation avancée
- Détection de doublons (email / téléphone)
- Journalisation des modifications

### Import / Export CSV

- Import massif de prospects via fichiers CSV
- Prévisualisation avant validation
- Détection des erreurs et doublons
- Résolution des conflits (ignorer / forcer)
- Rapport d’import détaillé
- Export filtré de la base au format CSV
- Limitation anti-abus sur les exports

### Tableau de bord KPIs BDD
- Répartition géographique (région, ville)
- Répartition par type de prospect
- Taille du public touché (par tranches)
- Volume followers / adhérents par réseau
- Proportion de prospects avec site web
- Statuts des prospects
- Taux d’acceptation de la communication
- Données de contact manquantes
- Prospects jamais contactés
- Taux de retour
- Délai moyen de réponse
- Filtres dynamiques (subset)
- Drill-down vers les listes de prospects

### Gestion des campagnes

- Création et gestion des campagnes
- Sous-base de prospects par campagne
- Historique complet des campagnes
- Suivi des performances
- Analyse par segment

### Assistants intelligents (Machine Learning)

- Clustering automatique des prospects
- Segmentation basée sur profils et comportements
- Génération de templates de mails
- Assistant de création de contenus
- Checklist & rétroplanning intelligent
- Suggestions automatiques de tâches
- Recommandations de stratégies de campagne

### Export & sauvegarde

- Export des visualisations
- Export des données au format CSV
- Backup et sauvegarde de l’historique de la base de données

## Stack technique
### Backend API
- Python
- FastAPI
- Pydantic (validation des données)

### Frontend
- Streamlit
- Requests
- Pandas
- Base de données
- MongoDB

### Data & Machine Learning
- Scikit-learn
- Random Forest
- K-Means (clustering)

### Visualisation
- Matplotlib
- Seaborn

###  Conteneurisation
- Docker
- Docker Compose

## Architecture

Streamlit : interface utilisateur (UI)
FastAPI : API backend (logique métier, validation, accès DB)
MongoDB : stockage des prospects, logs et imports
Services :
  prospects
  imports CSV
  exports CSV
  KPIs

## État du projet
🟡 En cours de développement

## Perspectives d’évolution

- Intégration avancée des réseaux sociaux
- Tracking des campagnes mailing
- Amélioration des modèles ML
- Recommandations automatiques de stratégies
- Segmentation prédictive
- Déploiement cloud
- Tableau de bord analytics avancé

## Auteur
Projet développé dans un objectif pédagogique et associatif par :
- Louisa TOUDJI
- Thomas CONSTANTIN
- Tom LEPERT
