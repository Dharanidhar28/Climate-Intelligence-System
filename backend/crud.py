from sqlalchemy.orm import Session
from models import WeatherData


def create_weather(db: Session, weather):
    db_weather = WeatherData(
        city=weather.city,
        temperature=weather.temperature,
        humidity=weather.humidity,
        wind_speed=weather.wind_speed
    )

    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)

    return db_weather