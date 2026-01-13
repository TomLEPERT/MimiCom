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

Scénario

Après s’être authentifié, Gigi est redirigé vers la page principale de MimiCom.
Il accède immédiatement à la visualisation de la base de données prospects.

Il consulte la liste complète des prospects synchronisés depuis Google Sheets, affichée sous forme de tableau interactif.
En haut de la page, plusieurs indicateurs clés lui donnent une vision rapide de l’état de la base : nombre total de prospects, répartition par type de contact et nombre de partenaires.

Gigi peut parcourir les données, appliquer des filtres simples et sélectionner des prospects afin de préparer une future campagne, sans modifier les données sources.

User Stories
US. Accès à la base de données prospects

En tant qu’utilisateur authentifié, je souhaite accéder à la base de données prospects afin de consulter l’ensemble des contacts disponibles.

Requis :

Une page Streamlit dédiée à la visualisation de la BDD prospects

Chargement des données depuis Google Sheets via l’API Google

Affichage des prospects sous forme de tableau

Règles de gestion :

L’accès à cette page est réservé aux utilisateurs authentifiés

Les données affichées sont en lecture seule

En cas d’erreur de connexion à Google Sheets, un message explicite est affiché

US. Affichage du tableau prospects

En tant qu’utilisateur authentifié, je souhaite visualiser les prospects sous forme de tableau afin de parcourir facilement les données.

Requis :

Tableau interactif Streamlit

Colonnes affichées selon la structure du Google Sheet (ex : nom, email, type, localisation, partenaire)

Règles de gestion :

Les données sont automatiquement rafraîchies au chargement de la page

Les valeurs vides ou manquantes sont affichées comme « Non renseigné »

Les données ne peuvent pas être modifiées depuis l’interface

US. Consultation des indicateurs clés (KPIs)

En tant qu’utilisateur authentifié, je souhaite consulter des indicateurs clés afin d’avoir une vision globale de la base prospects.

Requis :

Affichage de KPIs en haut de la page :

Nombre total de prospects

Répartition par type de prospect

Nombre de partenaires distincts

Règles de gestion :

Les KPIs sont calculés dynamiquement à partir des données Google Sheets

Les indicateurs se mettent à jour à chaque chargement de la page

En cas de données manquantes, les KPIs s’adaptent automatiquement

US. Filtrage simple des prospects

En tant qu’utilisateur authentifié, je souhaite filtrer les prospects afin de faciliter leur consultation.

Requis :

Filtres disponibles sur :

Type de prospect

Localisation

Règles de gestion :

Les filtres s’appliquent uniquement à l’affichage

Le filtrage ne modifie pas les données sources

Les KPIs restent calculés sur l’ensemble de la base (hors filtres)

US. Sélection de prospects

En tant qu’utilisateur authentifié, je souhaite pouvoir sélectionner des prospects afin de préparer une future campagne de mailing.

Requis :

Possibilité de sélectionner une ou plusieurs lignes du tableau

Règles de gestion :

La sélection est stockée temporairement dans la session Streamlit

Aucune modification n’est effectuée sur Google Sheets

La sélection pourra être réutilisée dans la fonctionnalité de création de campagne

Données – Google Sheets

Feuille Prospects (exemple de champs) :

prospect_id

nom

email

type_prospect

localisation

partenaire

statut_contact

Règles de gestion :

Chaque prospect est identifié de manière unique

Les emails ne sont pas nécessairement uniques à ce stade

Les données sont considérées comme source de vérité

Contraintes techniques

Application développée avec Streamlit

Données chargées depuis Google Sheets via l’API Google

Accès en lecture seule pour cette fonctionnalité

Gestion des erreurs de chargement côté application

Résultat attendu

À la fin de cette fonctionnalité, MimiCom permet :

la consultation claire et centralisée des prospects,

une compréhension rapide de l’état de la base via des KPIs,

une préparation efficace à la création de campagnes de mailing,

sans altération des données sources.