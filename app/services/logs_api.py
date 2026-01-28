from typing import Any, Dict, List, Optional, Tuple

from .request import request

# -------------------------------------------------------------------
# Logs
# -------------------------------------------------------------------
def get_prospect_logs(
    prospect_id: str,
    limit: int = 50,
    skip: int = 0,
) -> Tuple[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
    """
    Logs d'un prospect (GET /prospects/{prospect_id}/logs)
    """
    return request(
        "GET",
        f"/prospects/{prospect_id}/logs",
        params={"limit": limit, "skip": skip},
    )


def list_logs(
    limit: int = 50,
    skip: int = 0,
    user: Optional[str] = None,
    field: Optional[str] = None,
    prospect_id: Optional[str] = None,
) -> Tuple[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
    """
    Liste tous les logs (GET /prospects/logs/all) + filtres optionnels
    """
    params: Dict[str, Any] = {"limit": limit, "skip": skip}
    if user is not None:
        params["user"] = user
    if field is not None:
        params["field"] = field
    if prospect_id is not None:
        params["prospect_id"] = prospect_id

    return request("GET", "/prospects/logs/all", params=params)