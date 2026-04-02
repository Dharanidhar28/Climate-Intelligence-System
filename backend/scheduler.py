from apscheduler.schedulers.background import BackgroundScheduler
from backend.weather_service import fetch_weather
from backend.database import SessionLocal
import backend.crud
import backend.schemas


cities = ["delhi", "chennai", "mumbai","kolkata", "bangalore", "hyderabad", "ahmedabad", "pune", "jaipur", "lucknow"]


def collect_weather():

    db = SessionLocal()

    for city in cities:

        try:
            weather_data = fetch_weather(city)

            weather = schemas.WeatherCreate(**weather_data)

            crud.create_weather(db, weather)

            print(f"Weather collected for {city}")

        except Exception as e:
            print("Error:", e)

    db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(collect_weather, "interval", minutes=30)