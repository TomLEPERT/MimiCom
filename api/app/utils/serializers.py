from typing import Any, Dict

def serialize_log(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convertit un document Mongo (logs) en dict JSON-friendly :
    - supprime le champ Mongo interne "_id"
    """
    doc = dict(doc)
    doc.pop("_id", None)
    return doc
