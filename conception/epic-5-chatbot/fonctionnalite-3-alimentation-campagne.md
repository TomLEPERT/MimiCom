# Fonctionnalité - Alimentation de la campagne

## Description
Module de gestion de la base de connaissances permettant l'ingestion et l'indexation de documents spécifiques liés à une opération de campagne.


## Objectfis
Rendre le chatbot "expert" sur la campagne pour maximiser la conversion et garantir qu'il fournisse les détails spécifiques de la campagne plutôt que des informations génériques.

## Scenario 
L'utilisateur dispose d'un mail type. 
Il se connecte, visualise le mail et indique si c'est valide.


## User stories
### US. 1 Import de documents
Mécanisme d'ingestion et de vectorisation (RAG) de fichiers externes pour enrichir le contexte de l'IA.
> **Requis :**
- Zone de "Drag & Drop" pour les fichiers.
- Support des formats standards (PDF, DOCX, TXT).
- Barre de progression de l'analyse (Statut : En cours / Indexé).

> **Règles de gestion :**
- Nettoyage : Le système doit pouvoir extraire le texte brut
- Volumétrie : Limite de taille par fichier (ex: 10 Mo) et limite de nombre de caractères pour garantir la performance.
- Validation : Un message de confirmation doit valider que le contenu est bien lisible par le bot après l'import.

### US. 2 Priorisation de la réponse
Configuration de la logique de récupération.

> **Requis :**
- Tag ou étiquette "Prioritaire" sur la source de données.
- Algorithme de recherche pondéré.

> **Règles de gestion :**
- Conflit de données 
- Seuil de pertinence : La priorisation s'applique uniquement si la question de l'utilisateur est pertinente par rapport au contenu de la campagne (Matching sémantique).


### US. 3 Gestion de la temporalité
Système de planification automatique pour l'activation et la désactivation des sources de connaissances.

> **Requis :**
- Sélecteur de date et heure (Datepicker Start / End) associé au document importé.
- Indicateur de statut (Planifié / Actif / Expiré).

> **Règles de gestion :**
- Activation automatique : À la date/heure de début, les documents sont rendus accessibles au moteur de réponse sans action humaine.
- Désactivation (Archivage) : À la date/heure de fin, les documents basculent en statut "Inactif" et ne sont plus utilisés pour générer des réponses, évitant les erreurs de communication post-campagne.
- Fuseau horaire : La temporalité doit se baser sur le fuseau horaire.