import os

# URL de base de l'API (dans Docker: http://api:8000)
API_URL = os.getenv("API_URL", "http://api:8000")

# Timeout réseau (important pour ne pas bloquer Streamlit)
DEFAULT_TIMEOUT_SECONDS = float(os.getenv("API_TIMEOUT", "8"))