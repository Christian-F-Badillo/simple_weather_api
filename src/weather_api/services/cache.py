import logging

from redis.exceptions import RedisError

from weather_api.core.protocols import NO_CACHE_BACKEND, CacheBackend

logger = logging.getLogger(__name__)


# We suppose the use of redis as backend
class CacheService:
    def __init__(self, backend: CacheBackend = NO_CACHE_BACKEND) -> None:
        self._backend = backend

    async def get(self, key: str) -> str | None:
        try:
            return await self._backend.get(key)
        except RedisError as exc:
            logger.warning(f"[ERROR] Error in reading from cache ({key}): {exc}")
            return None

    async def set(self, key: str, value: str, ttl_seconds: int = 900) -> bool:
        try:
            return bool(await self._backend.set(key, value, ttl_seconds))
        except RedisError as exc:
            logger.warning(f"[ERROR] Error in writting to cache ({key}): {exc}")
            return False
