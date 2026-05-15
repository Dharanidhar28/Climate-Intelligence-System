🌍 Climate Intelligence System
A high-frequency data pipeline and analytics dashboard that monitors global weather patterns, predicts heatwaves, and visualizes climate trends.

🚀 Key Features
Real-time Data Pipeline: Automated ingestion from OpenWeather API every 30 minutes.

Time-Series Analytics: Historical tracking of temperature, humidity, and wind speed.

Heatwave Detection: Backend logic to analyze and alert on extreme temperature spikes.

Interactive Visualization: Dynamic graphs powered by Chart.js.

🛠️ Technical Stack
Backend: FastAPI (Python 3.12)

Database: PostgreSQL (Supabase) with SQLAlchemy ORM

Deployment: Dockerized for environment parity

Infrastructure: Hosted on Render with Connection Pooling (Supavisor)

🧠 Challenges Overcome (The "DevOps" Story)
Database Migration: Successfully migrated from local SQLite to cloud-based PostgreSQL while managing persistent data storage.

Cloud Networking: Resolved IPv6/IPv4 routing incompatibilities between Render and Supabase by implementing Session Pooling on port 6543.

Containerization: Fully Dockerized the application to ensure seamless deployment and scalability.

📦 How to Run (Local Docker)
Bash
docker build -t climate-app .
docker run -p 8000:10000 \
  -e DATABASE_URL="your_supabase_url" \
  -e OPENWEATHER_API_KEY="your_api_key" \
  climate-app
Access the API at http://localhost:8000/docs
