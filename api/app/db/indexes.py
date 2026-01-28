from .prospects import get_prospects_collection

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
