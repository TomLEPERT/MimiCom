# Fonctionnalité 2 – Visualisation de la base de données prospects

## Description

La visualisation de la base de données prospects est la première fonctionnalité accessible après authentification.
Elle permet aux utilisateurs de consulter, explorer et comprendre les données prospects stockées dans Google Sheets, directement depuis l’interface MimiCom développée en Streamlit.

Cette fonctionnalité offre une vue centralisée de l’ensemble des prospects, ainsi qu’un premier niveau d’analyse via des indicateurs clés (KPIs), sans modifier les données sources.

## Objectifs
- Permettre la consultation centralisée des prospects
- Offrir une lecture claire et exploitable des données issues de Google Sheets
- Fournir une vision globale de la base via des indicateurs KPI
- Faciliter la compréhension de la qualité et de la structure des données
- Préparer l’utilisateur à la création de campagnes de mailing

## Scénario
Après s’être authentifié, Gigi est redirigé vers la page principale de MimiCom.
Il accède immédiatement à la visualisation de la base de données prospects.

Il consulte la liste complète des prospects synchronisés depuis Google Sheets, affichée sous forme de tableau interactif.
En haut de la page, plusieurs indicateurs clés lui donnent une vision rapide de l’état de la base : nombre total de prospects, répartition par type de contact et nombre de partenaires.

Gigi peut parcourir les données, appliquer des filtres simples et sélectionner des prospects afin de préparer une future campagne, sans modifier les données sources.

## User Stories
### US. Accès à la base de données prospects
En tant qu’utilisateur authentifié, je souhaite accéder à la base de données prospects afin de consulter l’ensemble des contacts disponibles.

> **Requis :**
- Une page Streamlit dédiée à la visualisation de la BDD prospects
- Chargement des données depuis Google Sheets via l’API Google
- Affichage des prospects sous forme de tableau

> **Règles de gestion :**
- L’accès à cette page est réservé aux utilisateurs authentifiés
- Les données affichées sont en lecture seule
- En cas d’erreur de connexion à Google Sheets, un message explicite est affiché

###  US. Affichage du tableau prospects
En tant qu’utilisateur authentifié, je souhaite visualiser les prospects sous forme de tableau afin de parcourir facilement les données.

> **Requis :**
- Tableau interactif Streamlit
- Colonnes affichées selon la structure du Google Sheet (ex : nom, email, type, localisation, partenaire)

> **Règles de gestion :**
- Les données sont automatiquement rafraîchies au chargement de la page
- Les valeurs vides ou manquantes sont affichées comme « Non renseigné »
- Les données ne peuvent pas être modifiées depuis l’interface

### US. Filtrage simple des prospects
En tant qu’utilisateur authentifié, je souhaite filtrer les prospects afin de faciliter leur consultation.

> **Requis :**
- Filtres disponibles sur :
    Type de prospect
    Localisation
    Nb follower
    Accept com (true/false)
    Contacté (true/false)

> **Règles de gestion :**
- Les filtres s’appliquent uniquement à l’affichage
- Le filtrage ne modifie pas les données sources

## Contraintes techniques
- Application développée avec Streamlit
- Données chargées depuis Google Sheets via l’API Google
- Accès en lecture seule pour cette fonctionnalité
- Gestion des erreurs de chargement côté application

## Résultat attendu
- À la fin de cette fonctionnalité, MimiCom permet :
- la consultation claire et centralisée des prospects, sans altération des données sources.