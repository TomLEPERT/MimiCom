# Fonctionnalité - Affichage du chatbot

## Description
Intégration technique et graphique du widget (composant visuel) sur l'interface utilisateur du site web, comprenant le bouton de lancement ("launcher") et la fenêtre de conversation.


## Objectifs
Rendre accessible à tout moment de la navigation utilisateur de manière intuitive, non intrusive et fluide.


## Scenario 
L'utilisateur navigue sur le site.
Il repère une icône distinctive en bas de page. 
Au clic, la fenêtre de discussion se déploie par-dessus le contenu. Lorsqu'il a terminé ou souhaite revoir le contenu de la page, il peut réduire la fenêtre d'un simple clic sans perdre le fil de la discussion.


## User stories
### US.1 Visibilité du Widget
En tant que visiteur du site, je veux voir un bouton d'action en permanence sur mon écran, afin de savoir immédiatement où cliquer si j'ai besoin d'aide.

> **Requis :**
- Icône du chatbot
- Code couleur 
- script d'intégration

> **Règles de gestion :**
- Positionnement : Le bouton doit être fixé en bas à droite de l'écran et rester visible au scroll (sticky).
- Superposition : Le bouton doit toujours s'afficher au-dessus des autres éléments du site, mais ne pas masquer des éléments critiques
- Responsive : La taille du bouton doit s'adapter

### US. 2 Ouverture/fermeture
En tant qu'utilisateur, je veux pouvoir déployer et réduire la fenêtre de chat en cliquant sur le bouton ou une croix, afin de consulter le site et le chat en alternance.

> **Requis :**
- Maquette de la fenêtre de chat
- Icône de fermeture ("X" ou chevron)
- Animation de transition

> **Règles de gestion :**
- Déclenchement : Un clic sur le launcher ouvre la fenêtre ; un clic sur la croix (ou le header) réduit la fenêtre.
- Persistance de l'état : Si l'utilisateur réduit la fenêtre alors qu'une conversation est en cours, l'historique ne doit pas être effacé lors de la réouverture (au sein de la même session).
