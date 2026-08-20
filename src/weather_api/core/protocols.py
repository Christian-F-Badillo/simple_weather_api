from collections.abc import Awaitable
from typing import Any, Protocol, runtime_checkable

import httpx

from weather_api.core.constants import DEFAULT_FORECAST_DAYS, DEFAULT_LANG
from weather_api.schemas.api_schemas import (
    CurrentWeatherReport,
    ForecastWeatherReport,
    SearchResultsMap,
)


@runtime_checkable
class CacheBackend(Protocol):
    def get(self, key: str) -> Awaitable[str | None]: ...

    def set(self, key: str, value: str, ex: int | None = None) -> Awaitable[bool]: ...

    def delete(self, key: str) -> Awaitable[None]: ...


@runtime_checkable
class HttpClientBackend(Protocol):
    def get(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Awaitable[httpx.Response]: ...


@runtime_checkable
class WeatherServiceProtocol(Protocol):
    def get_current(
        self, query: str, lang: str = DEFAULT_LANG
    ) -> Awaitable[CurrentWeatherReport]: ...

    def get_forecast(
        self, query: str, days: int = DEFAULT_FORECAST_DAYS, lang: str = DEFAULT_LANG
    ) -> Awaitable[ForecastWeatherReport]: ...


@runtime_checkable
class SearchServiceProtocol(Protocol):
    def search_locations(self, query: str) -> Awaitable[SearchResultsMap]: ...


class InactiveCacheBackend:
    """
    Inactive backed cache implementation
    """

    _instance: "InactiveCacheBackend | None" = None

    def __new__(cls) -> "InactiveCacheBackend":
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    async def get(self, key: str) -> None:
        return None

    async def set(self, key: str, value: str, ex: int | None = None) -> bool:
        return False

    async def delete(self, key: str) -> None:
        return None

    def __repr__(self) -> str:
        return "<InactiveCacheBackend: NO-ACTIVE>"


NO_CACHE_BACKEND = InactiveCacheBackend()
