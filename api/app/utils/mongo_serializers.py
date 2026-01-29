from datetime import date, datetime
from typing import Any, Dict

def serialize_prospect(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convertit un document Mongo en dict JSON-friendly :
    - supprime le champ Mongo interne "_id"
    - convertit les dates/datetimes si besoin
    """
    doc = dict(doc)  # copie pour éviter de modifier l'original
    
    # Suppression de l'identifiant interne MongoDB
    doc.pop("_id", None)
    
    # On cache les champs internes
    doc.pop("email_norm", None)
    doc.pop("telephone_norm", None)
    doc.pop("allow_duplicate", None)
    doc.pop("email_unique_key", None)
    doc.pop("telephone_unique_key", None)

    # Si Mongo renvoie un datetime, on le convertit en date
    if isinstance(doc.get("date_dernier_contact"), datetime):
        doc["date_dernier_contact"] = doc["date_dernier_contact"].date()

    return doc
