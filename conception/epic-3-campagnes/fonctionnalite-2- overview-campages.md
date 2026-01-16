# Fonctionnalité 2 – Overview des campagnes

## Description
Création d'un tableau de bord centralisé offrant une vision macroscopique de l'ensemble de l'activité campagne. 
Cette page agrège les statistiques de toutes les campagnes (passées et actives), propose une visualisation temporelle et permet un accès rapide aux dernières opérations.


## Objectfis
- Superviser la performance globale via des indicateurs consolidés.
- Visualiser la charge de travail et la planification grâce à une frise chronologique.
- Comparer l'efficacité des campagnes actives par rapport à l'historique.
- Naviguer rapidement vers les campagnes récentes.

## Scenario 

L'utilisateur clique sur l'onglet "Campagnes" du menu principal. 
Il atterrit sur la page "Overview Campagnes". 
Il consulte d'abord les KPI globaux (taux d'ouverture moyen, volume total), observe la répartition entre campagnes actives et terminées, analyse le calendrier via la frise chronologique, et clique enfin sur une campagne spécifique dans la liste des "Dernières campagnes" pour voir les détails.

## User stories
### US. Selection
Point d'entrée principal de la navigation, permettant un accès immédiat et intuitif au tableau de bord de supervision de toutes les opérations campagne.

> **Requis :**
- Présence dans la barre de navigation latérale ou supérieure (Menu principal).
- Icône représentative.
- État "Actif" (surbrillance) défini dans la feuille de style.

> **Règles de gestion :**
- Le bouton est visible pour tous les utilisateurs qui ont accès.
- Au clic, l'utilisateur est redirigé par défaut vers la vue "Overview" (Dashboard global) et non vers une sous-page spécifique.
- Une fois sur la page, l'onglet doit rester visuellement sélectionné pour indiquer la position de l'utilisateur dans l'arborescence.

### US. Affichage des KPIs
Interface de synthèse agrégeant les métriques de performance globales et temporelles, offrant une visualisation comparative entre l'activité en cours et l'historique archivé.

> **Requis :**
- Accès à la base de données de toutes les campagnes.
- Moteur de calcul pour l'agrégation des stats (Moyennes globales).

> **Règles de gestion :**
- Les indicateurs (Taux d'ouverture, Taux de clic, Taux de réponse, etc.) doivent être calculés sur la moyenne pondérée de toutes les campagnes présentes en base, ou filtrables par période (Année/Mois).
- Le graphique de répartition doit distinguer les campagnes selon leur statut : "En cours" (Date fin > Date jour OU Statut = Active) vs "Terminées" (Date fin < Date jour OU Statut = Archived).
- Frise Chronologique:
Doit afficher les campagnes sur un axe temporel horizontal.
Code couleur distinct pour les campagnes futures, en cours et passées.
Au survol d'une barre de la frise, une infobulle (tooltip) affiche le nom et les dates clés.
- Listes "Dernières campagnes":
Deux listes distinctes (ou onglets) : "Dernières terminées" et "Dernières lancées".
Tri décroissant par date (de la plus récente à la plus ancienne).
Limite d'affichage (ex: Top 5) avec un lien "Voir tout" pour accéder à la liste complète.