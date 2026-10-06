from __future__ import annotations

from backend.app.indicators.technical import calculate_indicators
from backend.app.market_data.alpha_vantage import fetch_stock_data
from backend.app.news.fetcher import fetch_news
from backend.app.recommendation.final_pipeline import compute_final_score
from backend.app.recommendation.rules import technical_score
from backend.app.sentiment.llm_service import analyze_sentiment


def generate_demo_report(symbol: str = 'AAPL') -> dict:
    df = fetch_stock_data(symbol)
    enriched = calculate_indicators(df)
    latest = enriched.iloc[-1]

    tech_value = technical_score(
        {
            'sma_20': float(latest['sma_20']),
            'sma_50': float(latest['sma_50']),
            'price': float(latest['close']),
            'rsi': float(latest['rsi_14']),
            'macd': float(latest['macd']),
            'macd_signal': float(latest['macd_signal']),
        }
    )

    articles = fetch_news(symbol)
    sentiments = [analyze_sentiment(article['headline'], article['summary']) for article in articles]
    avg_sentiment = sum(item.score for item in sentiments) / max(len(sentiments), 1)
    combined = compute_final_score(float(tech_value), float(avg_sentiment))

    explanation = (
        'Positive technical momentum combined with positive recent news sentiment.'
        if combined['recommendation'] == 'BUY'
        else 'Neutral technical structure and balanced sentiment suggest a cautious hold.'
        if combined['recommendation'] == 'HOLD'
        else 'Weak technical momentum and deteriorating sentiment justify caution.'
    )

    return {
        'symbol': symbol.upper(),
        'price': round(float(latest['close']), 2),
        'technical_score': tech_value,
        'sentiment_score': round(avg_sentiment, 2),
        'final_score': round(combined['final_score'], 2),
        'recommendation': combined['recommendation'],
        'confidence': round(combined['confidence'], 2),
        'rsi': round(float(latest['rsi_14']), 2),
        'sma_20': round(float(latest['sma_20']), 2),
        'sma_50': round(float(latest['sma_50']), 2),
        'macd': round(float(latest['macd']), 4),
        'sentiment_summary': sentiments[0].model_dump() if sentiments else {'sentiment': 'neutral', 'score': 0.0, 'confidence': 0.5, 'reason': 'Demo sentiment summary'},
        'news_count': len(articles),
        'reason': explanation,
    }


if __name__ == '__main__':
    report = generate_demo_report()
    print('📊 AI STOCK MARKET REPORT')
    print(f"Symbol: {report['symbol']}")
    print(f"Recommendation: {report['recommendation']}")
    print(f"Confidence: {report['confidence'] * 100:.0f}%")
    print(f"Price: ${report['price']:.2f}")
    print(f"Technical Analysis: RSI {report['rsi']}, SMA20 ${report['sma_20']}, SMA50 ${report['sma_50']}, MACD {report['macd']}")
    print(f"News Sentiment: {report['sentiment_summary']['sentiment']} ({report['sentiment_summary']['score']:.2f})")
    print(f"Final Score: {report['final_score']:.2f}")
    print(f"Reason: {report['reason']}")
    print('Educational/research use only. Not financial advice.')
