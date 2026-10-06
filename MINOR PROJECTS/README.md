# AI-Powered Stock Market Recommendation Workflow Automation Using Python and n8n

This project demonstrates a complete university-level workflow for stock-market analysis and automation. It fetches market data, calculates technical indicators, collects recent financial news, analyzes sentiment with an LLM-style service, builds a deterministic recommendation, stores results in PostgreSQL, exposes an API through FastAPI, automates execution with n8n, and sends results to Telegram and email.

## Project Goal

The system is designed for educational and research use only. It should not be treated as a guaranteed stock-prediction system or as financial advice.

## Main Features

- Market-data retrieval from Alpha Vantage or a demo mode
- Technical indicators: SMA 20, SMA 50, RSI 14, MACD, daily return, volume change, price trend
- Deterministic rule-based recommendation engine
- Financial-news collection and deduplication
- Sentiment analysis using a structured LLM output model
- Final combined score using 60% technical + 40% sentiment weighting
- PostgreSQL storage with historical recommendation tables
- FastAPI backend with analysis endpoints
- n8n workflow automation
- Telegram and HTML email reports
- Streamlit dashboard
- Backtesting module and pytest tests
- Docker Compose support

## Architecture

Market API -> Python backend -> Technical indicators -> News API -> Sentiment analysis -> Recommendation -> PostgreSQL -> FastAPI -> n8n -> Telegram/Email -> Streamlit dashboard

## Technologies

- Python 3.11+
- FastAPI
- Pandas, NumPy
- PostgreSQL
- SQLAlchemy
- n8n
- Streamlit
- pytest
- Docker / Docker Compose

## Local Setup

1. Create a virtual environment:
   python -m venv .venv
   .venv\Scripts\Activate.ps1
2. Install dependencies:
   pip install -r backend/requirements.txt
3. Copy .env.example to .env and set your credentials.
4. Start the FastAPI app:
   uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
5. Open the dashboard:
   streamlit run dashboard/streamlit_app.py

## Environment Variables

Key variables include:
- ALPHA_VANTAGE_API_KEY
- NEWS_API_KEY
- LLM_API_KEY
- LLM_BASE_URL
- DATABASE_URL
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID
- SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASSWORD
- ALERT_EMAIL

## Database Setup

The app uses PostgreSQL by default in Docker, while SQLite is accepted for local quick testing if DATABASE_URL is set to sqlite://.

## FastAPI Endpoints

- GET /
- GET /health
- GET /api/stocks
- GET /api/stocks/{symbol}
- GET /api/stocks/{symbol}/analysis
- GET /api/stocks/{symbol}/news
- GET /api/recommendations
- GET /api/recommendations/{symbol}

## n8n Workflow

Import the JSON workflow from n8n/workflows/stock_analysis_workflow.json.
Set the schedule to every 1 hour or switch to 5 minutes for testing.

## Telegram and Email

The workflow can send a compact Telegram message and a richer HTML email report when credentials are configured.

## Backtesting

The project includes a simple backtesting module to evaluate recommendation decisions using historical data and forward-return metrics, without using data that would not have been available at recommendation time.

## Docker

Run:

docker compose up -d

This starts PostgreSQL, FastAPI, n8n, and Streamlit.

## Testing

Run:

pytest backend/tests -q

## Disclaimer

Educational and research use only. This project is not financial advice and should not be used as a live trading recommendation system.
