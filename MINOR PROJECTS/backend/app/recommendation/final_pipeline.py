from __future__ import annotations

from backend.app.config import settings


def normalize_technical_score(score: float, min_value: float = -10.0, max_value: float = 10.0) -> float:
    if max_value == min_value:
        return 0.0
    value = (score - min_value) / (max_value - min_value)
    return max(0.0, min(1.0, value))


def compute_final_score(technical_score_value: float, sentiment_score: float) -> dict:
    tech_weight = settings.technical_weight
    sentiment_weight = settings.sentiment_weight
    technical_norm = normalize_technical_score(technical_score_value)
    final_score = (technical_norm * tech_weight) + (sentiment_score * sentiment_weight)

    if final_score >= settings.buy_threshold:
        recommendation = 'BUY'
    elif final_score >= settings.hold_threshold:
        recommendation = 'HOLD'
    else:
        recommendation = 'AVOID'

    confidence = round(min(0.95, 0.55 + abs(final_score - 0.5) + max(0.0, sentiment_score) * 0.2), 2)

    return {
        'technical_normalized': round(technical_norm, 4),
        'sentiment_score': round(sentiment_score, 4),
        'final_score': round(final_score, 4),
        'recommendation': recommendation,
        'confidence': confidence,
    }
