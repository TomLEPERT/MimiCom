from typing import Any, Dict, Optional, Tuple
import requests

from config import API_URL, DEFAULT_TIMEOUT_SECONDS
from utils.error import make_error

# -------------------------------------------------------------------
# Request API
# -------------------------------------------------------------------
def request(
    method: str,
    path: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> Tuple[Optional[Any], Optional[Dict[str, Any]]]:
    """
    Exécute une requête HTTP vers l'API et renvoie (data, error).

    - data : dict/list si succès
    - error : dict standardisé si erreur
    """
    url = f"{API_URL}{path}"

    try:
        resp = requests.request(
            method=method,
            url=url,
            params=params,
            json=json,
            timeout=timeout,
        )
    except requests.Timeout:
        return None, make_error(
            err_type="timeout",
            message="Délai dépassé : impossible de contacter l’API.",
        )
    except requests.RequestException as e:
        return None, make_error(
            err_type="network",
            message="Erreur réseau : impossible de contacter l’API.",
            detail=str(e),
        )

    body: Any = None
    if resp.content:
        try:
            body = resp.json()
        except ValueError:
            body = resp.text

    if 200 <= resp.status_code < 300:
        return body, None

    detail = body.get("detail") if isinstance(body, dict) and "detail" in body else body

    if resp.status_code == 409:
        return None, make_error(
            err_type="conflict",
            status_code=409,
            message="Conflit : doublon détecté.",
            detail=detail,
        )

    if resp.status_code == 404:
        return None, make_error(
            err_type="not_found",
            status_code=404,
            message="Ressource introuvable.",
            detail=detail,
        )

    return None, make_error(
        err_type="http",
        status_code=resp.status_code,
        message="Erreur API : impossible de terminer l’opération.",
        detail=detail,
    )


# -------------------------------------------------------------------
# Request API (FILES / multipart)
# -------------------------------------------------------------------
def request_files(
    method: str,
    path: str,
    *,
    files: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> Tuple[Optional[Any], Optional[Dict[str, Any]]]:
    """
    Exécute une requête multipart/form-data (upload fichier) vers l'API
    et renvoie (data, error).

    Exemple files:
        {"file": ("mon.csv", bytes_data, "text/csv")}
    """
    url = f"{API_URL}{path}"

    try:
        resp = requests.request(
            method=method,
            url=url,
            params=params,
            files=files,
            timeout=timeout,
        )
    except requests.Timeout:
        return None, make_error(
            err_type="timeout",
            message="Délai dépassé : impossible de contacter l’API.",
        )
    except requests.RequestException as e:
        return None, make_error(
            err_type="network",
            message="Erreur réseau : impossible de contacter l’API.",
            detail=str(e),
        )

    body: Any = None
    if resp.content:
        try:
            body = resp.json()
        except ValueError:
            body = resp.text

    if 200 <= resp.status_code < 300:
        return body, None

    detail = body.get("detail") if isinstance(body, dict) and "detail" in body else body

    if resp.status_code == 409:
        return None, make_error(
            err_type="conflict",
            status_code=409,
            message="Conflit : doublon détecté.",
            detail=detail,
        )

    if resp.status_code == 404:
        return None, make_error(
            err_type="not_found",
            status_code=404,
            message="Ressource introuvable.",
            detail=detail,
        )

    return None, make_error(
        err_type="http",
        status_code=resp.status_code,
        message="Erreur API : impossible de terminer l’opération.",
        detail=detail,
    )