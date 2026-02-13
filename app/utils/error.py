from typing import Any, Dict, Optional

# -------------------------------------------------------------------
# Gestion des erreures
# -------------------------------------------------------------------
def make_error(
    *,
    err_type: str,
    message: str,
    status_code: Optional[int] = None,
    detail: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Construit un objet d'erreur uniforme pour l'UI Streamlit.
    """
    return {
        "type": err_type,
        "status_code": status_code,
        "message": message,
        "detail": detail,
    }
