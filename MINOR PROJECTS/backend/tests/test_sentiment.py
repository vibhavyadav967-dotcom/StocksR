from backend.app.sentiment.models import SentimentResult


def test_sentiment_validation():
    payload = {
        "sentiment": "positive",
        "score": 0.72,
        "confidence": 0.88,
        "reason": "Strong company momentum and positive earnings expectations."
    }
    result = SentimentResult(**payload)
    assert result.sentiment == "positive"
    assert -1 <= result.score <= 1
    assert 0 <= result.confidence <= 1
