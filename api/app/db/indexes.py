from .prospects import get_prospects_collection

async def ensure_prospects_indexes():
    """
    Crée les index MongoDB nécessaires pour éviter les doublons.
    Appelé au démarrage de l'application.
    """
    prospects_col = get_prospects_collection()

    # Index unique partiel sur email_norm
    await prospects_col.create_index(
        [("email_norm", 1)],
        name="uniq_email_norm",
        unique=True,
        partialFilterExpression={
            "email_norm": {"$exists": True, "$type": "string", "$gt": ""}
        },
    )


    # Index unique partiel sur telephone_norm
    await prospects_col.create_index(
        [("telephone_norm", 1)],
        name="uniq_telephone_norm",
        unique=True,
        partialFilterExpression={
            "telephone_norm": {"$exists": True, "$type": "string", "$gt": ""}
        },
    )
