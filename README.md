# Stock AI Alerts

A full-stack project that combines **FastAPI**, **React**, and **AI** to analyze stock data, detect extreme events, and send automated alerts.

***

## Overview

Stock AI Alerts automatically:
- Fetches real-time stock data from **Finnhub**.
- Calculates technical indicators like **SMA** and **RSI**.
- Detects extreme events (for example, sudden price drops or spikes).
- Summarizes recent market news using **OpenAI**.
- Sends daily email alerts about relevant stocks.
- Runs everything via **Docker Compose**.

***

## Architecture

- frontend/ → React UI (search, watchlist, results)
- backend/ → FastAPI API (technical + AI analysis)
- alert_service/ → Python scheduler for daily email alerts
- docker-compose.yml → Runs all services together

***

##  Tech Stack

| Area          | Tools                                 |
|---------------|---------------------------------------|
| Backend       | FastAPI, Python 3.11, Pandas, SQLite  |
| AI            | OpenAI API                            |
| Market Data   | Finnhub API, yfinance                 |
| Frontend      | React (JS)                            |
| Email & Scheduler | yagmail, schedule                 |
| DevOps        | Docker, Docker Compose                |

***

##  How to Run (Docker)

```bash
git clone https://github.com/<YOUR_USERNAME>/stock-ai-alerts.git
cd stock-ai-alerts

# Create env files
cp backend/.env.example backend/.env
cp alert_service/.env.example alert_service/.env

# Build & run everything
docker compose up --build
```

Then open:  
Backend Docs: [http://localhost:8000/docs](http://localhost:8000/docs)  
Frontend App: [http://localhost:3000](http://localhost:3000)

***

## Environment Variables

**backend/.env.example**
```
FINNHUB_API_KEY=YOUR_FINNHUB_KEY
OPENAI_API_KEY=YOUR_OPENAI_KEY
```

**alert_service/.env.example**
```
SENDER_EMAIL=example@gmail.com
APP_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@example.com
BACKEND_INFER_URL=http://backend:8000/infer
ALERT_TIME=09:00
```

***

## Features

- SMA and RSI calculations
- Extreme price event detection
- AI-based financial news summary
- Daily alert emails
- Dockerized multi-service setup
- SQLite persistence

***

## Example Workflow

- Add stocks to your watchlist via the React UI.
- The backend analyzes their technical and AI data.
- The alert service runs every morning and emails alerts.

***

## Skills Demonstrated

- REST API design (FastAPI)
- AI integration into backend pipelines
- Docker Compose orchestration
- Automation with Python (schedule, yagmail)
- Frontend API integration (React)
- Clean data handling with Pandas and SQLite

***

## Contact

Author: Daniel Wiesel  
LinkedIn: [www.linkedin.com/in/daniel-wiesel-767a611a7]
Email: daniel62127@gmail.com

***
