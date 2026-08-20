# **Weather API Gateway & Caching Proxy**

An asynchronous microservice built with FastAPI that functions as an API Gateway and caching proxy in front of WeatherAPI. It provides a decoupled, strongly typed REST interface for querying weather and geocoding data, implementing distributed caching policies via Redis.

## **Architectural Features**

* **Dependency Inversion and Protocols:** Uses typing.Protocol to decouple concrete infrastructure implementations (HTTP client, caching layer) from domain logic.  
* **Fault Tolerance (Null Object Pattern):** Implements sentinel objects (InactiveCacheBackend) allowing the service to operate in a degraded mode if the Redis instance is unavailable (to implement).  
* **Asynchronous Cache Optimization:**  
  * Geocoding cache (/search) with a 7-day TTL.  
  * Forecast (/forecast) and current weather (/current) cache with a 15 to 30-minute TTL.  
  * **Strict Schema Validation:** Utilizes Pydantic v2 (BaseModel and RootModel) for thorough raw payload validation and clean DTO generation.  
  * **Persistent Connections:** Lifecycle management (lifespan) maintains asynchronous connection pools using httpx.AsyncClient and redis.asyncio.

## **Project Structure**

```bash
├── src/  
│   └── weather_api/  
│       ├── api/  
│       │   ├── dependencies.py          # Lifecycle (lifespan) and dependency injection  
│       │   └── v1/  
│       │       └── endpoints/  
│       │           ├── search.py        # Location resolution and search endpoints  
│       │           └── weather.py       # Current weather and forecast endpoints  
│       ├── core/  
│       │   ├── constants.py             # Global constants and configuration  
│       │   ├── endpoint_builders.py     # API URL construction functions  
│       │   └── protocols.py             # Interface contracts and Null Object implementation  
│       ├── schemas/  
│       │   ├── api_schemas.py           # Normalized DTOs and RootModels for public API  
│       │   └── raw_schemas.py           # External payload validation models  
│       ├── services/  
│       │   ├── cache.py                 # Adapter and resiliency layer over Redis  
│       │   ├── search.py                # Geocoding business logic  
│       │   └── weather.py               # Weather business logic  
│       └── main.py                      # FastAPI application entry point  
├── compose.yml                          # Infrastructure orchestration (Redis)  
├── pyproject.toml                       # Project metadata and dependencies  
└── uv.lock                              # Lockfile managed by uv
```

## **Prerequisites**

* Python 3.11 or higher  
* [uv](https://github.com/astral-sh/uv) (recommended Python package and venv manager)  
* Docker and Docker Compose  
* WeatherAPI API Key

## **Environment Setup**

1. Clone the repository:  

``` bash
git clone https://github.com/Christian-F-Badillo/simple_weather_api.git
cd simple_weather_api
```

2. Create and activate a virtual environment using uv:  

```bash
uv venv  
source .venv/bin/activate
```

3. Install project dependencies using uv:  

```bash
uv sync
```

4. Configure environment variables by creating a .env file in the project root:  

```txt
WEATHER_API_KEY=your_weatherapi_key  
REDIS_PASSWORD=your_secure_redis_password  
REDIS_HOST=localhost  
REDIS_PORT=6379
```

## **Running the Application**

### **1. Start the Cache Service (Redis)**

Launch the Redis container configured with authentication:  

```bash
docker compose up -d
```

### **2. Start the FastAPI Application**

Run the development server using Uvicorn:  

```bash
uv run uvicorn weather_api.main:app --reload --host 0.0.0.0 --port 8000
```

## **API Documentation**

Once the application is running, interactive OpenAPI documentation is available at:

* Swagger UI: http://127.0.0.1:8000/docs  
* ReDoc: http://127.0.0.1:8000/redoc

## **Key Endpoints**

### **Search & Geocoding**

* GET /api/v1/search?q={city}&lang={es|en}  
  * Returns an indexed map of geographic matches (SearchResultsMap) paired with coordinates and normalized names.

### **Current Weather**

* GET /api/v1/weather/current?q={city}&lang={es|en}  
  * Returns current weather conditions by location name.

* GET /api/v1/weather/current/coords?lat={latitude}&lon={longitude}&lang={es|en}  
  * Returns current weather by resolving exact geographical coordinates.

### **Forecast**

* GET /api/v1/weather/forecast?q={city}&days={1-3}&lang={es|en}  
  * Returns detailed weather forecast broken down by days and hours.  
* GET /api/v1/weather/forecast/coords?lat={latitude}&lon={longitude}&days={1-3}&lang={es|en}  
  * Returns weather forecast by exact geographical coordinates.

## **License**

This project is licensed under the MIT License.

## Proyect Idea

The project is based on the [roadmap.sh](https://roadmap.sh) project [WeatherAPI](https://roadmap.sh/projects/weather-api-wrapper-service).
