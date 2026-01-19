# MimiCom – Documentation Produit

## 1. Vue d’ensemble
Objectif de l’application
MimiCom est une application de gestion de base de données et de campagnes de mailing destinée à des bénévoles et community managers de l’association Mimic, peu techniques, souhaitant communiquer efficacement avec leurs prospects et partenaires.

Persona principal
Gigi, 50 ans, ouvrier et bénévole chez Mimic. Peu à l’aise avec l’informatique, il souhaite :
- Envoyer facilement des newsletters / mails
- Visualiser rapidement des KPIs clés
- Naviguer dans une interface simple, claire et intuitive

### Scénario principal
Gigi arrive sur MimiCom et s’authentifie simplement grâce à son identifiant et son mot de passe.
Une fois connecté, il accède immédiatement à la visualisation de la base de données des prospects, où il peut parcourir l’ensemble des contacts de l’association.

Il consulte ensuite les indicateurs clés de la base, tels que la répartition géographique des prospects, le nombre de contacts actifs ou encore les partenaires déjà engagés, afin d’avoir une vision globale et rapide de la situation.

Pour préparer un nouvel événement de Mimic, Gigi crée une nouvelle campagne. Il sélectionne les prospects les plus pertinents en fonction de leur type et, s’il le souhaite, de leur localisation. L’outil lui propose alors automatiquement un regroupement des prospects en différentes catégories grâce à un système de segmentation intelligente (optionnel).

Une fois la campagne prête, Gigi peut envoyer ses mails directement depuis l’application. Il suit ensuite l’évolution de la campagne via un tableau de bord dédié, lui permettant de visualiser les retours, les réponses positives ou négatives, ainsi que les relances à effectuer.

## 2. Découpage produit
### MVP
- Authentification
- Interface de gestion de la BDD
- Tableau de bord KPIs BDD

### Évolution par EPIC
- Epic 1 : Gestion BDD & Authentification (MVP)
- Epic 2 : Import & Merging CSV
- Epic 3 : Gestion des campagnes
- Epic 4 : Paramètres utilisateur
- EPIC 5 : Chatbot intelligent d’assistance (IA)

## 3. EPIC & Fonctionnalités
### EPIC 1 – Authentification & BDD

**Fonctionnalités :**
- Authentification utilisateur
- Visualisation de la BDD
- Ajout / modification de prospects
- Recherche & filtres
- Export BDD
- Tableau de bord KPIs BDD

> **Voir dossier : epic-1-authentification-bdd**

### EPIC 2 – Merging CSV

**Fonctionnalités :**
- Import CSV
- Mapping des colonnes
- Détection doublons
- Fusion avec la BDD existante

> **Voir dossier : epic-2-merging-csv**

### EPIC 3 – Campagnes

**Fonctionnalités :**
- Création de campagne
- Sélection dynamique de prospects
- Clustering ML
- Tableau de bord de campagne
- Suivi des tâches
- Interface mailing
- Export KPIs & CSV

> **Voir dossier : epic-3-campagnes**

### EPIC 4 – User Settings

**Fonctionnalités :**
- Paramètres profil
- Paramètres applicatifs
- Filtres globaux
- Gestion des préférences

> **Voir dossier : epic-4-user-settings**

### EPIC 5 – Chatbot intelligent d’assistance (IA)

**Fonctionnalités :**
- Chatbot accessible depuis l’interface (global + page campagne)
- Mémoire de l’outil (BDD, KPIs, campagnes, clusters)
- Explication du clustering lors d’une campagne
- Proposition de messages types par cluster

> **Voir dossier : epic-5-chatbot-ia**

## 4. Modèle de fiche Fonctionnalité

Chaque fonctionnalité détaillée suit le même format :

# NomDeLaFonctionnalité

Description / Contexte

## Objectifs

## Scénario (narratif, persona)

## User Stories
- US.x : Titre
  - Description
  - Requis fonctionnels
  - Contraintes / règles métier
  - Ressources (wireframes, maquettes)