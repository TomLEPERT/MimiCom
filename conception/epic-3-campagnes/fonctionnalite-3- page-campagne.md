# Fonctionnalité 3 – Page Campagne

## Description
Interface de pilotage "tout-en-un" dédiée à une campagne spécifique. Elle centralise la supervision des résultats (KPIs), la gestion organisationnelle (Tâches) et l'exécution opérationnelle (Traitement des données prospects et module d'envoi d'emails assisté)

## Objectfis
- Centraliser l'information pour éviter la dispersion entre différents outils (Excel, Email, Todo list).
- Qualifier dynamiquement la base de données (enrichissement des prospects au fil de l'eau).
- Accélérer le processus de démarchage et de relance grâce à l'automatisation et l'assistant IA.
- Assurer le suivi rigoureux des interactions (historique des échanges et rappels automatiques).

## Scenario 

L'utilisateur sélectionne une campagne depuis la liste "En cours" ou "Passées".
Il arrive sur l'onglet Overview et consulte les KPIs pour valider la performance actuelle.
Il vérifie dans le Tableau de tâches les actions prioritaires (ex: "Relances à faire").
Il navigue vers l'onglet Visualisation pour identifier les prospects à traiter (ex: filtrer sur "Démarché ? = False").
Il bascule sur l'onglet Interface Mailing, utilise le switch pour choisir "Démarchage", génère un message avec l'assistant, et envoie le mail.
Le système met automatiquement à jour la ligne du prospect (Date dernier échange, Statut).
En fin de session, l'utilisateur génère un Export PNG des résultats pour son reporting.

## User stories
### US. Acceder a differentes campagnes
Mécanisme de navigation permettant d'atteindre la page de détail d'une campagne spécifique depuis les listes globales de l'application

> **Requis :**
- Listes cliquables dans l'onglet "Campagnes en cours" et "Campagnes passées".
- URL dynamique acceptant un ID (ex: /campaign/{id}).

> **Règles de gestion :**
- Au clic sur une campagne dans l'Overview, l'ID unique de la campagne est passé en paramètre URL pour charger le contexte spécifique.
- Vérification des permissions de l'utilisateur pour voir ou éditer cette campagne spécifique avant le chargement.

### US. Charger le csv en fonction du choix
Chargement initial des données brutes et enrichies associées à la campagne via l'appel d'une fonction de lecture du fichier CSV source.

> **Requis :**
- Fonction backend loadCampaignData(csvPath).
- Accès en lecture au fichier CSV généré lors de la création.

> **Règles de gestion :**
- La fonction doit parser le CSV et transformer les lignes en objets manipulables par le Front-end (JSON).
- Si le fichier est corrompu ou introuvable, une alerte "Source de données manquante" doit s'afficher et bloquer les onglets "Visualisation" et "Mailing"

### US. Afficher les KPIs de la campagne en cours
Affichage des indicateurs de performance clés spécifiques à la campagne consultée pour un monitoring en temps réel

> **Requis :**
- Moteur de calcul statistique filtré par Campaign_ID.
- Widgets graphiques (Jauges, Compteurs).

> **Règles de gestion :**
- Les KPIs (Taux d'ouverture, de clic, de réponse) sont calculés exclusivement sur les prospects liés à cette campagne.
- Les données doivent être actualisées à chaque chargement de page ou via un bouton "Refresh".

### US. Affichage du tableau de bord des tâches de la campagne
Espace de gestion de projet intégré listant les actions opérationnelles à réaliser pour le bon déroulement de la campagne

> **Requis :**
- Vue des tâches (En cours, Terminées, À faire).
- Base de données des tâches liée à l'ID Campagne.

> **Règles de gestion :**
- Certaines tâches (ex: "Relancer le segment VIP") peuvent être créées automatiquement par le système si des règles de trigger sont atteintes.
- La modification d'un statut de tâche (drag & drop ou clic) met à jour la base de données instantanément.

### US. Naviguer entre les differents onglets
Barre de navigation persistante (Sticky Header) permettant de basculer entre la supervision (Overview), la gestion des données (Visualisation) et l'action (Mailing).

> **Requis :**
- Header "Sticky" (reste visible au scroll).
- 3 Onglets principaux : Overview, Visualisation, Interface Mailing.

> **Règles de gestion :**
- Lors du changement d'onglet, l'état des données non sauvegardées doit être préservé (ou une invite de sauvegarde proposée).

- Détails par Onglet :

Onglet 1 : Overview
Affiche les KPIs (point c) et une liste prioritaire des "Relances à effectuer aujourd'hui".

Onglet 2 : Visualisation (Data Grid)

Affichage du subset CSV.
Ajout et gestion des colonnes spécifiques :
Passe automatiquement à TRUE si un mail est envoyé via l'interface Mailing.
Mise à jour automatique si mail envoyé, ou modifiable manuellement.
Saisie manuelle ou détectée par webhook (réception mail).
Sélecteur manuel (Positif/Négatif) pour qualifier l'intérêt.
Champ datepicker. Si rempli, crée une Notification système pour l'utilisateur à la date J.
Mise à jour automatique lors de l'envoi d'une relance via l'interface.
Les champs commentaires et les colonnes enrichies doivent être éditables "in-line" (directement dans le tableau).

Onglet 3 : Interface Mailing

Un bouton switch bascule l'interface entre "Premier Démarchage" (Cold mailing) et "Relance" (Follow-up).
Intégration du Chatbot/Assistant IA pour générer ou adapter le contenu du mail selon le contexte du prospect sélectionné.
Bouton "Envoyer" qui déclenche la fonction mailer backend avec les paramètres (SMTP, Template, Destinataire) et met à jour les colonnes de l'onglet Visualisation (Démarché ?, Date dernier échange).

### US. Export format PNG du tbleau de bord et subset
Fonctionnalités d'extraction permettant de générer des rapports visuels ou de récupérer les données enrichies pour un usage externe.

> **Requis :**
- Librairie de génération d'image (ex: html2canvas) pour les KPIs.
- Générateur CSV serveur.

> **Règles de gestion :**
- Capture l'état visuel actuel des widgets KPIs et du tableau de bord pour générer une image téléchargeable.
- Génère un nouveau CSV incluant toutes les données initiales PLUS les colonnes enrichies (commentaires, statuts, dates de relance) saisies dans l'onglet Visualisation.