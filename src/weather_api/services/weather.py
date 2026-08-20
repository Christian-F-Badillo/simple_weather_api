import logging
from typing import Any

from weather_api.core.constants import (
    CACHE_PREFIX_CURRENT,
    CACHE_PREFIX_FORECAST,
    CACHE_TTL_CURRENT,
    CACHE_TTL_FORECAST,
    DEFAULT_FORECAST_DAYS,
    DEFAULT_LANG,
)
from weather_api.core.endpoint_builders import (
    get_url_current_weather_by_city,
    get_url_current_weather_by_lat_lon,
    get_url_forecast_by_city,
    get_url_forecast_by_lat_lon,
)
from weather_api.core.protocols import HttpClientBackend
from weather_api.schemas.api_schemas import CurrentWeatherReport, ForecastWeatherReport
from weather_api.schemas.raw_schemas import WeatherAPIResponse
from weather_api.services.cache import CacheService

logger = logging.getLogger(__name__)


class WeatherService:
    def __init__(
        self, http_client: HttpClientBackend, cache_service: CacheService
    ) -> None:
        self._http = http_client
        self._cache = cache_service

    async def _fetch_url(self, target_url: str) -> dict[str, Any]:
        response = await self._http.get(target_url)
        response.raise_for_status()

        return response.json()

    async def get_current_by_city(self, city: str, lang: str) -> CurrentWeatherReport:
        clean_city = city.strip().lower()
        clean_lang = lang.strip().lower()
        cache_key = f"{CACHE_PREFIX_CURRENT}:{clean_city}:{clean_lang}"

        cached = await self._cache.get(cache_key)

        if cached:
            return CurrentWeatherReport.model_validate_json(cached)

        endpoint = get_url_current_weather_by_city(clean_city, lang=clean_lang)
        raw_json_response = await self._fetch_url(endpoint)

        report = CurrentWeatherReport.from_raw(
            WeatherAPIResponse.model_validate(raw_json_response)
        )

        await self._cache.set(
            cache_key, report.model_dump_json(), ttl_seconds=CACHE_TTL_CURRENT
        )

        return report

    async def get_current_by_coords(
        self, lat: float, lon: float, lang: str = DEFAULT_LANG
    ) -> CurrentWeatherReport:
        clean_lang = lang.strip().lower()
        cache_key = (
            f"{CACHE_PREFIX_CURRENT}:{round(lat, 2)}:{round(lon, 2)}:{clean_lang}"
        )

        cached = await self._cache.get(cache_key)
        if cached:
            return CurrentWeatherReport.model_validate_json(cached)

        url = get_url_current_weather_by_lat_lon(lat, lon, lang=clean_lang)
        raw_json = await self._fetch_url(url)

        report = CurrentWeatherReport.from_raw(
            WeatherAPIResponse.model_validate(raw_json)
        )
        await self._cache.set(
            cache_key,
            report.model_dump_json(),
            ttl_seconds=CACHE_TTL_CURRENT,
        )
        return report

    async def get_forecast_by_city(
        self,
        city: str,
        days: int = DEFAULT_FORECAST_DAYS,
        lang: str = DEFAULT_LANG,
    ) -> ForecastWeatherReport:
        clean_city = city.strip().lower()
        clean_lang = lang.strip().lower()
        cache_key = f"{CACHE_PREFIX_FORECAST}:{clean_city}:{days}:{clean_lang}"

        cached = await self._cache.get(cache_key)
        if cached:
            return ForecastWeatherReport.model_validate_json(cached)

        url = get_url_forecast_by_city(clean_city, days=days, lang=clean_lang)
        raw_json = await self._fetch_url(url)

        report = ForecastWeatherReport.from_raw(
            WeatherAPIResponse.model_validate(raw_json)
        )
        await self._cache.set(
            cache_key,
            report.model_dump_json(),
            ttl_seconds=CACHE_TTL_FORECAST,
        )
        return report

    async def get_forecast_by_coords(
        self,
        lat: float,
        lon: float,
        days: int = DEFAULT_FORECAST_DAYS,
        lang: str = DEFAULT_LANG,
    ) -> ForecastWeatherReport:
        clean_lang = lang.strip().lower()
        cache_key = f"{CACHE_PREFIX_FORECAST}:{round(lat, 2)}:{round(lon, 2)}:{days}:{clean_lang}"

        cached = await self._cache.get(cache_key)
        if cached:
            return ForecastWeatherReport.model_validate_json(cached)

        url = get_url_forecast_by_lat_lon(lat, lon, days=days, lang=clean_lang)
        raw_json = await self._fetch_url(url)

        report = ForecastWeatherReport.from_raw(
            WeatherAPIResponse.model_validate(raw_json)
        )
        await self._cache.set(
            cache_key,
            report.model_dump_json(),
            ttl_seconds=CACHE_TTL_FORECAST,
        )
        return report
