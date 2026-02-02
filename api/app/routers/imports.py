from uuid import uuid4
from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, File, UploadFile, HTTPException, status
from ..db.prospects import get_prospects_collection
from ..db.import_previews import get_import_previews_collection
from ..models.imports import ImportPreviewOut, ImportCommitIn, ImportCommitOut, ImportRowError, ImportRowDuplicate, ImportPreviewStats
from ..utils.csv_import import parse_csv_bytes, validate_rows
from ..utils.duplicates import find_duplicates_for_payloads
from .prospects import create_prospect

router = APIRouter(prefix="/imports", tags=["imports"])


# -------------------------------------------------------------------
# POST /imports/prospects/preview
# -------------------------------------------------------------------
@router.post("/prospects/preview", response_model=ImportPreviewOut, status_code=status.HTTP_200_OK)
async def preview_import_prospects(file: UploadFile = File(...)):
    """
    Preview import CSV :
    - lit le CSV
    - mappe vers payload ProspectCreate
    - valide Pydantic (sans insérer)
    - détecte doublons en base (sans insérer)
    - stocke un preview_id en Mongo (TTL)
    """

    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Fichier CSV requis.")

    csv_bytes = await file.read()

    rows = parse_csv_bytes(csv_bytes)
    valid_payloads, invalid = validate_rows(rows)

    prospects_col = get_prospects_collection()

    # Doublons uniquement sur les payloads valides
    duplicates_raw = await find_duplicates_for_payloads(prospects_col, valid_payloads)

    # On sépare : payloads valides NON doublons
    duplicate_indexes = {d["row_index"] for d in duplicates_raw}
    importables = [p for idx, p in enumerate(valid_payloads) if idx not in duplicate_indexes]

    preview_id = str(uuid4())
    now = datetime.now(timezone.utc)

    # Format erreurs / doublons pour UI
    invalid_rows = [
        {"row": row_no, "errors": errs, "raw": raw}
        for (row_no, errs, raw) in invalid
    ]

    duplicate_rows = [
        {
            "row": (d["row_index"] + 2),  # +2 car header=1 et enumerate start=2
            "fields": d["fields"],
            "existing_prospect_id": d["existing_prospect_id"],
        }
        for d in duplicates_raw
    ]

    doc = {
        "preview_id": preview_id,
        "created_at": now,
        "filename": file.filename,

        # stockage
        "rows_importable": importables,       # ok + pas doublon
        "rows_duplicates": [valid_payloads[d["row_index"]] for d in duplicates_raw],
        "rows_invalid": invalid_rows,
        "duplicates_meta": duplicate_rows,

        "stats": {
            "total": len(rows),
            "valid": len(valid_payloads),
            "invalid": len(invalid_rows),
            "duplicates": len(duplicate_rows),
        },
    }

    previews_col = get_import_previews_collection()
    await previews_col.insert_one(doc)

    return ImportPreviewOut(
        preview_id=preview_id,
        filename=file.filename,
        stats=ImportPreviewStats(**doc["stats"]),
        invalid_rows=[ImportRowError(**x) for x in invalid_rows],
        duplicate_rows=[ImportRowDuplicate(**x) for x in duplicate_rows],
    )


# -------------------------------------------------------------------
# POST /imports/prospects/commit
# -------------------------------------------------------------------
@router.post("/prospects/commit", response_model=ImportCommitOut, status_code=status.HTTP_200_OK)
async def commit_import_prospects(payload: ImportCommitIn):
    """
    Commit import à partir d'un preview_id :
    - force=false : insère uniquement rows_importable
    - force=true : insère rows_importable + rows_duplicates (en forçant)
    """

    previews_col = get_import_previews_collection()
    doc = await previews_col.find_one({"preview_id": payload.preview_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Preview introuvable ou expiré.")

    prospects_col = get_prospects_collection()

    rows_importable: List[Dict[str, Any]] = doc.get("rows_importable", [])
    rows_duplicates: List[Dict[str, Any]] = doc.get("rows_duplicates", [])
    rows_invalid = doc.get("rows_invalid", [])

    created = 0
    forced_created = 0
    skipped_duplicates = 0

    # 1) insère importables (normal)
    for p in rows_importable:
        # ici tu peux appeler ta logique create_prospect si tu veux (mais c’est un endpoint FastAPI)
        # plus simple : réutiliser la logique d'insertion interne si tu as une fonction dédiée.
        from uuid import uuid4
        from app.utils.normalizers import normalize_email_for_db, normalize_phone_for_db

        email_norm = normalize_email_for_db(p.get("email")) if p.get("email") else None
        tel_norm = normalize_phone_for_db(p.get("telephone")) if p.get("telephone") else None

        doc_to_insert = dict(p)
        doc_to_insert["prospect_id"] = str(uuid4())
        doc_to_insert["allow_duplicate"] = False
        if email_norm:
            doc_to_insert["email_norm"] = email_norm
            doc_to_insert["email_unique_key"] = email_norm
        if tel_norm:
            doc_to_insert["telephone_norm"] = tel_norm
            doc_to_insert["telephone_unique_key"] = tel_norm

        await prospects_col.insert_one(doc_to_insert)
        created += 1

    # 2) doublons
    if payload.force:
        for p in rows_duplicates:
            from uuid import uuid4
            from app.utils.normalizers import normalize_email_for_db, normalize_phone_for_db

            email_norm = normalize_email_for_db(p.get("email")) if p.get("email") else None
            tel_norm = normalize_phone_for_db(p.get("telephone")) if p.get("telephone") else None

            doc_to_insert = dict(p)
            doc_to_insert["prospect_id"] = str(uuid4())
            doc_to_insert["allow_duplicate"] = True

            # IMPORTANT : bypass index unique (clé random)
            if email_norm:
                doc_to_insert["email_norm"] = email_norm
                doc_to_insert["email_unique_key"] = f"FORCED:{uuid4()}"
            if tel_norm:
                doc_to_insert["telephone_norm"] = tel_norm
                doc_to_insert["telephone_unique_key"] = f"FORCED:{uuid4()}"

            await prospects_col.insert_one(doc_to_insert)
            forced_created += 1
    else:
        skipped_duplicates = len(rows_duplicates)

    return ImportCommitOut(
        preview_id=payload.preview_id,
        created=created + forced_created,
        forced_created=forced_created,
        skipped_invalid=len(rows_invalid),
        skipped_duplicates=skipped_duplicates,
    )