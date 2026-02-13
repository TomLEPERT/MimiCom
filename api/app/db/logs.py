from app.db.mongo import get_db

def get_logs_collection():
    """
    Retourne la collection MongoDB qui contient les logs des modifications.
    """
    db = get_db()
    return db["logs"]