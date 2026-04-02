import requests

import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def fetch_weather(city: str):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    data = response.json()

    # Debug: print API response
    print(data)

    # Check if API returned an error
    if response.status_code != 200:
        raise Exception(f"Weather API error: {data}")

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }