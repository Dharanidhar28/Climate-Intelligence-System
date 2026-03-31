import pandas as pd
from sqlalchemy.orm import Session
from models import WeatherData


def analyze_city_weather(db: Session, city: str):

    weather_records = db.query(WeatherData).filter(
        WeatherData.city == city
    ).all()

    if not weather_records:
        return {"message": "No weather data found"}

    data = []

    for record in weather_records:
        data.append({
            "temperature": record.temperature,
            "humidity": record.humidity,
            "wind_speed": record.wind_speed
        })

    df = pd.DataFrame(data)

    return {
        "city": city,
        "avg_temperature": float(df["temperature"].mean()),
        "max_temperature": float(df["temperature"].max()),
        "min_temperature": float(df["temperature"].min()),
        "avg_humidity": float(df["humidity"].mean())
    }

def detect_heatwave(db: Session, city: str):

    records = db.query(WeatherData).filter(
        WeatherData.city == city
    ).all()

    if not records:
        return {"message": "No weather data found"}

    temps = [r.temperature for r in records]

    df = pd.DataFrame({"temperature": temps})

    # heatwave rule
    heatwave = (df["temperature"] >= 38).rolling(3).sum().max() >= 3

    return {
        "city": city,
        "heatwave": bool(heatwave)
    }

import pandas as pd
from sqlalchemy.orm import Session
from models import WeatherData


def get_weather_history(db: Session, city: str):

    records = db.query(WeatherData).filter(
        WeatherData.city == city
    ).all()

    if not records:
        return {"message": "No data found"}

    data = []

    for r in records:
        data.append({
            "temperature": r.temperature,
            "humidity": r.humidity,
            "wind_speed": r.wind_speed,
            "time": str(r.created_at)
        })

    return data