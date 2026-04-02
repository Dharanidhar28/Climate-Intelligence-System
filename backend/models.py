from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.database import Base
import datetime


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)