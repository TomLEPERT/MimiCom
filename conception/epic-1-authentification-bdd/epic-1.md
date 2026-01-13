# EPIC 1 – Authentification & Gestion de la BDD

## Description

L’EPIC 1 constitue le socle fonctionnel de MimiCom. Il permet à un utilisateur de s’authentifier, d’accéder à la base de données des prospects, de la consulter, la modifier et d’en extraire des indicateurs clés.

Cette EPIC correspond au MVP de l’application et doit permettre à un utilisateur peu technique, comme Gigi, de prendre en main l’outil rapidement.

## Objectifs
- Authentifier de manière sécurisée les utilisateurs
- Accéder et visualiser la BDD de manière fluide via Streamlit
- Ajouter, modifier et consulter les prospects en respectant les contraintes métiers
- Générer et exporter des KPIs précis et filtrables

## Scénario principal

Gigi arrive sur MimiCom et s’authentifie.
Une fois connecté, il accède à la base de données des prospects, stockée dans Google Sheets et affichée dans Streamlit sous forme de tableau interactif.

Il peut rechercher un prospect, en consulter la fiche détaillée, en modifier certaines informations ou en ajouter de nouveaux.
À tout moment, Gigi peut consulter un tableau de bord affichant les KPIs principaux calculés à partir de la feuille Google.

## Liste des fonctionnalitées
Fonctionnalité 1 – Authentification
- US1 – Connexion
- US2 – Déconnexion

Fonctionnalité 2 – Visualisation de la BDD prospects
- US3 – Affichage de la BDD
- US4 – Recherche et filtres

Fonctionnalité 3 – Gestion d’un prospect
- US5 – Ajout d’un prospect
- US6 – Consultation d’un prospect
- US7 – Modification d’un prospect

Fonctionnalité 4 – Import / Export CSV
- US8 – Import CSV
- US9 – Export BDD

Fonctionnalité 5 – Tableau de bord KPIs BDD
- US10 – Visualisation des KPIs
- US11 – Filtrage et export des KPIs


