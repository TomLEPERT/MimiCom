# Fonctionnalité 5 – Tableau de bord KPIs BDD

## Description

Le tableau de bord KPIs BDD permet à l’utilisateur de visualiser rapidement l’état global de la base de données prospects à travers des indicateurs clés.

Il s’appuie sur les données stockées dans Google Sheets et propose des visualisations simples et compréhensibles pour des utilisateurs non techniques comme Gigi.

Cette fonctionnalité ne modifie pas les données sources.
Elle a pour objectif de transformer la base prospects en un outil de pilotage et d’aide à la décision.

## Objectifs
- Donner une vision synthétique et actionnable de la base prospects
- Mettre en évidence la qualité et la complétude des données
- Aider à identifier les prospects prioritaires à contacter
- Permettre l’analyse rapide de la structure de la base
- Préparer la création de campagnes ciblées

## Scénario

Depuis la page de visualisation de la BDD, Gigi clique sur l’onglet « Tableau de bord ».
Il accède alors à une page dédiée affichant les principaux KPIs calculés à partir des données Google Sheets.

Il commence par consulter la répartition géographique des prospects sur une carte interactive.
Il observe ensuite la répartition des catégories de prospects et la taille du public touché via des graphiques simples.

En remarquant qu’un grand nombre de prospects n’ont pas de numéro de téléphone renseigné, Gigi clique sur l’indicateur correspondant afin d’afficher la liste des prospects concernés.

Enfin, il applique un filtre sur un type de prospect précis afin de recalculer les KPIs sur ce subset et préparer une future campagne.

## User Stories
### US10 – Accès au tableau de bord KPIs
En tant qu’utilisateur authentifié, je souhaite accéder au tableau de bord KPIs afin d’avoir une vision globale de la base prospects.

> **Requis :**
- Un onglet « Tableau de bord » accessible depuis le menu de navigation
- Une page Streamlit dédiée aux KPIs
- Chargement des données depuis Google Sheets via l’API Google

> **Règles de gestion :**
- L’accès à cette page est réservé aux utilisateurs authentifiés
- Les KPIs sont calculés dynamiquement à partir des données de la feuille Prospects
- En cas d’erreur de chargement des données, un message explicite est affiché

### US11 – Répartition géographique des prospects
En tant qu’utilisateur authentifié, je souhaite visualiser la répartition des prospects sur le territoire afin de comprendre leur implantation géographique.

> **Requis :**
- Une carte ou un graphique affichant la répartition par :
    région
    ville

> **Règles de gestion :**
- Les données géographiques sont issues des colonnes correspondantes dans Google Sheets
- Les valeurs manquantes sont regroupées dans une catégorie « Non renseigné »
- La carte se met à jour à chaque rafraîchissement de la page

### US12 – Catégories de prospects
En tant qu’utilisateur authentifié, je souhaite voir la répartition des prospects par catégorie afin de comprendre la structure de la base.

> **Requis :**
Un graphique affichant le nombre de prospects par type :
- CSCS
- Bar à jeux
- Influenceur
- MJC
- Médiathèque
- Artisan
- Éditeur
- Asso JDR
- Boutique spécialisée
- Ludothèque

> **Règles de gestion :**
- Les types sont regroupés selon la valeur type_prospect
- Les valeurs inconnues sont regroupées sous « Autre »
- Le total affiché correspond au nombre total de prospects

### US13 – Taille du public touché (par tranches)
En tant qu’utilisateur authentifié, je souhaite visualiser la taille du public touché par les prospects afin d’évaluer leur portée potentielle.

> **Requis :**
Un graphique affichant la répartition par tranches :
- < 50
- 50–149
- 150–499
- 500–999
- ≥ 1 000

> **Règles de gestion :**
- Le calcul se base sur :
    nb_followers pour les influenceurs
    nb_adherents pour les associations
- Les prospects sans valeur sont regroupés dans « Non renseigné »
- Chaque prospect ne peut appartenir qu’à une seule tranche

## US14 – Adhérents / followers par réseau social
En tant qu’utilisateur authentifié, je souhaite voir le volume d’adhérents ou de followers par réseau social afin de comparer leur impact potentiel.

> **Requis :**
- Un graphique affichant le total par réseau social
    (Instagram, Facebook, TikTok, X, etc.)

> **Règles de gestion :**
- Le calcul se base sur la colonne reseau_social
- Les prospects sans réseau renseigné sont regroupés sous « Non renseigné »
- Le total correspond à la somme des followers / adhérents associés

### US15 – Sites web renseignés
En tant qu’utilisateur authentifié, je souhaite voir la proportion de prospects disposant d’un site web afin d’évaluer leur niveau de professionnalisation.

> **Requis :**
- Un indicateur affichant :
    % de prospects avec site web
    % de prospects sans site web

> **Règles de gestion :**
- Le calcul se base sur la colonne site_web
- Un site est considéré comme renseigné si la valeur n’est ni vide ni nulle

### US16 – Répartition du statut prospect
En tant qu’utilisateur authentifié, je souhaite visualiser la répartition du statut des prospects afin de suivre leur avancement.

> **Requis :**
Un graphique affichant les statuts suivants :
- Jamais contacté
- Contacté
- En attente de réponse
- Intéressé
- Refusé

> **Règles de gestion :**
- Le calcul se base sur la colonne statut
- Les statuts inconnus sont regroupés sous « Autre »

### US17 – Taux de prospects acceptant la communication
En tant qu’utilisateur authentifié, je souhaite voir le taux de prospects acceptant d’être contactés afin de cibler les campagnes.

> **Requis :**
- Un indicateur affichant :
    % accepte_contact = true
    % accepte_contact = false

> **Règles de gestion :**
- Le calcul se base sur la colonne accepte_contact
- Le bouton « Voir le subset » applique automatiquement un filtre sur la BDD

### US18 – Données de contact manquantes
En tant qu’utilisateur authentifié, je souhaite voir combien de prospects n’ont pas de mail ou de téléphone afin d’identifier les données incomplètes.

> **Requis :**
- Deux indicateurs :
    % prospects sans email
    % prospects sans téléphone
    Un bouton « Afficher les prospects concernés »

> **Règles de gestion :**
- Le calcul se base sur les colonnes email et telephone
- Une valeur est considérée comme manquante si elle est vide ou nulle

### US19 – Prospects jamais contactés
En tant qu’utilisateur authentifié, je souhaite voir combien de prospects n’ont jamais été contactés afin de prioriser mes actions.

> **Requis :**
Un indicateur affichant :
- nombre
- % du total
- Un bouton « Voir la liste »

> **Règles de gestion :**
- Le calcul se base sur la colonne contacte
- Les prospects avec contacte = false sont inclus

### US20 – Taux de retour
En tant qu’utilisateur authentifié, je souhaite voir le taux de retour global afin d’évaluer l’efficacité de mes actions passées.

> **Requis :**
Un indicateur affichant le pourcentage de prospects ayant répondu

> **Règles de gestion :**
- Le calcul se base sur la colonne retour_prospect
- Les prospects sans valeur sont exclus du calcul

### US21 – Délai de réponse moyen
En tant qu’utilisateur authentifié, je souhaite voir le délai moyen de réponse afin d’optimiser mes relances.

> **Requis :**
Un indicateur affichant un nombre de jours moyen

> **Règles de gestion :**
- Le calcul se base sur :
    date_dernier_contact
    date_retour
- Seuls les prospects ayant répondu sont pris en compte

## Contraintes techniques
- Application développée avec Streamlit
- Données chargées depuis Google Sheets via l’API Google
- Calcul des KPIs côté application
- Mise à jour via un bouton « Rafraîchir »
- Aucune écriture dans Google Sheets
- Gestion des erreurs de calcul (valeurs manquantes, types invalides)

## Résultat attendu
- À la fin de cette fonctionnalité, MimiCom permet :
- la visualisation complète des KPIs de la base prospects,
- l’analyse rapide de la qualité des données,
- l’identification des prospects prioritaires,
- le zoom sur des subsets actionnables,
- sans altération des données sources,
- avec une interface simple et compréhensible pour Gigi.