import os
import random
import time
import logging
from typing import Dict

import httpx
from celery import Celery
from pymongo import MongoClient
from bson import ObjectId

from app.utils.geocoding import geocode, build_query_from_fields

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Celery app (worker)
# ------------------------------------------------------------------
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery = Celery(
    "geocoding_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

# ------------------------------------------------------------------
# Mongo (sync, réservé au worker Celery)
# ------------------------------------------------------------------
MONGO_URI = os.getenv("MONGO_URI", os.getenv("MONGO_URL", "mongodb://mongodb:27017"))
MONGO_DB = os.getenv("MONGO_DB", "mimicom")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "prospects")


def _get_collection():
    client = MongoClient(MONGO_URI)
    return client[MONGO_DB][MONGO_COLLECTION]


# ------------------------------------------------------------------
# Geocoding tasks
# ------------------------------------------------------------------
RETRYABLE_STATUS = {429, 500, 502, 503, 504}


@celery.task(bind=True, name="geocode.prospect", max_retries=8)
def geocode_prospect_task(self, prospect_id: str) -> Dict:
    col = _get_collection()
    oid = ObjectId(prospect_id)

    doc = col.find_one({"_id": oid})
    if not doc:
        return {"status": "not_found", "prospect_id": prospect_id}

    if doc.get("lat") is not None and doc.get("lon") is not None:
        return {"status": "already_ok", "prospect_id": prospect_id}

    query = build_query_from_fields(
        doc.get("adresse"),
        doc.get("ville"),
        doc.get("departement"),
        doc.get("region"),
        doc.get("pays"),
    )
    if not query:
        col.update_one(
            {"_id": oid},
            {"$set": {"geocode_status": "failed", "geocode_error": "no_query"}},
        )
        return {"status": "no_address", "prospect_id": prospect_id}

    # jitter anti-rafale (réduit les 504)
    if self.request.retries == 0:
        time.sleep(random.uniform(0.05, 0.25))

    try:
        res = geocode(query)
    except httpx.HTTPStatusError as e:
        code = e.response.status_code if e.response else None
        if code in RETRYABLE_STATUS:
            countdown = min(300, (2 ** self.request.retries)) + random.randint(0, 3)
            raise self.retry(exc=e, countdown=countdown)
        col.update_one(
            {"_id": oid},
            {"$set": {"geocode_status": "failed", "geocode_error": f"http_{code}"}},
        )
        return {"status": "failed", "prospect_id": prospect_id, "reason": f"http_{code}"}

    except httpx.RequestError as e:
        countdown = min(300, (2 ** self.request.retries)) + random.randint(0, 3)
        raise self.retry(exc=e, countdown=countdown)

    if not res:
        col.update_one(
            {"_id": oid},
            {"$set": {"geocode_status": "failed", "geocode_error": "no_result"}},
        )
        return {"status": "not_found_in_provider", "prospect_id": prospect_id}

    col.update_one(
        {"_id": oid},
        {"$set": {
            "lat": res.lat,
            "lon": res.lon,
            "geocode_label": res.label,
            "geocode_provider": res.provider,
            "geocode_status": "ok",
            "geocode_error": None,
        }},
    )

    return {
        "status": "updated",
        "prospect_id": prospect_id,
        "lat": res.lat,
        "lon": res.lon,
        "provider": res.provider,
    }


@celery.task(name="geocode.backfill")
def geocode_backfill_task(limit: int = 500) -> Dict:
    col = _get_collection()

    cursor = col.find(
        {
            "$or": [
                {"lat": {"$exists": False}},
                {"lon": {"$exists": False}},
                {"lat": None},
                {"lon": None},
            ]
        },
        {"_id": 1},
    ).limit(limit)

    enqueued = 0
    for doc in cursor:
        geocode_prospect_task.delay(str(doc["_id"]))
        enqueued += 1

    return {"status": "enqueued", "count": enqueued, "limit": limit}
