# depuis la racine du projet
source .venv/Scripts/activate# Gestion de l’environnement
## Créer un environnement virtuel (standard)
python -m venv .venv

## Activer le venv
### PowerShell
.venv\Scripts\Activate.ps1
### CMD
.venv\Scripts\activate.bat
### Git Bash / WSL / macOS / Linux
source .venv/bin/activate

# Désactiver l’environnement
deactivate

# Gestion des packages
## Initialiser un projet
uv init

## Créer un venv
uv venv

## Ajouter un package
uv add pandas numpy

## Exécuter une commande dans l’environnement
uv run python main.py

## Verrouiller les versions (crée uv.lock)
uv lock

## Supprimer un package
uv remove numpy

# Exécution de scripts Python
## Exécuter un fichier Python
python script.py

## Exécuter un module (structure src/)
python -m mon_package.mon_module

## Exécuter avec uv (gère le venv automatiquement)
uv run python -m mon_package.mon_module

# Vérifications et infos système
## Version de Python
python --version

## Chemin de l’exécutable Python
which python        # macOS / Linux / Git Bash
where python        # Windows PowerShell / CMD

## Informations sur un package installé
pip show numpy


# Commandes utiles pour le développement
## Lancer Jupyter Notebook
jupyter notebook

## Lancer JupyterLab
jupyter lab

## Lancer des tests unitaires
pytest

## Ajouter src au PYTHONPATH
export PYTHONPATH=$(pwd)/src

# Nettoyage
## Supprimer le cache Python
rm -rf __pycache__ *.pyc

## Supprimer l’environnement virtuel
rm -rf .venv