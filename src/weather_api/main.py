from fastapi import FastAPI

from weather_api.api.dependencies import app_lifespan
from weather_api.api.v1.endpoints import search, weather

app = FastAPI(
    title="Weather & Geocoding API Gateway",
    version="1.0.0",
    lifespan=app_lifespan,
)

app.include_router(weather.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
