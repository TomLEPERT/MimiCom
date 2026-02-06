import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Set
from uuid import uuid4
import asyncio

from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError

from ..core.redis_client import get_redis
from ..db.prospects import get_prospects_collection
from ..models.prospect import ProspectCreate
from ..models.imports import (
    ImportPreviewResponse,
    ImportPreviewSummary,
    ImportStatus,
    InvalidRowError,
    DuplicateMatch,
    ImportCommitRequest,
    ImportCommitResponse,
    MergeStrategy,
)
from ..utils.normalizers import normalize_email_for_db, normalize_phone_for_db
from ..utils.csv_reader import read_csv_bytes
from ..core.redis_lock import acquire_import_lock, release_import_lock
from ..core.import_progress import set_progress, get_progress, set_result, get_result

router = APIRouter(prefix="/imports", tags=["imports"])

PREVIEW_TTL_SECONDS = 30 * 60  # 30 minutes


@router.post("/preview", response_model=ImportPreviewResponse, status_code=status.HTTP_200_OK)
async def import_preview(file: UploadFile = File(...)):
    """
    Preview import CSV:
    - parse + validate via ProspectCreate
    - détecte doublons (csv + db) via email_norm / telephone_norm
    - stocke le preview dans Redis (TTL)
    """

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Veuillez envoyer un fichier .csv")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Fichier vide")

    headers, rows = read_csv_bytes(content)

    required_columns = ["nom_structure", "type_prospect"]
    detected_norm = {h.strip() for h in headers if h}
    missing = [c for c in required_columns if c not in detected_norm]

    import_id = str(uuid4())
    summary = ImportPreviewSummary(
        total_rows=len(rows),
        valid_rows=0,
        invalid_rows=0,
        duplicates_in_csv=0,
        duplicates_in_db=0,
    )

    if missing:
        return ImportPreviewResponse(
            status=ImportStatus.INVALID_CSV,
            import_id=import_id,
            summary=summary,
            invalid=[
                InvalidRowError(
                    row_number=1,
                    raw={},
                    errors=[f"Colonnes manquantes: {', '.join(missing)}"],
                )
            ],
            duplicates=[],
            required_columns=required_columns,
            detected_columns=headers,
            message="CSV mal formatté (colonnes manquantes).",
        )

    invalid: List[InvalidRowError] = []
    duplicates: List[DuplicateMatch] = []
    valid_rows_for_commit: List[Dict[str, Any]] = []

    seen_email: Dict[str, int] = {}
    seen_phone: Dict[str, int] = {}

    email_norms: Set[str] = set()
    phone_norms: Set[str] = set()

    # rows est déjà une liste de dict => row_number = index+1
    for idx, raw in enumerate(rows, start=1):
        payload = {k: (v.strip() if isinstance(v, str) else v) for k, v in raw.items()}

        try:
            obj = ProspectCreate(**payload)
        except ValidationError as e:
            invalid.append(
                InvalidRowError(
                    row_number=idx,
                    raw=payload,
                    errors=[err["msg"] for err in e.errors()],
                )
            )
            continue

        doc = obj.model_dump()
        doc = {k: v for k, v in doc.items() if v is not None}

        email_norm = normalize_email_for_db(obj.email) if obj.email else None
        phone_norm = normalize_phone_for_db(obj.telephone) if obj.telephone else None

        if email_norm:
            doc["email_norm"] = email_norm
            email_norms.add(email_norm)

        if phone_norm:
            doc["telephone_norm"] = phone_norm
            phone_norms.add(phone_norm)

        doc["_row_number"] = idx

        # doublons internes csv
        if email_norm:
            if email_norm in seen_email:
                duplicates.append(
                    DuplicateMatch(
                        match_on="email",
                        email_normalized=email_norm,
                        telephone_normalized=None,
                        row_number=idx,
                        csv_row=payload,
                        existing_prospect_id=None,
                        existing_snapshot={"row_number": seen_email[email_norm]},
                        source="csv",
                    )
                )
            else:
                seen_email[email_norm] = idx

        if phone_norm:
            if phone_norm in seen_phone:
                duplicates.append(
                    DuplicateMatch(
                        match_on="telephone",
                        email_normalized=None,
                        telephone_normalized=phone_norm,
                        row_number=idx,
                        csv_row=payload,
                        existing_prospect_id=None,
                        existing_snapshot={"row_number": seen_phone[phone_norm]},
                        source="csv",
                    )
                )
            else:
                seen_phone[phone_norm] = idx

        valid_rows_for_commit.append(doc)

    summary.valid_rows = len(valid_rows_for_commit)
    summary.invalid_rows = len(invalid)
    summary.duplicates_in_csv = len([d for d in duplicates if d.source == "csv"])

    if summary.invalid_rows > 0:
        return ImportPreviewResponse(
            status=ImportStatus.INVALID_CSV,
            import_id=import_id,
            summary=summary,
            invalid=invalid,
            duplicates=[],
            required_columns=required_columns,
            detected_columns=headers,
            message="Certaines lignes sont invalides. Corrige le CSV puis réessaie.",
        )

    # ---- doublons DB
    col = get_prospects_collection()

    or_filters: List[Dict[str, Any]] = []
    if email_norms:
        or_filters.append({"email_norm": {"$in": list(email_norms)}, "allow_duplicate": {"$ne": True}})
    if phone_norms:
        or_filters.append({"telephone_norm": {"$in": list(phone_norms)}, "allow_duplicate": {"$ne": True}})

    existing_by_email: Dict[str, Dict[str, Any]] = {}
    existing_by_phone: Dict[str, Dict[str, Any]] = {}

    if or_filters:
        cursor = col.find(
            {"$or": or_filters},
            {
                "prospect_id": 1,
                "email_norm": 1,
                "telephone_norm": 1,
                "nom_structure": 1,
                "email": 1,
                "telephone": 1,
                "type_prospect": 1,
            },
        )
        async for d in cursor:
            if d.get("email_norm"):
                existing_by_email[d["email_norm"]] = d
            if d.get("telephone_norm"):
                existing_by_phone[d["telephone_norm"]] = d

    for doc in valid_rows_for_commit:
        row_number = doc["_row_number"]
        email_norm = doc.get("email_norm")
        phone_norm = doc.get("telephone_norm")

        hit_email = existing_by_email.get(email_norm) if email_norm else None
        hit_phone = existing_by_phone.get(phone_norm) if phone_norm else None

        if hit_email or hit_phone:
            if hit_email and hit_phone:
                match_on = "both"
                hit = hit_email
            elif hit_email:
                match_on = "email"
                hit = hit_email
            else:
                match_on = "telephone"
                hit = hit_phone

            duplicates.append(
                DuplicateMatch(
                    match_on=match_on,
                    email_normalized=email_norm,
                    telephone_normalized=phone_norm,
                    row_number=row_number,
                    csv_row={k: v for k, v in doc.items() if not k.startswith("_")},
                    existing_prospect_id=hit.get("prospect_id"),
                    existing_snapshot={
                        "prospect_id": hit.get("prospect_id"),
                        "nom_structure": hit.get("nom_structure"),
                        "email": hit.get("email"),
                        "telephone": hit.get("telephone"),
                        "type_prospect": hit.get("type_prospect"),
                    },
                    source="db",
                )
            )

    summary.duplicates_in_db = len([d for d in duplicates if d.source == "db"])

    if summary.duplicates_in_csv > 0 or summary.duplicates_in_db > 0:
        status_out = ImportStatus.DUPLICATES_FOUND
        msg = "Des doublons ont été détectés (email/téléphone). Choisis une stratégie de merge."
    else:
        status_out = ImportStatus.OK_TO_MERGE
        msg = "Tout est ok, on peut merger."

    # store redis
    redis_client = get_redis()
    preview_payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "headers": headers,
        "required_columns": required_columns,
        "summary": summary.model_dump(),
        "valid_rows": valid_rows_for_commit,
        "duplicates": [d.model_dump() for d in duplicates],
    }
    
    await redis_client.setex(
        f"import_preview:{import_id}",
        PREVIEW_TTL_SECONDS,
        json.dumps(jsonable_encoder(preview_payload)),
    )

    return ImportPreviewResponse(
        status=status_out,
        import_id=import_id,
        summary=summary,
        invalid=[],
        duplicates=duplicates,
        required_columns=required_columns,
        detected_columns=headers,
        message=msg,
    )

@router.post("/commit", response_model=ImportCommitResponse, status_code=status.HTTP_200_OK)
async def import_commit(payload: ImportCommitRequest):
    token = await acquire_import_lock(payload.import_id)
    if not token:
        raise HTTPException(
            status_code=409,
            detail="Un merge est déjà en cours pour cet import. Réessaie dans quelques secondes.",
        )

    try:
        result = await _run_commit(payload.import_id, payload.merge_strategy, payload.overrides)
        return ImportCommitResponse(**result)
    finally:
        await release_import_lock(payload.import_id, token)
        
@router.get("/progress")
async def import_progress(import_id: str):
    p = await get_progress(import_id)
    if not p:
        raise HTTPException(status_code=404, detail="Progress introuvable.")
    return p


@router.get("/result")
async def import_result(import_id: str):
    r = await get_result(import_id)
    if not r:
        raise HTTPException(status_code=404, detail="Résultat introuvable.")
    return r

async def _run_commit(
    import_id: str,
    merge_strategy: MergeStrategy,
    overrides: Dict[int, MergeStrategy] | None = None,
) -> Dict[str, Any]:
    overrides = overrides or {}

    redis_client = get_redis()
    key = f"import_preview:{import_id}"
    raw = await redis_client.get(key)

    if not raw:
        raise HTTPException(
            status_code=404,
            detail="Import introuvable ou expiré (Redis TTL). Relance un preview.",
        )

    preview = json.loads(raw)
    valid_rows: List[Dict[str, Any]] = preview.get("valid_rows", [])
    if not valid_rows:
        raise HTTPException(status_code=400, detail="Aucune ligne valide à merger.")

    # override seulement sur doublons DB
    duplicates = preview.get("duplicates", []) or []
    db_duplicate_rows: Set[int] = set()
    for d in duplicates:
        if d.get("source") == "db" and d.get("row_number") is not None:
            try:
                db_duplicate_rows.add(int(d["row_number"]))
            except (TypeError, ValueError):
                pass

    total = len(valid_rows)

    await set_progress(
        import_id,
        {"status": "running", "phase": "loading", "processed": 0, "total": total, "percent": 0},
    )

    col = get_prospects_collection()

    # --- lookup DB safe
    await set_progress(
        import_id,
        {"status": "running", "phase": "lookup_db", "processed": 0, "total": total, "percent": 2},
    )

    email_norms: Set[str] = set()
    phone_norms: Set[str] = set()
    for d in valid_rows:
        if d.get("email_norm"):
            email_norms.add(d["email_norm"])
        if d.get("telephone_norm"):
            phone_norms.add(d["telephone_norm"])

    or_filters: List[Dict[str, Any]] = []
    if email_norms:
        or_filters.append({"email_norm": {"$in": list(email_norms)}, "allow_duplicate": {"$ne": True}})
    if phone_norms:
        or_filters.append({"telephone_norm": {"$in": list(phone_norms)}, "allow_duplicate": {"$ne": True}})

    existing_by_email: Dict[str, Dict[str, Any]] = {}
    existing_by_phone: Dict[str, Dict[str, Any]] = {}

    if or_filters:
        cursor = col.find({"$or": or_filters}, {"prospect_id": 1, "email_norm": 1, "telephone_norm": 1})
        async for ex in cursor:
            if ex.get("email_norm"):
                existing_by_email[ex["email_norm"]] = ex
            if ex.get("telephone_norm"):
                existing_by_phone[ex["telephone_norm"]] = ex

    existing_email_to_id = {k: v["prospect_id"] for k, v in existing_by_email.items()}
    existing_phone_to_id = {k: v["prospect_id"] for k, v in existing_by_phone.items()}

    inserted = 0
    updated = 0
    ignored = 0
    errors: List[str] = []

    inserts: List[Dict[str, Any]] = []
    update_ops: List[UpdateOne] = []

    def _build_insert_doc(src: Dict[str, Any], force: bool) -> Dict[str, Any]:
        doc = {k: v for k, v in src.items() if not k.startswith("_")}
        doc["prospect_id"] = str(uuid4())

        email_norm = doc.get("email_norm")
        tel_norm = doc.get("telephone_norm")

        doc["allow_duplicate"] = bool(force)

        if email_norm:
            doc["email_unique_key"] = email_norm if not force else f"FORCED:{uuid4()}"
        if tel_norm:
            doc["telephone_unique_key"] = tel_norm if not force else f"FORCED:{uuid4()}"

        return doc

    # ---- build ops
    await set_progress(
        import_id,
        {"status": "running", "phase": "building_ops", "processed": 0, "total": total, "percent": 5},
    )

    processed = 0
    for src in valid_rows:
        email_norm = src.get("email_norm")
        tel_norm = src.get("telephone_norm")
        row_number = src.get("_row_number")

        # override autorisé uniquement si row_number ∈ doublons DB
        row_override = None
        rn = None
        if row_number is not None:
            try:
                rn = int(row_number)
            except (TypeError, ValueError):
                rn = None

        if rn is not None and rn in db_duplicate_rows:
            row_override = overrides.get(rn)

        effective_strategy = row_override or merge_strategy

        # match DB: priorité email puis telephone
        hit = None
        if email_norm and email_norm in existing_by_email:
            hit = existing_by_email[email_norm]
        elif tel_norm and tel_norm in existing_by_phone:
            hit = existing_by_phone[tel_norm]

        # IGNORE
        if effective_strategy == MergeStrategy.IGNORE_DUPLICATES:
            if hit:
                ignored += 1
            else:
                inserts.append(_build_insert_doc(src, force=False))

        # FORCE_ADD
        elif effective_strategy == MergeStrategy.FORCE_ADD:
            inserts.append(_build_insert_doc(src, force=True))

        # REPLACE_EXISTING
        elif effective_strategy == MergeStrategy.REPLACE_EXISTING:
            if hit:
                target_id = hit["prospect_id"]

                if email_norm and existing_email_to_id.get(email_norm) and existing_email_to_id[email_norm] != target_id:
                    ignored += 1
                    errors.append(
                        f"Ligne {rn or row_number}: email {email_norm} déjà utilisé par un autre prospect ({existing_email_to_id[email_norm]})."
                    )
                    processed += 1
                    continue

                if tel_norm and existing_phone_to_id.get(tel_norm) and existing_phone_to_id[tel_norm] != target_id:
                    ignored += 1
                    errors.append(
                        f"Ligne {rn or row_number}: téléphone {tel_norm} déjà utilisé par un autre prospect ({existing_phone_to_id[tel_norm]})."
                    )
                    processed += 1
                    continue

                update_doc = {k: v for k, v in src.items() if not k.startswith("_")}
                update_doc.pop("prospect_id", None)

                update_doc["allow_duplicate"] = False
                if email_norm:
                    update_doc["email_unique_key"] = email_norm
                if tel_norm:
                    update_doc["telephone_unique_key"] = tel_norm

                update_ops.append(UpdateOne({"prospect_id": target_id}, {"$set": update_doc}))
            else:
                inserts.append(_build_insert_doc(src, force=False))

        else:
            raise HTTPException(status_code=400, detail="merge_strategy invalide")

        processed += 1
        if processed % 25 == 0 or processed == total:
            pct = 5 + int((processed / total) * 60)  # 5 -> 65
            await set_progress(
                import_id,
                {"status": "running", "phase": "building_ops", "processed": processed, "total": total, "percent": pct},
            )

    # ---- bulk insert
    await set_progress(
        import_id,
        {"status": "running", "phase": "writing_inserts", "processed": total, "total": total, "percent": 70},
    )

    if inserts:
        try:
            res = await col.insert_many(inserts, ordered=False)
            inserted = len(res.inserted_ids)
        except BulkWriteError as bwe:
            errors.append(f"Bulk insert error: {bwe.details}")

    # ---- bulk update
    await set_progress(
        import_id,
        {"status": "running", "phase": "writing_updates", "processed": total, "total": total, "percent": 85},
    )

    if update_ops:
        try:
            res = await col.bulk_write(update_ops, ordered=False)
            updated = res.matched_count
        except BulkWriteError as bwe:
            errors.append(f"Bulk update error: {bwe.details}")

    # cleanup preview
    await redis_client.delete(key)

    result = {
        "import_id": import_id,
        "merge_strategy": merge_strategy,  # stratégie globale
        "inserted": inserted,
        "updated": updated,
        "ignored": ignored,
        "errors": errors,
        "message": "Merge terminé.",
        "overrides_count": len(overrides),
    }

    await set_result(import_id, result)
    await set_progress(
        import_id,
        {"status": "done", "phase": "done", "processed": total, "total": total, "percent": 100},
    )

    return result

@router.post("/commit-async", status_code=202)
async def import_commit_async(payload: ImportCommitRequest):
    token = await acquire_import_lock(payload.import_id)
    if not token:
        raise HTTPException(
            status_code=409,
            detail="Un merge est déjà en cours pour cet import. Réessaie dans quelques secondes.",
        )

    await set_progress(payload.import_id, {
        "status": "queued",
        "phase": "queued",
        "processed": 0,
        "total": 0,
        "percent": 0,
    })

    async def _task():
        try:
            await _run_commit(payload.import_id, payload.merge_strategy, payload.overrides)
        except Exception as e:
            await set_progress(payload.import_id, {
                "status": "error",
                "phase": "error",
                "processed": 0,
                "total": 0,
                "percent": 100,
                "error": str(e),
            })
        finally:
            await release_import_lock(payload.import_id, token)

    asyncio.create_task(_task())
    return {"import_id": payload.import_id, "status": "started"}