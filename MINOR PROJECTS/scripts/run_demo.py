from backend.app.market_data.alpha_vantage import fetch_stock_data
from backend.app.indicators.technical import calculate_indicators
from backend.app.news.fetcher import fetch_news
from backend.app.sentiment.llm_service import analyze_sentiment
from backend.app.recommendation.rules import technical_score
from backend.app.recommendation.final_pipeline import compute_final_score


symbol = 'AAPL'
df = fetch_stock_data(symbol)
tech_df = calculate_indicators(df)
latest = tech_df.iloc[-1]
score = technical_score({
    'sma_20': float(latest['sma_20']),
    'sma_50': float(latest['sma_50']),
    'price': float(latest['close']),
    'rsi': float(latest['rsi_14']),
    'macd': float(latest['macd']),
    'macd_signal': float(latest['macd_signal']),
})
articles = fetch_news(symbol)
mean_sentiment = sum(analyze_sentiment(article['headline'], article['summary']).score for article in articles) / max(1, len(articles))
final = compute_final_score(float(score), float(mean_sentiment))
print({
    'symbol': symbol,
    'price': round(float(latest['close']), 2),
    'technical_score': score,
    'sentiment_score': round(mean_sentiment, 4),
    'final_score': final['final_score'],
    'recommendation': final['recommendation'],
    'confidence': final['confidence'],
})
