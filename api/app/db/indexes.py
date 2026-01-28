from .prospects import get_prospects_collection
from .logs import get_logs_collection

async def ensure_prospects_indexes():
    """
    Crée les index MongoDB nécessaires pour éviter les doublons.
    Appelé au démarrage de l'application.
    """
    prospects_col = get_prospects_collection()

    # Index unique partiel sur email_norm, appliqué seulement si allow_duplicate != True
    await prospects_col.create_index(
        [("email_unique_key", 1)],
        name="uniq_email_key",
        unique=True,
        background=True,
    )


    # Index unique partiel sur telephone_norm, appliqué seulement si allow_duplicate != True
    await prospects_col.create_index(
        [("telephone_unique_key", 1)],
        name="uniq_telephone_key",
        unique=True,
        background=True,
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
