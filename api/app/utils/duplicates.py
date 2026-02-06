from typing import Any, Dict, List
from utils.normalizers import normalize_email_for_db, normalize_phone_for_db

async def find_duplicates_for_payloads(col, payloads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    duplicates = []

    for i, p in enumerate(payloads):
        email_norm = normalize_email_for_db(p.get("email")) if p.get("email") else None
        tel_norm = normalize_phone_for_db(p.get("telephone")) if p.get("telephone") else None

        or_filters = []
        if email_norm:
            or_filters.append({"email_norm": email_norm, "allow_duplicate": {"$ne": True}})
        if tel_norm:
            or_filters.append({"telephone_norm": tel_norm, "allow_duplicate": {"$ne": True}})

        if not or_filters:
            continue

        existing = await col.find_one({"$or": or_filters}, {"prospect_id": 1, "email_norm": 1, "telephone_norm": 1})
        if existing:
            fields = []
            if email_norm and existing.get("email_norm") == email_norm:
                fields.append("email")
            if tel_norm and existing.get("telephone_norm") == tel_norm:
                fields.append("telephone")

            duplicates.append({
                "row_index": i,  # index dans valid_payloads
                "fields": fields,
                "existing_prospect_id": existing.get("prospect_id"),
            })

    return duplicates
