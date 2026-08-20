from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status

from weather_api.api.dependencies import get_search_service
from weather_api.core.constants import DEFAULT_LANG, SEARCH_MIN_QUERY_LENGTH
from weather_api.schemas.api_schemas import SearchResultsMap
from weather_api.services.search import SearchService

router = APIRouter(prefix="/search", tags=["Search & Geocoding"])


@router.get(
    "",
    response_model=SearchResultsMap,
    status_code=status.HTTP_200_OK,
    summary="Search cities to resolve geolocation data",
    description="Returns a indexed map with all the coincidences found for the query.",
)
async def search_locations(
    q: Annotated[
        str,
        Query(
            min_lenght=SEARCH_MIN_QUERY_LENGTH,
            description="Search text (city name) partial or complete.",
            examples=["Santiago", "Madrid", "York"],
        ),
    ],
    service: Annotated[SearchService, Depends(get_search_service)],
    lang: Annotated[
        str,
        Query(
            description="Language code of the response. ",
            examples=["es", "en"],
        ),
    ] = DEFAULT_LANG,
) -> SearchResultsMap:
    try:
        return await service.search_by_city(city=q, lang=lang)
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error with geolocation provider: {e.response.text}",
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Connection timeout with provider: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error at processing search request: {str(e)}",
        )
