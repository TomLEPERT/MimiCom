import requests

def authentification_user(email, password):
    url = "http://localhost:8501/"
    payload = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return response.json()  # statut ok
        else:
            return None  
            
    except Exception as e:
        print(f"Erreur de connexion à l'API : {e}")
        return None