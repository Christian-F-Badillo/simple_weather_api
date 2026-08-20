import json
import logging
from typing import Any

from weather_api.core.constants import (
    CACHE_PREFIX_SEARCH,
    CACHE_TTL_SEARCH,
    DEFAULT_LANG,
)
from weather_api.core.endpoint_builders import get_url_search_by_city
from weather_api.core.protocols import HttpClientBackend
from weather_api.schemas.api_schemas import SearchResultsMap
from weather_api.services.cache import CacheService

logger = logging.getLogger(__name__)


class SearchService:
    def __init__(
        self,
        http_client: HttpClientBackend,
        cache_service: CacheService,
    ) -> None:
        self._http = http_client
        self._cache = cache_service

    async def search_by_city(
        self, city: str, lang: str = DEFAULT_LANG
    ) -> SearchResultsMap:
        clean_city = city.strip().lower()
        cache_key = f"{CACHE_PREFIX_SEARCH}:{clean_city}"

        cached = await self._cache.get(cache_key)
        if cached:
            return SearchResultsMap.model_validate_json(cached)

        target_url = get_url_search_by_city(clean_city, lang=lang)
        response = await self._http.get(target_url)
        response.raise_for_status()

        search_results = SearchResultsMap.from_raw_list(response.json())

        await self._cache.set(
            cache_key,
            search_results.model_dump_json(),
            ttl_seconds=CACHE_TTL_SEARCH,
        )

        return search_results
