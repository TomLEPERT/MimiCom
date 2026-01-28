from typing import Any, Dict, List, Tuple

def compute_diff(old_doc: Dict[str, Any], new_doc: Dict[str, Any], fields: List[str]) -> List[Tuple[str, Any, Any]]:
    """
    Compare old_doc et new_doc sur une liste de champs.
    Retourne uniquement les champs réellement modifiés.
    """
    diffs = []

    for field in fields:
        old_val = old_doc.get(field)
        new_val = new_doc.get(field)

        if old_val != new_val:
            diffs.append((field, old_val, new_val))

    return diffs