from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status

from weather_api.api.dependencies import get_weather_service
from weather_api.core.constants import (
    DEFAULT_FORECAST_DAYS,
    DEFAULT_LANG,
    MAX_FORECAST_DAYS,
    MIN_FORECAST_DAYS,
)
from weather_api.schemas.api_schemas import CurrentWeatherReport, ForecastWeatherReport
from weather_api.services.weather import WeatherService

router = APIRouter(prefix="/weather", tags=["Weather"])


# Current Weather Endpoints
# ----------------------------------------------------------------------------------------------------------------------------
@router.get(
    "/current",
    response_model=CurrentWeatherReport,
    status_code=status.HTTP_200_OK,
    summary="Get the current weather of a city",
    description="Consult the current weather by the city name. You can user the search API to search for the city names.",
)
async def get_current_weather(
    q: Annotated[
        str,
        Query(
            description="City name",
            examples=["Monterrey", "London"],
        ),
    ],
    service: Annotated[WeatherService, Depends(get_weather_service)],
    lang: Annotated[
        str,
        Query(
            description="Language code of the response. ",
            examples=["es", "en"],
        ),
    ] = DEFAULT_LANG,
) -> CurrentWeatherReport:
    try:
        return await service.get_current_by_city(city=q, lang=lang)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 400:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Location not found: '{q}'",
            )
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Error from weather provider: {exc.response.text}",
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Connection error with provider: {str(exc)}",
        )


@router.get(
    "/current/coords",
    response_model=CurrentWeatherReport,
    status_code=status.HTTP_200_OK,
    summary="Get the current weather with geolocation data: lat, lon.",
)
async def get_current_weather_by_coords(
    lat: Annotated[
        float,
        Query(ge=-90.0, le=90.0, description="Lat", examples=[19.29]),
    ],
    lon: Annotated[
        float,
        Query(ge=-180.0, le=180.0, description="Lon", examples=[-99.17]),
    ],
    service: Annotated[WeatherService, Depends(get_weather_service)],
    lang: Annotated[
        str,
        Query(
            description="Language code of the response. ",
            examples=["es", "en"],
        ),
    ] = DEFAULT_LANG,
) -> CurrentWeatherReport:
    try:
        return await service.get_current_by_coords(lat=lat, lon=lon, lang=lang)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Error en proveedor de clima: {exc.response.text}",
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Error de conexión: {str(exc)}",
        )


# Forecast Endpoints
# ---------------------------------------------------------------------------------------------------------------------------


@router.get(
    "/forecast",
    response_model=ForecastWeatherReport,
    status_code=status.HTTP_200_OK,
    summary="Get weather forecast by city",
    description="Return a summary of the weather forecast hourly for each day.",
)
async def get_forecast(
    q: Annotated[
        str,
        Query(
            description="City name",
            examples=["Querétaro", "Madrid"],
        ),
    ],
    service: Annotated[WeatherService, Depends(get_weather_service)],
    days: Annotated[
        int,
        Query(
            ge=MIN_FORECAST_DAYS,
            le=MAX_FORECAST_DAYS,
            description=f"Forecast days (min {MIN_FORECAST_DAYS}, max {MAX_FORECAST_DAYS})",
        ),
    ] = DEFAULT_FORECAST_DAYS,
    lang: Annotated[
        str,
        Query(
            description="Language code of the response. ",
            examples=["es", "en"],
        ),
    ] = DEFAULT_LANG,
) -> ForecastWeatherReport:
    try:
        return await service.get_forecast_by_city(city=q, days=days, lang=lang)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 400:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Location not found: '{q}'",
            )
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Error with weather provider: {exc.response.text}",
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Connection error with provider: {str(exc)}",
        )


@router.get(
    "/forecast/coords",
    response_model=ForecastWeatherReport,
    status_code=status.HTTP_200_OK,
    summary="Get weather forecast by geolocation: lat, lon",
)
async def get_forecast_by_coords(
    lat: Annotated[
        float,
        Query(ge=-90.0, le=90.0, description="Lat", examples=[20.59]),
    ],
    lon: Annotated[
        float,
        Query(ge=-180.0, le=180.0, description="Lon", examples=[-100.39]),
    ],
    service: Annotated[WeatherService, Depends(get_weather_service)],
    days: Annotated[
        int,
        Query(
            ge=MIN_FORECAST_DAYS,
            le=MAX_FORECAST_DAYS,
            description=f"Forecast days (min {MIN_FORECAST_DAYS}, max {MAX_FORECAST_DAYS})",
        ),
    ] = DEFAULT_FORECAST_DAYS,
    lang: Annotated[
        str,
        Query(
            description="Language code of the response. ",
            examples=["es", "en"],
        ),
    ] = DEFAULT_LANG,
) -> ForecastWeatherReport:
    try:
        return await service.get_forecast_by_coords(
            lat=lat, lon=lon, days=days, lang=lang
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Error with weather provider: {exc.response.text}",
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Connection error with provider: {str(exc)}",
        )
