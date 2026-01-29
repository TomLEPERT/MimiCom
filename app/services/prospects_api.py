from typing import Any, Dict, List, Optional, Tuple

from services.request import request


# -------------------------------------------------------------------
# Prospects : CRUD
# -------------------------------------------------------------------
def get_prospect(prospect_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Récupère un prospect (GET /prospects/{prospect_id})
    """
    return request("GET", f"/prospects/{prospect_id}")


def list_prospects() -> Tuple[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
    """
    Liste tous les prospects (GET /prospects)
    """
    return request("GET", "/prospects")


def create_prospect(
    payload: Dict[str, Any],
    force: bool = False,
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Crée un prospect (POST /prospects?force=...)
    """
    return request("POST", "/prospects", params={"force": force}, json=payload)


def update_prospect(
    prospect_id: str,
    payload: Dict[str, Any],
    force: bool = False,
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Met à jour un prospect (PATCH /prospects/{prospect_id}?force=...)
    """
    return request("PATCH", f"/prospects/{prospect_id}", params={"force": force}, json=payload)


def delete_prospect(prospect_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Supprime un prospect (DELETE /prospects/{prospect_id})
    """
    return request("DELETE", f"/prospects/{prospect_id}")


# -------------------------------------------------------------------
# Prospects : récupération par liste d'IDs
# -------------------------------------------------------------------
def get_prospects_by_ids(
    prospect_ids: List[str],
) -> Tuple[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
    """
    Récupère une liste précise de prospects (GET /prospects/by-ids).
    """
    params = [("prospect_ids", pid) for pid in prospect_ids]
    return request("GET", "/prospects/by-ids", params=dict(params) if False else params)

# -------------------------------------------------------------------
# Prospects : recherche / filtres
# -------------------------------------------------------------------
def search_prospects(
    *,
    nom: Optional[str] = None,
    type_prospect: Optional[str] = None,
    region: Optional[str] = None,
    departement: Optional[str] = None,
    statut: Optional[str] = None,
    accepte_contact: Optional[bool] = None,
    email: Optional[bool] = None,
    telephone: Optional[bool] = None,
    sit_web: Optional[bool] = None,
    min_nb_aderents: Optional[int] = None,
    max_nb_aderents: Optional[int] = None,
    min_followers_total: Optional[int] = None,
    max_followers_total: Optional[int] = None,
    sort_by: str = "nom_structure",
    sort_dir: str = "asc",
) -> Tuple[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
    """
    Recherche prospects (GET /prospects/search) sans pagination.

    On n'envoie que les params non None pour que "si un param est non fourni, ça passe".
    """
    params: Dict[str, Any] = {
        "sort_by": sort_by,
        "sort_dir": sort_dir,
    }

    # On ajoute uniquement les filtres fournis
    if nom is not None:
        params["nom"] = nom
    if type_prospect is not None:
        params["type_prospect"] = type_prospect
    if region is not None:
        params["region"] = region
    if departement is not None:
        params["departement"] = departement
    if statut is not None:
        params["statut"] = statut
    if accepte_contact is not None:
        params["accepte_contact"] = accepte_contact
    if email is not None:
        params["email"] = email
    if telephone is not None:
        params["telephone"] = telephone
    if sit_web is not None:
        params["sit_web"] = sit_web
    if min_nb_aderents is not None:
        params["min_nb_aderents"] = min_nb_aderents
    if max_nb_aderents is not None:
        params["max_nb_aderents"] = max_nb_aderents
    if min_followers_total is not None:
        params["min_followers_total"] = min_followers_total
    if max_followers_total is not None:
        params["max_followers_total"] = max_followers_total

    return request("GET", "/prospects/search", params=params)


"""
Cas d'utilisation : 

from services.prospects_api import search_prospects

data, error = search_prospects(region="IDF", type_prospect="Influenceur")

if error:
    st.error(error["message"])
else:
    st.dataframe(data)

"""