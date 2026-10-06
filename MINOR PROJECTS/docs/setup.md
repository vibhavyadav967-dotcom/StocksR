# Setup Guide

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git
- Optional API keys for Alpha Vantage, news feed, and LLM service

## Local development

1. python -m venv .venv
2. .venv\Scripts\Activate.ps1
3. pip install -r backend/requirements.txt
4. Copy .env.example to .env and fill in the required values.
5. Start the API: uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
6. Start the dashboard: streamlit run dashboard/streamlit_app.py

## Docker development

Run:

docker compose up -d

The app will start FastAPI, PostgreSQL, n8n, and Streamlit.
