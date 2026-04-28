from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.models import WeatherData
from backend.weather_service import fetch_weather


def analyze_city_weather(db: Session, city: str):
    weather_records = db.query(WeatherData).filter(
        func.lower(WeatherData.city) == city.lower()
    ).all()

    if not weather_records:
        return {"message": "No weather data found"}

    data = []

    for record in weather_records:
        data.append(
            {
                "temperature": record.temperature,
                "humidity": record.humidity,
                "wind_speed": record.wind_speed,
            }
        )

    df = pd.DataFrame(data)

    return {
        "city": city,
        "avg_temperature": float(df["temperature"].mean()),
        "max_temperature": float(df["temperature"].max()),
        "min_temperature": float(df["temperature"].min()),
        "avg_humidity": float(df["humidity"].mean()),
    }


def detect_heatwave(db: Session, city: str):
    records = db.query(WeatherData).filter(
        func.lower(WeatherData.city) == city.lower()
    ).all()

    if not records:
        return {"message": "No weather data found"}

    temps = [r.temperature for r in records]
    df = pd.DataFrame({"temperature": temps})

    heatwave = (df["temperature"] >= 38).rolling(3).sum().max() >= 3

    return {
        "city": city,
        "heatwave": bool(heatwave),
    }


def _local_time(timestamp: datetime, timezone_offset: int):
    return timestamp + timedelta(seconds=timezone_offset)


def _get_today_window(timezone_offset: int):
    local_now = datetime.utcnow() + timedelta(seconds=timezone_offset)
    local_start = local_now.replace(hour=5, minute=0, second=0, microsecond=0)
    return local_start, local_now


def _history_item(record: WeatherData, timezone_offset: int):
    return {
        "temperature": record.temperature,
        "humidity": record.humidity,
        "wind_speed": record.wind_speed,
        "time": record.created_at.isoformat() if record.created_at else None,
        "local_time": _local_time(record.created_at, timezone_offset).isoformat()
        if record.created_at
        else None,
    }


def _build_safety_measures(current_weather, summary, heatwave):
    measures = []

    if current_weather["temperature"] >= 38 or heatwave:
        measures.append("Avoid direct sun exposure for long periods and keep drinking water nearby.")
        measures.append("Limit strenuous outdoor activity during the hottest part of the day.")
    elif current_weather["temperature"] >= 32:
        measures.append("Wear light clothing and take shade breaks if you are outdoors.")
    else:
        measures.append("Current temperature is moderate, but continue checking updates if you plan to stay outside.")

    if current_weather["humidity"] >= 80:
        measures.append("High humidity may increase discomfort. Plan extra hydration and ventilation.")

    if current_weather["wind_speed"] >= 10:
        measures.append("Strong winds are present. Secure loose objects and ride carefully if travelling.")

    if summary["temperature_trend"] == "rising":
        measures.append("Conditions are warming up since 5 AM, so earlier outdoor plans are safer than later ones.")
    elif summary["temperature_trend"] == "falling":
        measures.append("Conditions are easing compared with earlier today, which may improve outdoor comfort.")

    return measures


def _build_analysis(city, current_weather, summary, heatwave):
    heatwave_text = "Heatwave risk is active." if heatwave else "No heatwave pattern is currently detected."

    return (
        f"{city.title()} is currently experiencing {current_weather['description']} conditions with "
        f"{current_weather['temperature']:.1f}°C temperature, {current_weather['humidity']:.0f}% humidity, "
        f"and {current_weather['wind_speed']:.1f} m/s wind. Since 5 AM, the temperature has ranged from "
        f"{summary['min_temperature']:.1f}°C to {summary['max_temperature']:.1f}°C and is trending "
        f"{summary['temperature_trend']}. {heatwave_text}"
    )


def get_weather_history(db: Session, city: str):
    city = city.lower()

    weather = fetch_weather(city)
    timezone_offset = int(weather.get("timezone_offset", 0))

    new_record = WeatherData(
        city=city,
        temperature=weather["temperature"],
        humidity=weather["humidity"],
        wind_speed=weather["wind_speed"],
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    window_start, local_now = _get_today_window(timezone_offset)

    records = (
        db.query(WeatherData)
        .filter(func.lower(WeatherData.city) == city)
        .order_by(WeatherData.created_at.asc())
        .all()
    )

    filtered_records = [
        record
        for record in records
        if record.created_at and window_start <= _local_time(record.created_at, timezone_offset) <= local_now
    ]

    history_source = filtered_records or [new_record]
    history = [_history_item(record, timezone_offset) for record in history_source]

    df = pd.DataFrame(
        [
            {
                "temperature": record.temperature,
                "humidity": record.humidity,
                "wind_speed": record.wind_speed,
            }
            for record in history_source
        ]
    )

    first_temp = history_source[0].temperature
    last_temp = history_source[-1].temperature
    temperature_delta = last_temp - first_temp

    if temperature_delta > 1:
        trend = "rising"
    elif temperature_delta < -1:
        trend = "falling"
    else:
        trend = "stable"

    heatwave = bool((df["temperature"] >= 38).rolling(3).sum().max() >= 3)

    summary = {
        "avg_temperature": float(df["temperature"].mean()),
        "max_temperature": float(df["temperature"].max()),
        "min_temperature": float(df["temperature"].min()),
        "avg_humidity": float(df["humidity"].mean()),
        "avg_wind_speed": float(df["wind_speed"].mean()),
        "temperature_trend": trend,
        "records_count": len(history_source),
    }

    current_weather = {
        "temperature": weather["temperature"],
        "feels_like": weather["feels_like"],
        "humidity": weather["humidity"],
        "pressure": weather["pressure"],
        "wind_speed": weather["wind_speed"],
        "condition": weather["condition"],
        "description": weather["description"],
        "timezone_offset": timezone_offset,
    }

    return {
        "city": city.title(),
        "current_weather": current_weather,
        "history": history,
        "summary": summary,
        "heatwave": heatwave,
        "time_window": {
            "start_local": window_start.isoformat(),
            "end_local": local_now.isoformat(),
            "label": "5 AM to present time",
        },
        "analysis": _build_analysis(city, current_weather, summary, heatwave),
        "safety_measures": _build_safety_measures(current_weather, summary, heatwave),
    }
