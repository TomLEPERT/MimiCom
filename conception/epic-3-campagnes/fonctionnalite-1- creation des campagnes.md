# Fonctionnalité 1 – Creation d'une campagne

## Description
Mise en place d'un workflow complet de création de campagne depuis l'Overview.
Ce processus inclut la sélection dynamique d'une population cible (subset), une segmentation automatique par Machine Learning (Clustering), l'export des données enrichies (CSV) et la génération automatique d'une page de dashboard dédiée à cette campagne.

## Objectifs

- Simplifier le lancement de campagnes via une interface unifiée.
- Optimiser le ciblage grâce à une prévisualisation du volume de prospects.
- Segmenter la base de données via un algorithme de Clustering pour personnaliser les mailings.
- Automatiser la préparation des données et la création de l'interface de suivi.

## Scénario
L'utilisateur clique sur "Créer Campagne" > Sélectionne ses filtres > Visualise le volume > Remplit les infos > Valide > Le système clusterise, génère le CSV et crée la page > L'utilisateur accède à la nouvelle page.

## User Stories
### US. Selection
Sélection interactive de la population cible (subset) avec prévisualisation immédiate du volume de données concerné

> **Requis :**
- Bouton "Créer une campagne" visible sur le dashboard principal (Overview).
- Volet latéral qui s'ouvre au clic.
- Liste de filtres à choix multiples correspondant aux catégories de prospects en base.
- Compteur visuel (ex: "Nombre de prospects : 0").

> **Règles de gestion :**
- Le compteur de prospects doit se rafraîchir en temps réel à chaque ajout/retrait de filtre.
- Si le compteur est égal à 0, le bouton "Suivant/Valider" est désactivé (grisé).
- Les filtres au sein d'une même catégorie fonctionnent en "OU" (ex: "Retail" OU "Tech"), les filtres entre catégories différentes fonctionnent en "ET" (ex: "Retail" ET "France").

### US. Utilisation de filtres / navigation
Configuration des attributs administratifs et temporels nécessaires à l'identification et au lancement de la campagne

> **Requis :**
- Champ texte "Nom de la campagne".
- Sélecteur de date pour "Date événement" et/ou champ numérique pour "Durée".
- Liste déroulante pour "Réseau social" (Optionnel).

> **Règles de gestion :**
- Le nom de la campagne doit être unique. Une vérification en base doit être faite à la volée. Si doublon, message d'erreur.
- Si une date de fin est demandée, elle doit être strictement supérieure à la date de début/événement.
- Si le champ "Réseau social" est laissé vide, la valeur par défaut Multi-canal est appliquée.
- Tous les champs obligatoires (Nom, Date) doivent être remplis pour débloquer l'action de création.

### US. Machine learning 
Traitement algorithmique du subset pour générer une segmentation prédictive (groupes de prospects) adaptée à la stratégie de communication.

> **Requis :**
- Modèle de clustering entraîné et accessible via API ou fonction interne.
- Composant de chargement sur l'interface utilisateur pendant le calcul.

> **Règles de gestion :**
- Le processus ML ne se déclenche qu'après la validation finale des étapes a et b.
- L'algorithme ne s'applique que sur les IDs du subset défini en étape a.
- L'algorithme doit retourner un Cluster_ID (ou Label) pour chaque ligne du subset.
- Si le subset est trop petit pour le clustering (ex: < 10 lignes), le système doit attribuer un cluster "Générique" par défaut sans lancer l'algo ML pour éviter les erreurs.

### US. Creation csv
Génération du fichier d'export regroupant l'ensemble des données du subset enrichies par le clustering, prêt pour l'exploitation.

> **Requis :**
- Service de génération de fichier.
- Espace de stockage les fichiers campagnes

> **Règles de gestion :**
- Le CSV doit contenir impérativement : Données prospects + Cluster_ID (issu de c) + Nom Campagne + Réseau Social + Date.
- Le fichier doit suivre la nomenclature : YYYY-MM-DD_[NomCampagne]_export.csv (les espaces dans le nom sont remplacés par des underscores).
- Le fichier doit être encodé en UTF-8 pour gérer les accents et caractères spéciaux.

### US. Creation campagne
Mise à jour dynamique de la page de dashboard propre à la campagne, centralisant les paramètres et les résultats du clustering pour un accès immédiat.

> **Requis :**
- Fonction existante createCampaignPage(params).
- Template de page "Dashboard Campagne".
- Menu de navigation mis à jour.

> **Règles de gestion :**
- La fonction doit recevoir en argument le chemin du CSV étape précédente ou l'objet JSON correspondant pour alimenter les graphiques.
- Une fois la page créée, l'utilisateur est redirigé vers cette nouvelle URL.
- Une entrée est ajoutée en base de données dans la table Campagnes pour que la page reste accessible via le menu lors des prochaines sessions.
