import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()

# Credentials
EXT_API_API_KEY: Final[str] = os.getenv("WEATHER_API_KEY")
REDIS_PASSWORD: Final[str] = os.getenv("REDIS_PASSWORD")


# Redis Constants
REDIS_HOST: Final[str] = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT: Final[str] = os.getenv("REDIS_PORT", "6379")
REDIS_URL: Final[str] = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"


# External API endpoints
EXT_API_BASE_URL: Final[str] = "https://api.weatherapi.com/v1"
EXT_API_CURRENT_WEATHER_ENDPOINT: Final[str] = "/current.json"
EXT_API_FORESCAST_ENDPOINT: Final[str] = "/forecast.json"
EXT_API_SEARCH_ENDPOINT: Final[str] = "/search.json"

# Constants Forecast
DEFAULT_FORECAST_DAYS: Final[int] = 1
MIN_FORECAST_DAYS: Final[int] = 1
MAX_FORECAST_DAYS: Final[int] = 3
SEARCH_MIN_QUERY_LENGTH: Final[int] = 2
DEFAULT_LANG: Final[str] = "es"

# Cache Constants
CACHE_TTL_CURRENT: Final[int] = 60 * 15  # 15 min
CACHE_TTL_FORECAST: Final[int] = 60 * 30  # 30 min
CACHE_TTL_SEARCH: Final[int] = 60 * 60 * 24 * 7  # 7 days

CACHE_PREFIX_CURRENT: Final[str] = "weather:current"
CACHE_PREFIX_FORECAST: Final[str] = "weather:forecast"
CACHE_PREFIX_SEARCH: Final[str] = "weather:search"
