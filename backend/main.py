import os

from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles

import backend.models
import backend.schemas
import backend.crud

from backend.database import engine, get_db
from backend.weather_service import fetch_weather
from backend.analytics_service import analyze_city_weather
from backend.analytics_service import detect_heatwave
from fastapi.middleware.cors import CORSMiddleware
from backend.analytics_service import get_weather_history
from backend.scheduler import scheduler

app = FastAPI()


scheduler.start()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


backend.models.Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/api")
def root():
    return {"message": "Climate Intelligence System API"}


@app.post("/weather")
def add_weather(weather: backend.schemas.WeatherCreate, db: Session = Depends(get_db)):
    return backend.crud.create_weather(db, weather)

@app.post("/weather/fetch/{city}")
def fetch_and_store_weather(city: str, db: Session = Depends(get_db)):

    weather_data = fetch_weather(city)

    weather = backend.schemas.WeatherCreate(**weather_data)

    return backend.crud.create_weather(db, weather)

@app.get("/analytics/{city}")
def get_city_analytics(city: str, db: Session = Depends(get_db)):
    return backend.analytics_service.analyze_city_weather(db, city)

@app.get("/heatwave/{city}")
def heatwave_alert(city: str, db: Session = Depends(get_db)):
    return backend.analytics_service.detect_heatwave(db, city)

@app.get("/history/{city}")
def weather_history(city: str, db: Session = Depends(get_db)):
    return backend.analytics_service.get_weather_history(db, city)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
