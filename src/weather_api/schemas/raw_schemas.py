from pydantic import BaseModel, ConfigDict


class Condition(BaseModel):
    text: str
    icon: str
    code: int

    @property
    def icon_url(self) -> str:
        return f"https:{self.icon}" if self.icon.startswith("//") else self.icon


class LocationData(BaseModel):
    name: str
    region: str
    country: str
    lat: float
    lon: float
    tz_id: str
    localtime: str


class CurrentWeather(BaseModel):
    last_updated: str
    temp_c: float
    feelslike_c: float
    humidity: int
    precip_mm: float
    cloud: int
    is_day: int
    uv: float
    condition: Condition


class AstroData(BaseModel):
    sunrise: str
    sunset: str
    moon_phase: str
    moon_illumination: int


class DaySummary(BaseModel):
    maxtemp_c: float
    mintemp_c: float
    avgtemp_c: float
    totalprecip_mm: float
    daily_chance_of_rain: int
    condition: Condition
    uv: float


class HourlyForecast(BaseModel):
    time_epoch: int
    time: str
    temp_c: float
    feelslike_c: float
    humidity: int
    cloud: int
    precip_mm: float
    chance_of_rain: int
    will_it_rain: int
    condition: Condition


class ForecastDay(BaseModel):
    date: str
    date_epoch: int
    day: DaySummary
    astro: AstroData
    hour: list[HourlyForecast]


class Forecast(BaseModel):
    forecastday: list[ForecastDay]


class WeatherAPIResponse(BaseModel):
    location: LocationData
    current: CurrentWeather
    forecast: Forecast | None = None


class SearchLocationRaw(BaseModel):
    id: int
    name: str
    region: str
    country: str
    lat: float
    lon: float
    url: str

    model_config = ConfigDict(extra="ignore")
