from pydantic import BaseModel, ConfigDict, Field, RootModel

from .raw_schemas import (
    CurrentWeather,
    ForecastDay,
    HourlyForecast,
    LocationData,
    WeatherAPIResponse,
)


class LocationDTO(BaseModel):
    city: str
    region: str
    country: str
    lat: float
    lon: float
    timezone: str
    local_time: str

    @classmethod
    def from_raw(cls, raw: LocationData) -> "LocationDTO":
        return cls(
            city=raw.name,
            region=raw.region,
            country=raw.country,
            lat=raw.lat,
            lon=raw.lon,
            timezone=raw.tz_id,
            local_time=raw.localtime,
        )


class CurrentWeatherDTO(BaseModel):
    last_updated: str
    temperature_c: float
    feels_like_c: float
    humidity: int
    precip_mm: float
    cloud_cover: int
    uv_index: float
    condition: str
    icon_url: str
    is_day: bool

    @classmethod
    def from_raw(cls, raw: CurrentWeather) -> "CurrentWeatherDTO":
        return cls(
            last_updated=raw.last_updated,
            temperature_c=raw.temp_c,
            feels_like_c=raw.feelslike_c,
            humidity=raw.humidity,
            precip_mm=raw.precip_mm,
            cloud_cover=raw.cloud,
            uv_index=raw.uv,
            condition=raw.condition.text,
            icon_url=raw.condition.icon_url,
            is_day=bool(raw.is_day),
        )


class HourlyPointDTO(BaseModel):
    time: str
    temperature_c: float
    feels_like_c: float
    rain_probability: int
    precip_mm: float
    humidity: int
    condition: str
    icon_url: str

    @classmethod
    def from_raw(cls, raw: HourlyForecast) -> "HourlyPointDTO":
        return cls(
            time=raw.time.split(" ")[-1],
            temperature_c=raw.temp_c,
            feels_like_c=raw.feelslike_c,
            rain_probability=raw.chance_of_rain,
            precip_mm=raw.precip_mm,
            humidity=raw.humidity,
            condition=raw.condition.text,
            icon_url=raw.condition.icon_url,
        )


class DayForecastDTO(BaseModel):
    date: str
    max_temp_c: float
    min_temp_c: float
    avg_temp_c: float
    rain_chance: int
    total_precip_mm: float
    uv_index: float
    condition: str
    icon_url: str
    sunrise: str
    sunset: str
    hours: list[HourlyPointDTO]

    @classmethod
    def from_raw(cls, raw: ForecastDay) -> "DayForecastDTO":
        return cls(
            date=raw.date,
            max_temp_c=raw.day.maxtemp_c,
            min_temp_c=raw.day.mintemp_c,
            avg_temp_c=raw.day.avgtemp_c,
            rain_chance=raw.day.daily_chance_of_rain,
            total_precip_mm=raw.day.totalprecip_mm,
            uv_index=raw.day.uv,
            condition=raw.day.condition.text,
            icon_url=raw.day.condition.icon_url,
            sunrise=raw.astro.sunrise,
            sunset=raw.astro.sunset,
            hours=[HourlyPointDTO.from_raw(h) for h in raw.hour],
        )


class CurrentWeatherReport(BaseModel):
    location: LocationDTO
    current: CurrentWeatherDTO

    @classmethod
    def from_raw(cls, raw: WeatherAPIResponse) -> "CurrentWeatherReport":
        return cls(
            location=LocationDTO.from_raw(raw.location),
            current=CurrentWeatherDTO.from_raw(raw.current),
        )


class ForecastWeatherReport(BaseModel):
    location: LocationDTO
    current: CurrentWeatherDTO
    forecast_days: list[DayForecastDTO] = Field(default_factory=list)

    @classmethod
    def from_raw(cls, raw: WeatherAPIResponse) -> "ForecastWeatherReport":
        days = []
        if raw.forecast:
            days = [DayForecastDTO.from_raw(fday) for fday in raw.forecast.forecastday]

        return cls(
            location=LocationDTO.from_raw(raw.location),
            current=CurrentWeatherDTO.from_raw(raw.current),
            forecast_days=days,
        )


class LocationMatchDTO(BaseModel):
    id: int = Field(description="ID original de WeatherAPI")
    city: str
    region: str
    country: str
    lat: float
    lon: float
    formatted_name: str

    model_config = ConfigDict(extra="ignore")


class SearchResultsMap(RootModel[dict[int, LocationMatchDTO]]):
    @classmethod
    def from_raw_list(cls, raw_list: list[dict]) -> "SearchResultsMap":
        results: dict[int, LocationMatchDTO] = {}

        for idx, item in enumerate(raw_list, start=1):
            parts = [item["name"]]
            if item.get("region") and item["region"].lower() != item["name"].lower():
                parts.append(item["region"])
            if item.get("country"):
                parts.append(item["country"])

            results[idx] = LocationMatchDTO(
                id=item["id"],
                city=item["name"],
                region=item["region"],
                country=item["country"],
                lat=item["lat"],
                lon=item["lon"],
                formatted_name=", ".join(parts),
            )

        return cls(root=results)

    def __getitem__(self, key: int) -> LocationMatchDTO:
        return self.root[key]

    def items(self):
        return self.root.items()

    def values(self):
        return self.root.values()

    def keys(self):
        return self.root.keys()
