# Image de base : Python 3.11 version "slim"
# → version légère de Python
FROM python:3.11-slim

# Définit le dossier de travail à l’intérieur du conteneur
WORKDIR /app

# Copie le fichier requirements.txt de l’interface Streamlit
# Même logique : on installe d’abord les libs avant le code
COPY app/requirements.txt /app/requirements.txt

# Installe les dépendances Python de l’interface
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le code Streamlit dans le conteneur
# (dossier app/ local → dossier /app/ dans le conteneur)
COPY app/ /app/

# Indique que l’application Streamlit va écouter sur le port 8501
EXPOSE 8501

# Commande lancée automatiquement au démarrage du conteneur
# - streamlit run main.py : lance l’app Streamlit
# - --server.address=0.0.0.0 : permet d’accéder à l’app depuis l’extérieur
# - --server.port=8501 : port utilisé par Streamlit
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]
