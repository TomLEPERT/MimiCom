import json
from typing import Any, Dict, Optional
from datetime import datetime, timezone

from .redis_client import get_redis

PROGRESS_TTL_SECONDS = 60 * 60  # 1h


def _progress_key(import_id: str) -> str:
    return f"import_progress:{import_id}"


def _result_key(import_id: str) -> str:
    return f"import_result:{import_id}"


async def set_progress(import_id: str, data: Dict[str, Any]) -> None:
    redis = get_redis()
    payload = {
        **data,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    await redis.setex(_progress_key(import_id), PROGRESS_TTL_SECONDS, json.dumps(payload))


async def get_progress(import_id: str) -> Optional[Dict[str, Any]]:
    redis = get_redis()
    raw = await redis.get(_progress_key(import_id))
    return json.loads(raw) if raw else None


async def set_result(import_id: str, data: Dict[str, Any]) -> None:
    redis = get_redis()
    await redis.setex(_result_key(import_id), PROGRESS_TTL_SECONDS, json.dumps(data))


async def get_result(import_id: str) -> Optional[Dict[str, Any]]:
    redis = get_redis()
    raw = await redis.get(_result_key(import_id))
    return json.loads(raw) if raw else None
