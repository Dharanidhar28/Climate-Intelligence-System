from pydantic import BaseModel

class WeatherCreate(BaseModel):
    city: str
    temperature: float
    humidity: float
    wind_speed: float