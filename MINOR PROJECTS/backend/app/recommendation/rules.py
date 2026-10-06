from __future__ import annotations


def technical_score(indicators: dict) -> int:
    score = 0
    sma_20 = float(indicators.get('sma_20', 0))
    sma_50 = float(indicators.get('sma_50', 0))
    price = float(indicators.get('price', 0))
    rsi = float(indicators.get('rsi', 50))
    macd = float(indicators.get('macd', 0))
    macd_signal = float(indicators.get('macd_signal', 0))

    if sma_20 > sma_50:
        score += 2
    if price > sma_20:
        score += 1
    if rsi < 30:
        score += 2
    elif 40 <= rsi <= 60:
        score += 1
    if macd > macd_signal:
        score += 2
    else:
        score -= 2
    if price < sma_50:
        score -= 2

    return int(score)


def classify_recommendation(score: int) -> str:
    if score >= 5:
        return 'BUY'
    if score >= 0:
        return 'HOLD'
    return 'AVOID'
