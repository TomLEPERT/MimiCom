# Fonctionnalité 3 – Gestion d’un prospect

## Description

La gestion d’un prospect permet à l’utilisateur de créer, consulter et modifier les informations détaillées d’un contact au sein de la base de données MimiCom.

Cette fonctionnalité est essentielle pour maintenir une base propre, à jour et exploitable pour les campagnes de mailing.
Elle repose sur une interaction directe avec la feuille Google Sheets des prospects via l’API Google, tout en offrant une interface simple et guidée dans Streamlit.

## Objectifs
- Permettre l’ajout de nouveaux prospects dans la BDD
- Offrir une fiche détaillée par prospect
- Autoriser la modification contrôlée des informations existantes
- Garantir la cohérence et la qualité des données
- Préparer les prospects à leur utilisation dans les campagnes

## Scénario

Depuis la page de visualisation de la BDD, Gigi clique sur un prospect existant afin d’en consulter la fiche détaillée.
Il accède alors à une page dédiée affichant l’ensemble des informations connues sur ce contact.

En remarquant qu’un numéro de téléphone est manquant, Gigi passe la fiche en mode édition et complète le champ concerné, puis enregistre les modifications.
Les données sont alors mises à jour dans Google Sheets.

Plus tard, Gigi souhaite ajouter un nouveau partenaire repéré lors d’un salon.
Il clique sur le bouton « Ajouter un prospect », renseigne les informations principales dans un formulaire, valide, et le nouveau prospect est automatiquement ajouté à la base de données.

## User Stories
### US5 – Ajout d’un prospect
En tant qu’utilisateur authentifié, je souhaite ajouter un nouveau prospect afin d’enrichir la base de données MimiCom.

> **Requis :**
- Un bouton « Ajouter un prospect » accessible depuis la page BDD
- Un formulaire Streamlit comprenant les champs suivants :
    Nom de la structure
    Nom du contact
    Email
    Téléphone
    Type de prospect
    Localisation (Pays, Région, Département, Ville)
    Nombre de followers / adhérents
    Réseau social principal
    Accepte d’être contacté (booléen)
    Méthode de contact à privilégier (email, téléphone, réseau social)

> **Règles de gestion :**
- Les champs obligatoires sont : Nom de la structure, Type de prospect, Ville
- Le champ Email doit respecter un format valide s’il est renseigné
- Le champ Téléphone doit respecter un format valide s’il est renseigné
- Le champ Type de prospect doit appartenir à une liste prédéfinie
    (CSCS, Bar à jeux, Influenceur, MJC, Médiathèque, Artisan, Éditeur, Asso JDR, Boutique spécialisée, Ludothèque)
- Si un prospect avec le même Email ou Téléphone existe déjà :
    un message d’avertissement est affiché
    l’utilisateur peut soit annuler, soit forcer l’ajout
- À la validation :
- une nouvelle ligne est ajoutée dans Google Sheets
- un identifiant unique prospect_id est généré automatiquement
- Les champs non renseignés sont enregistrés comme vides
- Un message de confirmation « Prospect ajouté avec succès » est affiché

## US6 – Consultation d’un prospect
En tant qu’utilisateur authentifié, je souhaite consulter la fiche détaillée d’un prospect afin de visualiser l’ensemble de ses informations.

> **Requis :**
- Une page dédiée générée dynamiquement à partir de l’identifiant du prospect
- Affichage structuré des informations du prospect
- Un bouton « Modifier » permettant de passer en mode édition
- Un bouton « Retour à la liste »

> **Règles de gestion :**
- Les données affichées proviennent exclusivement de Google Sheets
- Les champs vides sont affichés comme « Non renseigné »
- Aucune modification n’est possible tant que le mode édition n’est pas activé
- Si le prospect n’existe plus dans Google Sheets :
    affichage d’un message d’erreur
    redirection vers la liste des prospects

## US7 – Modification d’un prospect
En tant qu’utilisateur authentifié, je souhaite modifier les informations d’un prospect afin de maintenir la base à jour.

> **Requis :**
- Un bouton « Modifier » sur la fiche prospect
- Passage de la fiche en mode édition
- Un bouton « Enregistrer »
- Un bouton « Annuler »

> **Règles de gestion :**
- Les mêmes règles de validation que pour l’ajout s’appliquent
- Le champ prospect_id est non modifiable
- La modification de l’Email ou du Téléphone déclenche une vérification de doublon
- En cas de doublon détecté :
    affichage d’un message d’avertissement
    possibilité d’annuler ou de confirmer la modification
- À la validation :
- la ligne correspondante est mise à jour dans Google Sheets
- un message « Prospect mis à jour avec succès » est affiché
- Toute modification est enregistrée dans une feuille Logs avec :
    prospect_id
    champ modifié
    ancienne valeur
    nouvelle valeur
    date de modification
    utilisateur
    Données – Google Sheets
- Feuille Prospects (champs principaux) :
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

> **Règles de gestion :**
- prospect_id est unique et non modifiable
- Email et Téléphone ne sont pas obligatoires mais recommandés
- Le champ contacte est false par défaut
- Les dates sont stockées au format ISO (YYYY-MM-DD)
- Les commentaires sont cumulables (historique simple séparé par horodatage)

## Contraintes techniques
- Application développée avec Streamlit
- Données lues et écrites via l’API Google Sheets
- Gestion des conflits simple :
    la dernière écriture écrase la précédente (MVP)
    Validation des champs côté application
    Journalisation des modifications dans une feuille Logs

## Résultat attendu
- À la fin de cette fonctionnalité, MimiCom permet :
- l’ajout structuré de nouveaux prospects,
- la consultation détaillée de chaque contact,
- la modification contrôlée des données,
- une base de données propre, traçable et exploitable pour les campagnes,
- tout en restant simple d’usage pour un utilisateur non technique comme Gigi.