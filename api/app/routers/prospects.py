from typing import List
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Query, status
from pymongo.errors import DuplicateKeyError
from ..db.prospects import get_prospects_collection
from ..models.prospect import ProspectCreate, ProspectOut
from ..utils.normalizers import normalize_email_for_db, normalize_phone_for_db
from ..utils.mongo_serializers import serialize_prospect


# -------------------------------------------------------------------
# Définition du router FastAPI pour les prospects
# -------------------------------------------------------------------
# prefix="/prospects" → toutes les routes commenceront par /prospects
# tags=["prospects"] → sert juste à organiser Swagger (/docs)
router = APIRouter(prefix="/prospects", tags=["prospects"])


# -------------------------------------------------------------------
# Endpoint POST /prospects
# -------------------------------------------------------------------
@router.post("", response_model=ProspectOut, status_code=status.HTTP_201_CREATED)
async def create_prospect(payload: ProspectCreate, force: bool = Query(default=False)):
    """
    Crée un prospect.

    - payload : données envoyées par le client (validées par Pydantic)
    - force : paramètre optionnel dans l'URL (?force=true)
    
    Comportement :
    - Si un doublon email/téléphone est détecté et force=false :
        → renvoie 409 + détails
    - Si force=true :
        → crée quand même (en bypassant l'unicité via allow_duplicate=true)
    """

    # Récupère la collection MongoDB "prospects"
    col = get_prospects_collection()

    # ----------------------------------------------------------------
    # Normalisation pour la détection de doublons / index Mongo
    # ----------------------------------------------------------------
    # Exemple :
    #   " Test@Mail.com " → "test@mail.com"
    #   "06 12 34 56 78" → "0612345678"
    email_norm = normalize_email_for_db(payload.email) if payload.email else None
    telephone_norm = normalize_phone_for_db(payload.telephone) if payload.telephone else None
    
    doc["email_norm"] = email_norm
    doc["telephone_norm"] = telephone_norm
    doc["allow_duplicate"] = bool(force)
    
    # clés utilisées par les index uniques
    # - si force=false => clé = valeur normalisée => unicité
    # - si force=true  => clé = valeur unique random => bypass unicité
    doc["email_unique_key"] = (
        email_norm if (email_norm and not force) else (f"FORCED:{uuid4()}" if email_norm else None)
    )

    doc["telephone_unique_key"] = (
        telephone_norm if (telephone_norm and not force) else (f"FORCED:{uuid4()}" if telephone_norm else None)
    )

    # ----------------------------------------------------------------
    # Construction des filtres pour détecter un doublon
    # ----------------------------------------------------------------
    # On va créer une requête Mongo du type :
    #   { "$or": [ {email_norm: ...}, {telephone_norm: ...} ] }
    # mais seulement pour les champs fournis
    or_filters = []

    # Si un email est fourni → on cherche un prospect avec le même email_norm
    # allow_duplicate != True → on ignore les prospects "forcés"
    if email_norm:
        or_filters.append({
            "email_norm": email_norm,
            "allow_duplicate": {"$ne": True}
        })

    # Si un téléphone est fourni → idem
    if telephone_norm:
        or_filters.append({
            "telephone_norm": telephone_norm,
            "allow_duplicate": {"$ne": True}
        })

    # ----------------------------------------------------------------
    # Vérification des doublons AVANT insertion
    # ----------------------------------------------------------------
    duplicate_info = None

    # On ne fait la requête que si on a au moins un filtre
    if or_filters:
        existing = await col.find_one(
            {"$or": or_filters},
            {"prospect_id": 1, "email_norm": 1, "telephone_norm": 1}
        )

        if existing:
            # On détermine quel champ est en conflit
            fields = []

            if email_norm and existing.get("email_norm") == email_norm:
                fields.append("email")

            if telephone_norm and existing.get("telephone_norm") == telephone_norm:
                fields.append("telephone")

            # Infos retournées à Streamlit
            duplicate_info = {
                "message": "Doublon détecté",
                "fields": fields,
                "existing_prospect_id": existing.get("prospect_id"),
            }

            # Si force=false → on bloque la création
            if not force:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=duplicate_info,
                )

    # ----------------------------------------------------------------
    # Préparation du document MongoDB à insérer
    # ----------------------------------------------------------------
    # On convertit le modèle Pydantic en dict Python
    doc = payload.model_dump()

    # Génère un identifiant unique côté backend
    doc["prospect_id"] = str(uuid4())

    # Champs normalisés (utiles pour index et détection de doublons)
    doc["email_norm"] = email_norm
    doc["telephone_norm"] = telephone_norm

    # Flag pour autoriser les doublons si force=true
    doc["allow_duplicate"] = bool(force)

    # ----------------------------------------------------------------
    # Insertion en base MongoDB
    # ----------------------------------------------------------------
    try:
        await col.insert_one(doc)

    except DuplicateKeyError:
        # Cas rare : 2 requêtes simultanées passent la vérification
        # mais Mongo bloque la 2e grâce à l'index unique

        existing = None
        if or_filters:
            existing = await col.find_one(
                {"$or": or_filters},
                {"prospect_id": 1}
            )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Doublon détecté (conflit d'insertion)",
                "existing_prospect_id": (existing or {}).get("prospect_id"),
            },
        )

    # ----------------------------------------------------------------
    # Réponse HTTP 201 : prospect créé
    # ----------------------------------------------------------------
    return doc

# -------------------------------------------------------------------
# Endpoint GET /prospects/{prospect_id}
# -------------------------------------------------------------------
@router.get("/{prospect_id}", response_model=ProspectOut, status_code=status.HTTP_200_OK)
async def get_prospect(prospect_id: str):
    """
    Récupère un prospect via son prospect_id (UUID).
    - Si introuvable : 404
    - Sinon : retourne toutes les infos (sans _id)
    """
    # Récupère la collection MongoDB "prospects"
    col = get_prospects_collection()

    # Recherche d'un document Mongo dont le champ "prospect_id"
    doc = await col.find_one({"prospect_id": prospect_id})
    # Si aucun document n'est trouvé
    if not doc:
        # On renvoie une erreur HTTP 404 (Not Found)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prospect introuvable",
        )

    # Si le prospect existe :
    # - on nettoie le document Mongo (suppression de _id, champs techniques)
    # - FastAPI valide automatiquement la réponse avec ProspectOut
    return serialize_prospect(doc)

# -------------------------------------------------------------------
# Endpoint GET /prospects/
# -------------------------------------------------------------------
@router.get("", response_model=List[ProspectOut], status_code=status.HTTP_200_OK)
async def list_prospects():
    """
    Récupère la liste complète des prospects.

    - Retourne une liste (vide si aucun prospect)
    - Supprime les champs internes Mongo
    """

    # Récupère la collection MongoDB "prospects"
    col = get_prospects_collection()

    # Récupère tous les documents Mongo
    cursor = col.find({})

    prospects = []
    async for doc in cursor:
        prospects.append(serialize_prospect(doc))

    return prospects

# -------------------------------------------------------------------
# Endpoint GET /prospects/by-ids?ids=uuid1&ids=uuid2&ids=uuid3
# -------------------------------------------------------------------
@router.get("/by-ids", response_model=List[ProspectOut])
async def get_prospects_by_ids(
    ids: List[str] = Query(...)
):
    """
    Récupère une liste de prospects à partir d'une liste de prospect_id.
    """
    # Récupère la collection MongoDB "prospects"
    col = get_prospects_collection()

    # Recherche d'un document Mongo dont le champ correspond une liste des ids
    cursor = col.find({"prospect_id": {"$in": ids}})

    prospects = []
    async for doc in cursor:
        prospects.append(serialize_prospect(doc))

    return prospects