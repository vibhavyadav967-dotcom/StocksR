from __future__ import annotations

from fastapi import FastAPI, HTTPException

from backend.app.config import settings
from backend.app.database.session import init_db
from backend.app.indicators.technical import calculate_indicators
from backend.app.market_data.alpha_vantage import fetch_stock_data
from backend.app.news.fetcher import fetch_news
from backend.app.recommendation.final_pipeline import compute_final_score
from backend.app.recommendation.rules import technical_score, classify_recommendation
from backend.app.sentiment.llm_service import analyze_sentiment

app = FastAPI(title=settings.app_name, version='1.0.0')


@app.on_event('startup')
def startup_event() -> None:
    init_db()


@app.get('/')
def root() -> dict:
    return {'message': 'AI Stock Recommendation project is running.'}


@app.get('/health')
def health() -> dict:
    return {'status': 'ok', 'project': settings.app_name}


@app.get('/api/stocks')
def get_stocks() -> dict:
    return {'symbols': [symbol.strip().upper() for symbol in settings.stock_symbols.split(',') if symbol.strip()]}


@app.get('/api/stocks/{symbol}')
def get_stock(symbol: str) -> dict:
    normalized = symbol.upper()
    df = fetch_stock_data(normalized)
    latest = df.iloc[-1]
    return {
        'symbol': normalized,
        'records': len(df),
        'latest_price': round(float(latest['close']), 2),
        'last_updated': df.index[-1].strftime('%Y-%m-%d'),
    }


@app.get('/api/stocks/{symbol}/news')
def get_news(symbol: str) -> dict:
    articles = fetch_news(symbol)
    return {'symbol': symbol.upper(), 'news': articles}


@app.get('/api/stocks/{symbol}/analysis')
def stock_analysis(symbol: str) -> dict:
    try:
        df = fetch_stock_data(symbol)
        enriched = calculate_indicators(df)
        latest = enriched.iloc[-1]
        technical_summary = {
            'sma_20': round(float(latest['sma_20']), 2),
            'sma_50': round(float(latest['sma_50']), 2),
            'rsi': round(float(latest['rsi_14']), 2),
            'macd': round(float(latest['macd']), 4),
            'macd_signal': round(float(latest['macd_signal']), 4),
            'volume_change': round(float(latest['volume_change']), 4),
        }

        technical_value = technical_score({
            'sma_20': float(latest['sma_20']),
            'sma_50': float(latest['sma_50']),
            'price': float(latest['close']),
            'rsi': float(latest['rsi_14']),
            'macd': float(latest['macd']),
            'macd_signal': float(latest['macd_signal']),
        })

        articles = fetch_news(symbol)
        sentiments = [analyze_sentiment(article['headline'], article['summary']) for article in articles]
        sentiment_scores = [item.score for item in sentiments]
        mean_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
        sentiment_score = round(max(-1.0, min(1.0, mean_sentiment)), 4)

        final = compute_final_score(float(technical_value), float(sentiment_score))
        reason = (
            'Positive technical momentum and healthy recent sentiment support a constructive outlook.'
            if final['recommendation'] == 'BUY'
            else 'Neutral conditions suggest waiting for stronger confirmation before taking a directional stance.'
            if final['recommendation'] == 'HOLD'
            else 'Weak technical and sentiment conditions justify avoiding the position at the moment.'
        )

        return {
            'symbol': symbol.upper(),
            'price': round(float(latest['close']), 2),
            'technical_score': technical_value,
            'sentiment_score': sentiment_score,
            'final_score': final['final_score'],
            'recommendation': final['recommendation'],
            'confidence': final['confidence'],
            'reason': reason,
            'technical_summary': technical_summary,
            'news': articles,
            'sentiment': [item.model_dump() for item in sentiments],
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get('/api/recommendations')
def recommendations() -> dict:
    symbols = [symbol.strip().upper() for symbol in settings.stock_symbols.split(',') if symbol.strip()]
    results = []
    for symbol in symbols:
        result = stock_analysis(symbol)
        results.append({
            'symbol': result['symbol'],
            'recommendation': result['recommendation'],
            'final_score': result['final_score'],
            'confidence': result['confidence'],
        })
    return {'results': results}


@app.get('/api/recommendations/{symbol}')
def recommendation_for_symbol(symbol: str) -> dict:
    return stock_analysis(symbol)


app.include_router(__import__('backend.app.api.routes.stocks', fromlist=['router']).router)
