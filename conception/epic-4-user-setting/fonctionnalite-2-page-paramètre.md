# Fonctionnalité 2 - Page paramètre

## Description
La page paramètres est un facteur important de la sécurité ainsi que de l'user experience de l'application MimiCom.
Elle permet à l'utilisateur de modifier l'adresse email liée au compte, la clef API de cette adresse mail, le mot de passe associé au compte et enfin le thème de l'application.

Cette page repose sur une interface développée en Streamlit et définit dans une fonction stockée dans un fichier .py.

## Objectifs
- Permettre à l'utilisateur de changer l'adresse mail liée au compte
- Permettre à l'utilisateur de changer la clef API liée à son mail
- Permettre à l'utilisateur de changer le mot de passe de son compte
- Permettre à l'utilisateur de modifier le thème de l'application

## Scénario
Gigi a appuyé sur le bouton "paramètre" dans le menu de l'application MimiCom et se retrouve sur la page paramètre afin d'y modifier les paramètres liés à son compte.
L'application renvoit la fonction "paramètre" qui affiche une page qui affiche :
- L'adresse email actuelle du compte et un bouton "modifier" à côté de celle-ci
- La clef API de l'email lié au compte et un bouton "modifier" à côté de celle-ci
- Un bouton "changer le mot de passe"
- Le thème actuel de l'application ("clair" ou "sombre") avec un bouton de type switch pour passer de l'un à l'autre

Gigi peut désormais cliquer sur l'une des options qu'il veut modifier avant de revenir à sa campagne en cours.


## User Stories
### US. Option de changement de l'adresse mail liée au compte
Une fois arrivé sur la page des paramètres, je clique sur le bouton "modifier" à côté de l'adresse mail, pour changer.

**Requis :**
- Une page Streamlit dédiée aux paramètres
- Un bouton dans le menu pour accéder aux paramètres
- Le display de l'adresse mail en cours d'utilisation
- un bouton "modifier" pour changer l'adresse mail
- un bouton "valider" pour acter les changement et rafraichir la page

**Règle de gestion :**
- Tant que le bouton "valider" n'a pas été cliqué, les changements de l'adresse mail ne sont pas actés.


### US. Option de changement de la clef API du mail
En tant qu'utilisateur connecté, je veux changer la clef API liée à mon mail.

**Requis :**
- Une page Streamlit dédiée aux paramètres
- Un bouton dans le menu pour accéder aux paramètres
- Le display la clef API de l'adresse mail en cours d'utilisation
- un bouton "modifier" pour changer la clef API
- un bouton "valider" pour acter les changement et rafraichir la page

**Règle de gestion :**
- Tant que le bouton "valider" n'a pas été cliqué, les changements de la clef API ne sont pas actés.


### US. Option de changement du mot de passe du compte
En tant qu'utilisateur connecté, je veux changer le mot de passe lié à mon compte.

**Requis :**
- Une page Streamlit dédiée aux paramètres
- Un bouton dans le menu pour accéder aux paramètres
- Le display du mot de passe sous forme d'étoiles
- un bouton "modifier" pour changer le mot de passe
- un bouton "valider" pour acter les changement et rafraichir la page

**Règle de gestion :**
- Tant que le bouton "valider" n'a pas été cliqué, les changements du mot de passe ne sont pas actés.


### US. Option de changement du thème de l'application
En tant qu'utilisateur connecté, je veux pouvoir changer le thème de l'application entre sombre et lumineux.

**Requis :**
- Une page Streamlit dédiée aux paramètres
- Un bouton dans le menu pour accéder aux paramètres
- Un switch bouton proposant les options du thème sombre ou du thème lumineux
- Un rafraichissement de la page au clic du switch button

**Règle de gestion :**
- Aucune