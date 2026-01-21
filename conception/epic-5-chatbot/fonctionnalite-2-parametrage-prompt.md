# Fonctionnalité - Parametrage du prompt

## Description

Mise en place d'une interface d'administration permettant de rédiger, éditer et configurer les instructions systèmes ("System Prompt") qui pilotent le comportement, le style rédactionnel et les directives éthiques de l'intelligence artificielle.

## Objectfis

Contrôler précisément la manière dont le chatbot s'exprime pour garantir l'alignement avec l'image de marque et s'assurer qu'il reste dans son périmètre de compétence (éviter les hallucinations ou les hors-sujets).

## Scenario 
L'administrateur se connecte. 
Il accède à l'onglet "Intelligence". Il rédige ou modifie le texte d'instruction (ex: "Tu es un expert support...").
Il définit les règles de politesse et les sujets interdits. 
Avant de publier, il teste le comportement et vérifie l'orthographe dans une zone dédiée (Sandbox) pour valider les réponses.


## User stories
### US.1 Définition du persona
Interface d'édition du texte fondateur qui conditionne toutes les réponses de l'IA.

> **Requis :**
- Champ de saisie texte multiligne 
- Accès aux variables de contexte (ex: {{Nom_prospect}}, {{Date_Jour}}).
- Bouton de sauvegarde.

> **Règles de gestion :**
- Priorité : Ce prompt système doit avoir la priorité absolue sur les instructions données par l'utilisateur final (pour éviter le "Prompt Injection").
- Versionning : Chaque modification du prompt doit être historisée pour pouvoir revenir à une version précédente en cas de régression.
- Longueur : Le système doit indiquer une limite de tokens ou de caractères recommandée pour ne pas saturer la mémoire contextuelle du modèle.

### US.2 Test en sandbox
Environnement de simulation isolé permettant d'éprouver la configuration sans impacter les utilisateurs réels.

> **Requis :**
- Fenêtre de chat intégrée à côté de la zone d'édition du prompt.
- Bouton "Réinitialiser la conversation" (Clear context).
- Indicateur visuel

> **Règles de gestion :**
- Temps réel : La Sandbox doit utiliser la version du prompt non sauvegardée (brouillon) ou fraîchement sauvegardée pour permettre des itérations rapides (Test & Learn).
