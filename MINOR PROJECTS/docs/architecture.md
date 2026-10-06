# Architecture Overview

The application follows a layered design that keeps data collection, analysis, storage, and reporting separate.

## Layers

1. Data Collection
   - Market data from Alpha Vantage or demo mode
   - News data from financial feeds
2. Analysis Layer
   - Technical indicators with Pandas and NumPy
   - Sentiment analysis using LLM-style structured JSON
3. Decision Layer
   - Rule-based recommendation engine with transparent scoring
   - Final weighted score combining technical and sentiment signals
4. Storage Layer
   - PostgreSQL tables for stocks, prices, news, sentiment, technical indicators, recommendations, and logs
5. API Layer
   - FastAPI endpoints expose the analysis workflow to n8n and dashboards
6. Automation Layer
   - n8n schedules the workflow and sends alerts
7. Presentation Layer
   - Streamlit dashboard for interactive study and demonstration

## Why it works well for a project

This architecture is easy to explain during a viva because each step is clear: collect data, transform it, score it, store it, and automate it.
