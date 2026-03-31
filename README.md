# Climate Intelligence System

A full-stack climate analytics platform that collects weather data, stores it in PostgreSQL, analyzes climate patterns, and visualizes results using a live dashboard.

## Features

- Weather data collection using OpenWeather API
- Automated data pipeline with APScheduler
- PostgreSQL database storage
- Climate analytics using Pandas
- Heatwave detection logic
- Live dashboard with Chart.js

## Tech Stack

Backend:
- FastAPI
- PostgreSQL
- SQLAlchemy

Data Analysis:
- Pandas
- NumPy

Frontend:
- HTML
- JavaScript
- Chart.js

## Architecture

Weather API → FastAPI → PostgreSQL → Pandas Analytics → Dashboard
