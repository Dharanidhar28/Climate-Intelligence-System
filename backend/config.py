import os

DATABASE_URL = os.getenv("database_url", "postgresql://postgres:12345678@localhost/climate_db")