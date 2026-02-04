import uuid
from typing import Optional

from .redis_client import get_redis

LOCK_TTL_SECONDS = 600


async def acquire_import_lock(import_id: str) -> Optional[str]:
    """
    Tente de prendre un lock Redis pour un import.
    Retourne un token si lock acquis, sinon None.
    """
    redis = get_redis()
    lock_key = f"import_lock:{import_id}"
    token = str(uuid.uuid4())

    ok = await redis.set(lock_key, token, nx=True, ex=LOCK_TTL_SECONDS)
    return token if ok else None


async def release_import_lock(import_id: str, token: str) -> None:
    """
    Libère le lock uniquement si le token correspond.
    """
    redis = get_redis()
    lock_key = f"import_lock:{import_id}"

    current = await redis.get(lock_key)
    if current == token:
        await redis.delete(lock_key)
