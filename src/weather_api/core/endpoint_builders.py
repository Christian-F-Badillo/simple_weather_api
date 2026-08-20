from weather_api.core.constants import (
    DEFAULT_FORECAST_DAYS,
    DEFAULT_LANG,
    EXT_API_API_KEY,
    EXT_API_BASE_URL,
    EXT_API_CURRENT_WEATHER_ENDPOINT,
    EXT_API_FORESCAST_ENDPOINT,
    EXT_API_SEARCH_ENDPOINT,
)


# Search builder
def get_url_search_by_city(
    city: str,
    lang: str = DEFAULT_LANG,
    api_key: str = EXT_API_API_KEY,
) -> str:
    return (
        f"{EXT_API_BASE_URL}{EXT_API_SEARCH_ENDPOINT}"
        f"?key={api_key}&q={city.strip()}&lang={lang}"
    )


# Current Weather builders
# -------------------------------------------------------------------------------
def get_url_current_weather_by_city(
    q: str,
    lang: str = DEFAULT_LANG,
    api_key: str = EXT_API_API_KEY,
) -> str:
    return (
        f"{EXT_API_BASE_URL}{EXT_API_CURRENT_WEATHER_ENDPOINT}"
        f"?key={api_key}&q={q.strip()}&lang={lang}"
    )


def get_url_current_weather_by_lat_lon(
    lat: float,
    lon: float,
    lang: str = DEFAULT_LANG,
    api_key: str = EXT_API_API_KEY,
) -> str:
    return (
        f"{EXT_API_BASE_URL}{EXT_API_CURRENT_WEATHER_ENDPOINT}"
        f"?key={api_key}&q={lat},{lon}&lang={lang}"
    )


# Forecast Weather builders
# -------------------------------------------------------------------------------
def get_url_forecast_by_city(
    q: str,
    days: int = DEFAULT_FORECAST_DAYS,
    lang: str = DEFAULT_LANG,
    api_key: str = EXT_API_API_KEY,
) -> str:
    return (
        f"{EXT_API_BASE_URL}{EXT_API_FORESCAST_ENDPOINT}"
        f"?key={api_key}&q={q.strip()}&days={days}&lang={lang}"
    )


def get_url_forecast_by_lat_lon(
    lat: float,
    lon: float,
    days: int = DEFAULT_FORECAST_DAYS,
    lang: str = DEFAULT_LANG,
    api_key: str = EXT_API_API_KEY,
) -> str:
    return (
        f"{EXT_API_BASE_URL}{EXT_API_FORESCAST_ENDPOINT}"
        f"?key={api_key}&q={lat},{lon}&days={days}&lang={lang}"
    )
