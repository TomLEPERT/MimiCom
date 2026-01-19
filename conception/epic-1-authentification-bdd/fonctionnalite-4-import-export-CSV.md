# Fonctionnalité 4 – Import / Export CSV

## Description

La fonctionnalité d’import / export CSV permet à l’utilisateur d’enrichir rapidement la base de données prospects à partir de fichiers externes, et de récupérer tout ou partie de la base pour une utilisation hors de MimiCom.

Elle constitue un pont essentiel entre MimiCom et les outils externes (Google Sheets), tout en garantissant la cohérence et la qualité des données intégrées.

Cette fonctionnalité repose sur :
- une interface Streamlit pour l’upload et le téléchargement de fichiers,
- une synchronisation avec la feuille Google Sheets utilisée comme base de données.

## Objectifs
- Permettre l’ajout massif de prospects via des fichiers CSV
- Réduire le temps de saisie manuelle
- Garantir la qualité et la cohérence des données importées
- Offrir la possibilité d’exporter la base de données ou un sous-ensemble filtré
- Faciliter l’interopérabilité avec des outils externes

## Scénario

Gigi récupère un fichier CSV contenant des contacts partenaires issus d’un salon.
Depuis MimiCom, il clique sur « Importer un CSV », sélectionne son fichier et lance l’import.

L’application analyse automatiquement la structure du fichier, mappe les colonnes avec celles de la base prospects et détecte d’éventuels doublons.
Un écran de prévisualisation lui permet de vérifier les données avant validation.

Après confirmation, seuls les prospects valides sont ajoutés à la base de données.
Un rapport d’import lui indique combien de lignes ont été ajoutées, ignorées ou mises en conflit.

Plus tard, Gigi souhaite transmettre la liste de ses prospects à un collègue.
Il applique des filtres dans la BDD puis clique sur « Exporter CSV ».
Un fichier est généré et téléchargé automatiquement avec uniquement les données visibles.

## User Stories
### US8 – Import CSV
En tant qu’utilisateur authentifié, je souhaite importer un fichier CSV afin d’ajouter plusieurs prospects à la base de données en une seule opération.

> **Requis :**
- Un bouton « Importer un CSV » accessible depuis la page BDD
- Un composant d’upload de fichier Streamlit
- Acceptation des formats .csv uniquement
- Une étape de prévisualisation des données importées
- Un bouton « Valider l’import »
- Un bouton « Annuler »

> **Règles de gestion :**
Le fichier doit contenir au minimum les colonnes suivantes :
    prospect_id (UUID)
    nom_structure
    nom_contact
    email
    telephone
    type_prospect
    pays
    region
    region
    adresse
    nb_followers
    reseau_social
    accepte_contact (bool)
    methode_contact
    contacte (bool)
    date_dernier_contact
    commentaires
- Les colonnes sont automatiquement mappées avec la feuille Prospects
- Si une colonne obligatoire est manquante :
    l’import est bloqué
    un message d’erreur explicite est affiché
- Détection des doublons par Email et Téléphone :
- si doublon détecté, la ligne est marquée comme « en conflit »
- l’utilisateur peut choisir :
    ignorer la ligne
    forcer l’ajout
- Les lignes invalides sont exclues de l’import
- Un rapport d’import est affiché avec :
    nombre total de lignes
    nombre de lignes ajoutées
    nombre de doublons
    nombre de lignes rejetées
- À la validation finale :
    seules les lignes valides sont ajoutées à Google Sheets
    un message « Import terminé avec succès » est affiché

### US9 – Export BDD
En tant qu’utilisateur authentifié, je souhaite exporter la base de données prospects afin de pouvoir l’utiliser dans un outil externe.

> **Requis :**
- Un bouton « Exporter CSV » accessible depuis la page BDD
- Génération automatique d’un fichier CSV
- Téléchargement du fichier via Streamlit

> **Règles de gestion :**
- L’export respecte les filtres actifs dans la BDD
- Seules les colonnes visibles sont exportées
- Les champs vides sont exportés comme cellules vides
- Le nom du fichier suit le format :
    mimicom_prospects_YYYYMMDD.csv
- Un message de confirmation « Export réussi » est affiché
- Limitation à un export toutes les 30 secondes pour éviter les abus
- Données – Google Sheets
- Feuille Prospects (impactées par cette fonctionnalité) :
- Ajout de nouvelles lignes lors des imports
- Lecture des lignes existantes lors des exports
- Feuille Logs (journal d’import) :
    import_id
    date_import
    utilisateur
    nb_lignes_total
    nb_lignes_ajoutees
    nb_doublons
    nb_lignes_rejetees
    nom_fichier

> **Règles de gestion :**
- Chaque import génère une entrée dans la feuille Logs
- Les erreurs détaillées sont conservées temporairement côté application
- Aucune ligne n’est modifiée automatiquement lors d’un import (MVP)

## Contraintes techniques
- Application développée avec Streamlit
- Lecture / écriture via l’API Google Sheets
- Parsing CSV effectué côté application
- Validation des données avant écriture
- Gestion simple des conflits (pas de merge automatique en MVP)

## Résultat attendu
- À la fin de cette fonctionnalité, MimiCom permet :
    l’import contrôlé de fichiers CSV,
    la détection des erreurs et doublons,
    l’export filtré de la base de données,
    une meilleure interopérabilité avec des outils externes,
    tout en garantissant la qualité des données.