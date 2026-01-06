# Configuration initiale
## Configurer ton nom et ton email (identité des commits)
git config --global user.name "Ton Nom"
git config --global user.email "ton.email@example.com"

## Vérifier ta configuration
git config --list

# Initialisation d’un dépôt
## Créer un dépôt Git dans le dossier actuel
git init

## Cloner un dépôt distant existant (GitHub, GitLab, etc.)
git clone https://github.com/utilisateur/nom_du_repo.git

# État du dépôt
## Voir les fichiers modifiés, suivis ou non
git status

## Voir l’historique des commits
git log

## Log condensé sur une seule ligne par commit
git log --oneline --graph --decorate --all

# Ajout et validation des modifications
## Ajouter un fichier spécifique à l’index (staging area)
git add fichier.py

## Ajouter tous les fichiers modifiés
git add .

## Annuler l’ajout avant commit
git reset fichier.py

## Enregistrer un commit avec un message
git commit -m "Ajout du module numpy"

## Modifier le dernier message de commit (avant push)
git commit --amend -m "Nouveau message"

# Synchronisation avec un dépôt distant
## Ajouter un dépôt distant (souvent "origin")
git remote add origin https://github.com/utilisateur/nom_du_repo.git

## Vérifier les dépôts distants
git remote -v

## Envoyer les commits locaux vers le dépôt distant
git push origin branch

## Récupérer les modifications du dépôt distant
git pull origin branch

# Cloner et synchroniser directement
git clone <url>

# Gestion des branches
## Créer une nouvelle branche
git branch nouvelle-branche

## Changer de branche
git checkout nouvelle-branche

## Créer et aller sur une branche directement
git checkout -b nouvelle-branche

## Lister toutes les branches
git branch

## Fusionner une branche dans la branche courante
git merge nouvelle-branche

## Supprimer une branche locale
git branch -d nouvelle-branche

# Annuler ou corriger
## Annuler un fichier modifié avant add
git restore fichier.py

## Annuler un commit déjà fait (sans le supprimer de l’historique)
git revert <id_commit>

## Revenir à un commit précis (danger si partagé)
git reset --hard <id_commit>