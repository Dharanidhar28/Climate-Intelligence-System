from apscheduler.schedulers.background import BackgroundScheduler

import backend.crud as crud
import backend.schemas as schemas
from backend.database import SessionLocal
from backend.weather_service import fetch_weather


cities = [
    "delhi",
    "chennai",
    "mumbai",
    "kolkata",
    "bangalore",
    "hyderabad",
    "ahmedabad",
    "pune",
    "jaipur",
    "lucknow",
]


def collect_weather():
    db = SessionLocal()

    try:
        for city in cities:
            try:
                weather_data = fetch_weather(city)
                weather = schemas.WeatherCreate(**weather_data)
                crud.create_weather(db, weather)
                print(f"Weather collected for {city}")
            except Exception as e:
                print("Error:", e)
    finally:
        db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(collect_weather, "cron", hour="5-23", minute="0,30")
