from typing import Optional

from redis.asyncio import Redis

from backend.config import RedisSettings

_client: Optional[Redis] = None


async def connect_redis(settings: RedisSettings) -> None:
    global _client

    if _client is not None:
        raise RuntimeError("Redis client is already initialized")

    client = Redis.from_url(settings.url, decode_responses=True)
    try:
        await client.ping()
    except Exception:
        await client.aclose()
        raise

    _client = client


def get_redis_client() -> Redis:
    if _client is None:
        raise RuntimeError("Redis is not configured or has not been initialized")
    return _client


async def close_redis() -> None:
    global _client

    client = _client
    _client = None
    if client is not None:
        await client.aclose()
