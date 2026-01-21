# Fonctionnalité 1 – Authentification

## Description
L’authentification est un prérequis pour accéder à MimiCom.
Elle permet de restreindre l’accès à la base de données prospects, aux campagnes de mailing et aux indicateurs clés, en garantissant que seuls les utilisateurs autorisés peuvent utiliser l’application.

Dans le cadre du MVP, l’authentification repose sur une interface développée en Streamlit et une gestion des identifiants stockée dans un fichier .env.
Les Google Sheets sont exclusivement utilisés pour les datasets (prospects, campagnes, KPIs) et ne contiennent aucune donnée d’authentification.

## Objectifs
- Restreindre l’accès à l’application MimiCom à un usage interne
- Identifier les utilisateurs autorisés
- Empêcher l’accès aux données sans authentification
- Proposer une expérience simple et rapide pour des utilisateurs non techniques
- Mettre en place une solution légère et évolutive pour un MVP

## Scénario
Gigi arrive sur MimiCom et accède à la page d’accueil.
Avant de pouvoir consulter la base de données ou créer une campagne, il doit s’authentifier.

Il saisit son adresse email et son mot de passe dans le formulaire de connexion.
L’application vérifie les informations à partir des variables définies dans le fichier .env.

Si les identifiants sont valides, Gigi est connecté et redirigé automatiquement vers la page principale de visualisation de la base de données prospects.
Dans le cas contraire, un message d’erreur lui indique que les informations saisies sont incorrectes.

À tout moment, Gigi peut se déconnecter afin de sécuriser son accès, notamment lorsqu’il utilise un poste partagé.

## User Stories
### US. Accès à la page d’authentification
En tant qu’utilisateur non authentifié, j’arrive sur la page de connexion de MimiCom afin de pouvoir m’identifier avant d’accéder à l’application.

> **Requis :**
- Une page Streamlit dédiée à l’authentification
- Un formulaire comprenant :
- un champ Email
- un champ Mot de passe
- Le logo MimiCom visible sur la page
- Un bouton « Se connecter »

> **Règles de gestion :**
- Tant que l’utilisateur n’est pas authentifié, aucune autre page de l’application n’est accessible
- Toute tentative d’accès direct à une page interne redirige vers la page de connexion

### US. Saisie des identifiants
En tant qu’utilisateur non authentifié, je souhaite saisir mon email et mon mot de passe afin de me connecter à mon compte MimiCom.

> **Requis :**
- Le champ Email est de type email
- Le champ Mot de passe est de type password
- Les champs sont obligatoires

> **Règles de gestion :**
- L’email doit correspondre à un email existant dans la feuille Users
- Le mot de passe est comparé à une version stockée dans dans le .ENV
- Les espaces avant/après les champs sont automatiquement supprimés
- Les champs invalides sont signalés visuellement à l’utilisateur

### US. Validation de la connexion
En tant qu’utilisateur non authentifié, je souhaite valider le formulaire afin d’accéder à l’application si mes identifiants sont corrects.

> **Requis :**
- Un bouton « Se connecter »
- Vérification des identifiants

> **Règles de gestion :**
Si l’email ou le mot de passe est incorrect :
- affichage du message : « Email ou mot de passe incorrect »
En cas de succès :
- création d’une session utilisateur Streamlit
- redirection automatique vers la page de visualisation de la BDD

### US. Gestion de la session utilisateur
En tant qu’utilisateur authentifié, je souhaite rester connecté afin de naviguer librement dans l’application.

> **Requis :**
- Stockage de l’état de connexion dans la session Streamlit

> **Règles de gestion :**
- La session est automatiquement invalidée après une période d’inactivité
- Un rafraîchissement de page ne doit pas déconnecter l’utilisateur
- Les informations de session ne doivent jamais contenir le mot de passe en clair

### US. Déconnexion
En tant qu’utilisateur authentifié, je souhaite me déconnecter afin de sécuriser mon compte.

> **Requis :**
- Un bouton « Se déconnecter » accessible depuis le menu principal

> **Règles de gestion :**
- Suppression immédiate de la session utilisateur
- Redirection vers la page de connexion
- Toute tentative d’action après déconnexion redirige vers l’authentification

### Données Users - .ENV

Champs obligatoires :
- user_id (UUID)
- email (VARCHAR 255, unique)
- password (VARCHAR 255)
- role (ENUM : admin, manager, benevole)

> **Règles de gestion :**
- Un email ne peut être associé qu’à un seul utilisateur
- Les rôles déterminent les droits d’accès aux fonctionnalités futures

### Contraintes techniques
- Authentification gérée côté Streamlit
- Données utilisateurs stockées dans un .env

## Résultat attendu
À la fin de cette fonctionnalité, MimiCom dispose :
- d’un système d’authentification fonctionnel,
- sécurisé pour un MVP,
- cohérent avec l’usage d'un .env,
- compréhensible et utilisable par des utilisateurs non techniques.