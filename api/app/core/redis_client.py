import os
from redis.asyncio import Redis
from redis.asyncio import from_url

_redis: Redis | None = None


def get_redis() -> Redis:
    """
    Redis singleton (async client).
    REDIS_URL exemple: redis://localhost:6379/0
    """
    global _redis
    if _redis is None:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        _redis = from_url(redis_url, decode_responses=True)
    return _redis