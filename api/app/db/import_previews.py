from .mongo import get_db

def get_import_previews_collection():
    db = get_db()
    return db["import_previews"]