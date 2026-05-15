from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.database import Base
from datetime import datetime, timezone

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    
    # Keeps city lookups fast
    city = Column(String, index=True)
    
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    
    # Added index=True here because your charts will query by time constantly
    # Using a lambda ensures the time is captured at the moment of insertion
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        index=True
    )