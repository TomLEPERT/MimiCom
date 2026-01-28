from typing import Any, Dict, List, Optional
from uuid import uuid4
from datetime import datetime, timezone
import re

from fastapi import APIRouter, HTTPException, Query, status
from pymongo.errors import DuplicateKeyError
from ..db.prospects import get_prospects_collection
from ..models.prospect import ProspectCreate, ProspectOut, ProspectUpdate
from ..utils.normalizers import normalize_email_for_db, normalize_phone_for_db
from ..utils.mongo_serializers import serialize_prospect
from ..db.logs import get_logs_collection
from ..utils.diff import compute_diff
from ..models.log import LogOut
from ..utils.serializers import serialize_log


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

# -------------------------------------------------------------------
# Endpoint PATCH /prospects/{prospect_id}
# -------------------------------------------------------------------
@router.patch("/{prospect_id}", response_model=ProspectOut, status_code=status.HTTP_200_OK)
async def update_prospect(
    prospect_id: str,
    payload: ProspectUpdate,
    force: bool = Query(default=False),
):
    """
    Met à jour partiellement un prospect.

    Règles :
    - prospect_id n'est jamais modifiable
    - email/téléphone → contrôle des doublons
    - doublon + force=false → 409
    - doublon + force=true → update autorisée
    - logs créés pour chaque champ réellement modifié
    """

    col = get_prospects_collection()

    # ---------------------------------------------------------------
    # Vérifier que le prospect existe
    # ---------------------------------------------------------------
    existing = await col.find_one({"prospect_id": prospect_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prospect introuvable",
        )

    # ---------------------------------------------------------------
    # Récupérer uniquement les champs envoyés par le client
    # ---------------------------------------------------------------
    updates: Dict[str, Any] = payload.model_dump(exclude_unset=True)

    # Sécurité : on empêche toute modification du prospect_id
    updates.pop("prospect_id", None)

    # ---------------------------------------------------------------
    # Normalisation email / téléphone (si fournis)
    # ---------------------------------------------------------------
    email_norm: Optional[str] = None
    telephone_norm: Optional[str] = None

    email_provided = "email" in updates
    telephone_provided = "telephone" in updates

    if email_provided:
        email_norm = normalize_email_for_db(updates.get("email"))

    if telephone_provided:
        telephone_norm = normalize_phone_for_db(updates.get("telephone"))

    # ---------------------------------------------------------------
    # Vérification des doublons (email / téléphone)
    # ---------------------------------------------------------------
    or_filters: List[Dict[str, Any]] = []

    if email_provided and email_norm:
        or_filters.append(
            {
                "email_norm": email_norm,
                "allow_duplicate": {"$ne": True},
                "prospect_id": {"$ne": prospect_id},
            }
        )

    if telephone_provided and telephone_norm:
        or_filters.append(
            {
                "telephone_norm": telephone_norm,
                "allow_duplicate": {"$ne": True},
                "prospect_id": {"$ne": prospect_id},
            }
        )

    if or_filters:
        duplicate = await col.find_one(
            {"$or": or_filters},
            {"prospect_id": 1, "email_norm": 1, "telephone_norm": 1},
        )

        if duplicate:
            fields = []
            if email_norm and duplicate.get("email_norm") == email_norm:
                fields.append("email")
            if telephone_norm and duplicate.get("telephone_norm") == telephone_norm:
                fields.append("telephone")

            if not force:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "message": "Doublon détecté",
                        "fields": fields,
                        "existing_prospect_id": duplicate.get("prospect_id"),
                    },
                )

            # force=true -> on autorise le doublon
            updates["allow_duplicate"] = True

    # ---------------------------------------------------------------
    # Préparer la mise à jour MongoDB
    # ---------------------------------------------------------------
    set_doc: Dict[str, Any] = {}
    unset_doc: Dict[str, Any] = {}

    set_doc.update(updates)

    # email_norm
    if email_provided:
        if email_norm:
            set_doc["email_norm"] = email_norm
        else:
            unset_doc["email_norm"] = ""

    # telephone_norm
    if telephone_provided:
        if telephone_norm:
            set_doc["telephone_norm"] = telephone_norm
        else:
            unset_doc["telephone_norm"] = ""

    mongo_update: Dict[str, Any] = {"$set": set_doc}
    if unset_doc:
        mongo_update["$unset"] = unset_doc

    # ---------------------------------------------------------------
    # Appliquer la mise à jour
    # ---------------------------------------------------------------
    try:
        await col.update_one({"prospect_id": prospect_id}, mongo_update)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "Doublon détecté (conflit d'index)"},
        )

    # Relire le document mis à jour
    updated = await col.find_one({"prospect_id": prospect_id})

    # ---------------------------------------------------------------
    # LOGS — journalisation des modifications (Ticket 3.6)
    # ---------------------------------------------------------------
    if updates:
        fields_to_log = list(updates.keys())

        # Sécurité : on ne log jamais prospect_id
        if "prospect_id" in fields_to_log:
            fields_to_log.remove("prospect_id")

        diffs = compute_diff(existing, updated, fields_to_log)

        if diffs:
            logs_col = get_logs_collection()
            user = "system"  # placeholder MVP
            now = datetime.now(timezone.utc)

            log_docs = []
            for field, old_val, new_val in diffs:
                log_docs.append(
                    {
                        "prospect_id": prospect_id,
                        "field": field,
                        "old_value": old_val,
                        "new_value": new_val,
                        "changed_at": now,
                        "user": user,
                    }
                )

            await logs_col.insert_many(log_docs)

    # ---------------------------------------------------------------
    # Retour API
    # ---------------------------------------------------------------
    return serialize_prospect(updated)

# -------------------------------------------------------------------
# Endpoint DELETE /prospects/{prospect_id}
# -------------------------------------------------------------------
@router.delete("/{prospect_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prospect(prospect_id: str):
    """
    Supprime un prospect via son prospect_id.

    - Si le prospect n'existe pas : 404
    - Sinon : suppression + 204 No Content
    """
    col = get_prospects_collection()

    res = await col.delete_one({"prospect_id": prospect_id})

    # delete_one renvoie deleted_count = 0 si rien n'a été supprimé
    if res.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prospect introuvable",
        )

    # 204 → pas de body
    return

# -------------------------------------------------------------------
# GET /prospects/{prospect_id}/logs
# -------------------------------------------------------------------
@router.get("/{prospect_id}/logs", response_model=List[LogOut], status_code=status.HTTP_200_OK)
async def get_prospect_logs(
    prospect_id: str,
    # Nombre maximum de logs à retourner
    # - par défaut : 50
    # - minimum : 1
    # - maximum : 200
    limit: int = Query(default=50, ge=1, le=200),

    # Nombre de logs à ignorer (pagination)
    # ex: skip=50 -> page suivante
    skip: int = Query(default=0, ge=0),
):
    """
    Récupère les logs d'un prospect (triés du plus récent au plus ancien).

    - 404 si le prospect n'existe pas
    - pagination via skip/limit
    """

    # Récupère la collection MongoDB "prospects"
    prospects_col = get_prospects_collection()

    # Vérifie l'existence du prospect
    # On ne récupère que le champ prospect_id
    exists = await prospects_col.find_one(
        {"prospect_id": prospect_id},
        {"prospect_id": 1}
    )

    # Si le prospect n'existe pas -> erreur 404
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prospect introuvable",
        )

    # Récupère la collection MongoDB "logs"
    logs_col = get_logs_collection()

    # Création de la requête Mongo :
    # - uniquement les logs du prospect
    # - triés du plus récent au plus ancien
    # - pagination via skip/limit
    cursor = (
        logs_col.find({"prospect_id": prospect_id})
        .sort("changed_at", -1)
        .skip(skip)
        .limit(limit)
    )

    # Liste qui contiendra les logs finaux
    logs: List[LogOut] = []

    # Parcours asynchrone des documents Mongo
    async for doc in cursor:
        # serialize_log :
        # - supprime _id
        # - convertit les dates
        # - rend le document JSON-compatible
        logs.append(serialize_log(doc))

    # Retourne la liste des logs
    # FastAPI valide automatiquement avec LogOut
    return logs


# -------------------------------------------------------------------
# GET /logs/all
# -------------------------------------------------------------------
@router.get("/logs/all", response_model=List[LogOut], status_code=status.HTTP_200_OK)
async def list_logs(
    # Pagination
    limit: int = Query(default=50, ge=1, le=200),
    skip: int = Query(default=0, ge=0),

    # Filtres optionnels
    user: Optional[str] = Query(default=None),        # utilisateur ayant fait la modif
    field: Optional[str] = Query(default=None),       # champ modifié
    prospect_id: Optional[str] = Query(default=None), # prospect concerné
):
    """
    Récupère tous les logs (triés du plus récent au plus ancien).

    Filtres optionnels :
    - user
    - field (nom du champ modifié)
    - prospect_id
    """

    # Récupère la collection MongoDB "logs"
    logs_col = get_logs_collection()

    # Dictionnaire de filtres Mongo
    query = {}

    # Ajoute dynamiquement les filtres s'ils sont fournis
    if user:
        query["user"] = user

    if field:
        query["field"] = field

    if prospect_id:
        query["prospect_id"] = prospect_id

    # Requête Mongo :
    # - filtres dynamiques
    # - tri décroissant par date
    # - pagination
    cursor = (
        logs_col.find(query)
        .sort("changed_at", -1)
        .skip(skip)
        .limit(limit)
    )

    # Liste de sortie
    logs: List[LogOut] = []

    # Parcours des logs
    async for doc in cursor:
        logs.append(serialize_log(doc))

    # Retourne la liste des logs
    return logs

@router.get("/search", response_model=List[ProspectOut], status_code=status.HTTP_200_OK)
async def search_prospects(
    # Recherche texte
    nom: Optional[str] = Query(default=None),

    type_prospect: Optional[str] = Query(default=None),
    region: Optional[str] = Query(default=None),
    departement: Optional[str] = Query(default=None),

    statut: Optional[str] = Query(default=None),
    accepte_contact: Optional[bool] = Query(default=None),

    email: Optional[bool] = Query(default=None),
    telephone: Optional[bool] = Query(default=None),
    sit_web: Optional[bool] = Query(default=None),

    # Filtres numériques
    min_nb_aderents: Optional[int] = Query(default=None, ge=0),
    max_nb_aderents: Optional[int] = Query(default=None, ge=0),

    min_followers_total: Optional[int] = Query(default=None, ge=0),
    max_followers_total: Optional[int] = Query(default=None, ge=0),

    # Tri optionnel
    sort_by: str = Query(default="nom_structure"),
    sort_dir: str = Query(default="asc"),
):
    """
    Recherche des prospects par filtres (sans pagination).

    - 'nom' filtre sur nom_structure (regex, insensible à la casse)
    - calcule nb_follower_total = max(facebook/x/instagram/youtube/tictok followers)
    - ignore automatiquement les filtres non fournis (None)
    """

    col = get_prospects_collection()

    # ------------------------------------------------------------
    # Construction du filtre Mongo ($match)
    # ------------------------------------------------------------
    match: Dict[str, Any] = {}

    # Filtre nom_structure (recherche partielle)
    if nom:
        pattern = re.escape(nom.strip())
        match["nom_structure"] = {"$regex": pattern, "$options": "i"}

    if type_prospect is not None:
        match["type_prospect"] = type_prospect

    if region is not None:
        match["region"] = region

    if departement is not None:
        match["departement"] = departement

    if statut is not None:
        match["statut"] = statut

    if accepte_contact is not None:
        match["accepte_contact"] = accepte_contact

    # Filtres exacts email/tel/site
    def _present(field: str) -> Dict[str, Any]:
        return {field: {"$exists": True, "$type": "string", "$ne": ""}}

    def _missing(field: str) -> Dict[str, Any]:
        return {"$or": [
            {field: {"$exists": False}},
            {field: None},
            {field: ""},
        ]}

    # email bool
    if email is True:
        match.update(_present("email"))
    elif email is False:
        match["$and"] = match.get("$and", [])
        match["$and"].append(_missing("email"))

    # telephone bool
    if telephone is True:
        match.update(_present("telephone"))
    elif telephone is False:
        match["$and"] = match.get("$and", [])
        match["$and"].append(_missing("telephone"))

    # sit_web bool
    if sit_web is True:
        match.update(_present("sit_web"))
    elif sit_web is False:
        match["$and"] = match.get("$and", [])
        match["$and"].append(_missing("sit_web"))

    # nb_aderents min/max
    if min_nb_aderents is not None or max_nb_aderents is not None:
        match["nb_aderents"] = {}
        if min_nb_aderents is not None:
            match["nb_aderents"]["$gte"] = min_nb_aderents
        if max_nb_aderents is not None:
            match["nb_aderents"]["$lte"] = max_nb_aderents

    # ------------------------------------------------------------
    # Pipeline aggregation (calcul nb_follower_total)
    # ------------------------------------------------------------
    pipeline: List[Dict[str, Any]] = [
        {"$match": match},
        {
            "$addFields": {
                # max(...) en considérant None comme 0
                "nb_follower_total": {
                    "$max": [
                        {"$ifNull": ["$facebook_followers", 0]},
                        {"$ifNull": ["$x_followers", 0]},
                        {"$ifNull": ["$instagram_followers", 0]},
                        {"$ifNull": ["$youtube_followers", 0]},
                        {"$ifNull": ["$tictok_followers", 0]},
                    ]
                }
            }
        },
    ]

    # Filtre min/max sur nb_follower_total (champ calculé)
    if min_followers_total is not None or max_followers_total is not None:
        cond: Dict[str, Any] = {}
        if min_followers_total is not None:
            cond["$gte"] = min_followers_total
        if max_followers_total is not None:
            cond["$lte"] = max_followers_total
        pipeline.append({"$match": {"nb_follower_total": cond}})

    # ------------------------------------------------------------
    # Tri
    # ------------------------------------------------------------
    allowed_sort = {
        "nom_structure",
        "type_prospect",
        "region",
        "departement",
        "nb_aderents",
        "nb_follower_total",
    }
    if sort_by not in allowed_sort:
        sort_by = "nom_structure"

    direction = 1 if sort_dir.lower() == "asc" else -1
    pipeline.append({"$sort": {sort_by: direction}})

    # ------------------------------------------------------------
    # Exécution + sérialisation
    # ------------------------------------------------------------
    results: List[Dict[str, Any]] = []
    cursor = col.aggregate(pipeline)

    async for doc in cursor:
        results.append(serialize_prospect(doc))

    return results