import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

import httpx
import redis.asyncio as aioredis
from fastapi import Depends, FastAPI
from redis.exceptions import RedisError

from weather_api.core.constants import EXT_API_BASE_URL, REDIS_URL
from weather_api.core.protocols import NO_CACHE_BACKEND, CacheBackend, HttpClientBackend
from weather_api.services.cache import CacheService
from weather_api.services.search import SearchService
from weather_api.services.weather import WeatherService

logger = logging.getLogger(__name__)


class ServiceContainer:
    def __init__(self) -> None:
        self.http_client: httpx.AsyncClient | None = None
        self.cache_backend: CacheBackend = NO_CACHE_BACKEND
        self._raw_redis: aioredis.Redis | None = None

    async def startup(self) -> None:
        self.http_client = httpx.AsyncClient(
            base_url=EXT_API_BASE_URL,
            timeout=httpx.Timeout(connect=3.0, read=5.0, write=5.0, pool=10.0),
        )

        try:
            redis_inst = aioredis.from_url(REDIS_URL)
            await redis_inst.ping()

            self._raw_redis = redis_inst
            self.cache_backend = redis_inst
            logger.info("[INFO] Correct connection to Redis Cache Backend.")

        except (RedisError, OSError) as exc:
            logger.warning(
                f"[WARNING] Unable to create connection to Redis Cache Backend ({exc}). Using API service without cache."
            )
            self.cache_backend = NO_CACHE_BACKEND

    async def shutdown(self) -> None:
        if self.http_client:
            await self.http_client.aclose()
        if self._raw_redis:
            await self._raw_redis.aclose()

        logger.info("[INFO] Connection to services closed sucessfully.")


container = ServiceContainer()


# Managment the life cicle of the API in fastAPI
@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[None]:
    await container.startup()
    yield
    await container.shutdown()


def get_http_client() -> HttpClientBackend:
    if container.http_client is None:
        logger.error("Http client not initialized")
        raise RuntimeError("Http Client has no been initialized.")

    return container.http_client


def get_cache_service() -> CacheService:
    return CacheService(backend=container.cache_backend)


def get_weather_service(
    http_client: Annotated[HttpClientBackend, Depends(get_http_client)],
    cache_service: Annotated[CacheService, Depends(get_cache_service)],
) -> WeatherService:
    return WeatherService(http_client=http_client, cache_service=cache_service)


def get_search_service(
    http_client: Annotated[HttpClientBackend, Depends(get_http_client)],
    cache_service: Annotated[CacheService, Depends(get_cache_service)],
) -> SearchService:
    return SearchService(http_client=http_client, cache_service=cache_service)
