from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
import schemas
import crud

from database import engine, get_db
from weather_service import fetch_weather
from analytics_service import analyze_city_weather
from analytics_service import detect_heatwave
from fastapi.middleware.cors import CORSMiddleware
from analytics_service import get_weather_history
from scheduler import scheduler

app = FastAPI()

scheduler.start()

origins = [
    "http://127.0.0.1",
    "http://localhost",
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Climate Intelligence System API"}


@app.post("/weather")
def add_weather(weather: schemas.WeatherCreate, db: Session = Depends(get_db)):
    return crud.create_weather(db, weather)

@app.post("/weather/fetch/{city}")
def fetch_and_store_weather(city: str, db: Session = Depends(get_db)):

    weather_data = fetch_weather(city)

    weather = schemas.WeatherCreate(**weather_data)

    return crud.create_weather(db, weather)

@app.get("/analytics/{city}")
def get_city_analytics(city: str, db: Session = Depends(get_db)):
    return analyze_city_weather(db, city)

@app.get("/heatwave/{city}")
def heatwave_alert(city: str, db: Session = Depends(get_db)):
    return detect_heatwave(db, city)

@app.get("/history/{city}")
def weather_history(city: str, db: Session = Depends(get_db)):
    return get_weather_history(db, city)