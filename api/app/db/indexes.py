from typing import Any, Dict, List

from .prospects import get_prospects_collection
from .logs import get_logs_collection

async def _drop_index_if_exists(col, name: str) -> None:
    """
    Supprime un index s'il existe.
    (Si l'index n'existe pas -> on ignore)
    """
    try:
        await col.drop_index(name)
    except Exception:
        # Index absent ou autre cas non bloquant
        pass

async def ensure_prospects_indexes():
    """
    Crée les index nécessaires sur la collection prospects.
    Si un ancien index existe avec le même nom mais une config différente,
    on le supprime puis on le recrée correctement.
    """
    prospects_col = get_prospects_collection()

    # On liste les index existants
    existing_indexes: List[Dict[str, Any]] = await prospects_col.list_indexes().to_list(length=None)
    existing_by_name = {idx.get("name"): idx for idx in existing_indexes}

    # Définition attendue des indexes
    desired_email = {
        "name": "uniq_email_key",
        "key": {"email_unique_key": 1},
        "unique": True,
        "partialFilterExpression": {
            "email_unique_key": {"$exists": True, "$type": "string", "$gt": ""}
        },
    }

    desired_tel = {
        "name": "uniq_telephone_key",
        "key": {"telephone_unique_key": 1},
        "unique": True,
        "partialFilterExpression": {
            "telephone_unique_key": {"$exists": True, "$type": "string", "$gt": ""}
        },
    }

    # ------------------------------------------------------------
    # Index email_unique_key
    # ------------------------------------------------------------
    idx = existing_by_name.get(desired_email["name"])
    if idx:
        # Si l'index existe mais n'a PAS la partialFilterExpression attendue -> on drop
        if idx.get("partialFilterExpression") != desired_email["partialFilterExpression"] or idx.get("unique") != True:
            await _drop_index_if_exists(prospects_col, desired_email["name"])

    # On (re)crée l'index
    await prospects_col.create_index(
        [("email_unique_key", 1)],
        name="uniq_email_key",
        unique=True,
        partialFilterExpression=desired_email["partialFilterExpression"],
    )

    # ------------------------------------------------------------
    # Index telephone_unique_key
    # ------------------------------------------------------------
    idx = existing_by_name.get(desired_tel["name"])
    if idx:
        if idx.get("partialFilterExpression") != desired_tel["partialFilterExpression"] or idx.get("unique") != True:
            await _drop_index_if_exists(prospects_col, desired_tel["name"])

    await prospects_col.create_index(
        [("telephone_unique_key", 1)],
        name="uniq_telephone_key",
        unique=True,
        partialFilterExpression=desired_tel["partialFilterExpression"],
    )

    # ------------------------------------------------------------
    # Index unique partiel sur telephone_unique_key
    # Même logique: string non vide
    # ------------------------------------------------------------
    await prospects_col.create_index(
        [("telephone_unique_key", 1)],
        name="uniq_telephone_key",
        unique=True,
        partialFilterExpression={
            "telephone_unique_key": {
                "$exists": True,
                "$type": "string",
                "$gt": "",
            }
        },
    )

async def ensure_logs_indexes():
    """
    Index utiles sur la collection logs.
    """
    col = get_logs_collection()

    # Pour retrouver rapidement les logs d'un prospect
    await col.create_index([("prospect_id", 1), ("changed_at", -1)], name="logs_by_prospect")

    # Pour filtrer par utilisateur
    await col.create_index([("user", 1), ("changed_at", -1)], name="logs_by_user")
