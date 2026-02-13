# Fonctionnalité 4 – Mes campagnes

## Description
Page dédiée à la gestion opérationnelle, affichant la liste exhaustive des campagnes actives sous forme de cartes ou de tableau. 
Elle permet de suivre l'avancement global et individuel des tâches et d'accéder rapidement au détail de chaque opération en cours.

## Objectfis
- Centraliser la vue des opérations actives pour un accès rapide.
- Prioriser le travail en visualisant instantanément les campagnes nécessitant une action (barre de progression des tâches).
- Monitorer la performance globale immédiate (entrées récentes, taux de retour moyen).

## Scenario 
L'utilisateur ouvre le menu "Campagnes" et clique sur "Mes Campagnes".
Il consulte d'abord le bandeau supérieur pour voir sa progression générale et les nouveaux leads.
Il parcourt ensuite la liste des campagnes triées du plus récent au moins récent, repère une campagne dont la barre de progression de tâches est faible, et clique dessus pour reprendre le travail.

## User stories
### US. Selection de la section "campagnes
Lien de navigation intégré dans la section thématique du menu, permettant d'accéder à la liste des opérations courantes.

> **Requis :**
- Menu latéral ou supérieur avec une section groupée "Campagnes".
- Libellé clair (ex: "Mes Campagnes" ou "Campagnes en cours").

> **Règles de gestion :**
- Le bouton est visible en permanence pour les utilisateurs ayant les accès.
- Lorsqu'on est sur cette page, le bouton doit apparaître en surbrillance pour situer l'utilisateur.

### US. Acceder à un listing
Affichage structuré de toutes les campagnes dont le cycle de vie n'est pas terminé, triées pour mettre en avant les créations récentes.

> **Requis :**
- Requête en base de données filtrant sur Status = 'Active' (ou Date_Fin >= Date_Jour).

> **Règles de gestion :**
- Le tri est chronologique décroissant (Date de création ou Date de début la plus récente en haut).
- Si le nombre de campagnes actives dépasse une limite définie (ex: 20), une pagination doit être mise en place.
- Chaque élément de la liste doit afficher au minimum : Nom de la campagne, Date de lancement, et les éléments visuels fixés.

### US. Navigation entre les campagnes
Mécanisme de redirection permettant à l'utilisateur d'entrer dans le détail d'une campagne spécifique par un simple clic sur son élément dans la liste.

> **Requis :**
- L'élément de liste doit être un lien ou contenir un bouton "Gérer / Voir".
- Routeur configuré pour l'URL dynamique /campaign/{id}.

> **Règles de gestion :**
- Toute la surface de la "carte" ou de la ligne doit être cliquable pour faciliter l'accès (sauf actions spécifiques type "supprimer").
- Le clic redirige vers la "Page Campagne" correspondante.

### US. Affichage de KPIs
Bandeau de synthèse situé en haut de page, agrégeant les performances de l'ensemble des campagnes actives pour donner une tendance générale

> **Requis :**
- Moteur de calcul d'agrégation (SUM, AVG) sur le subset des campagnes actives.
- Widgets visuels (Jauge, Gros chiffres).

> **Règles de gestion :**
- Moyenne des taux de réponse de toutes les campagnes actives.
- Somme des nouveaux prospects qualifiés sur une période glissante (ex: "7 derniers jours").
- Moyenne des pourcentages d'avancement de toutes les campagnes actives (Calcul : Somme(Avancement_Individuel) / Nb_Campagnes).

### US. Barre de progression des tâches
indicateur visuel intégré à chaque élément de la liste, reflétant le taux de complétude des tâches opérationnelles associées à la campagne.

> **Requis :**
- Accès au nombre total de tâches et au nombre de tâches "Terminées" pour chaque campagne.
- Composant "Progress Bar".

> **Règles de gestion :**
- Le pourcentage = (Nombre de tâches statut "Done" / Nombre total de tâches) * 100. Si Total = 0, afficher 0% ou masquer la barre.
- La couleur de la barre peut changer dynamiquement selon l'avancement (ex: Rouge < 30%, Jaune < 70%, Vert > 70%).
- Le pourcentage textuel (ex: "45%") doit être affiché à côté ou dans la barre pour plus de précision.
