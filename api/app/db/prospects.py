from .mongo import get_db

def get_prospects_collection():
    """
    Retourne la collection MongoDB 'prospects'.
    """
    db = get_db()
    return db["prospects"]