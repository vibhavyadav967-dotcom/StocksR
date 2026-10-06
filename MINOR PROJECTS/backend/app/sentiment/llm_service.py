from __future__ import annotations

import json
import re

import requests

from backend.app.config import settings
from backend.app.sentiment.models import SentimentResult
from backend.app.sentiment.prompts import build_sentiment_prompt


def _heuristic_sentiment(text: str) -> SentimentResult:
    lowered = text.lower()
    positive_terms = ['growth', 'beat', 'strong', 'upbeat', 'rally', 'profit', 'optimistic', 'expansion', 'surge']
    negative_terms = ['drop', 'loss', 'fall', 'weak', 'risk', 'downgrade', 'decline', 'concern', 'pressure']
    positive_count = sum(1 for term in positive_terms if term in lowered)
    negative_count = sum(1 for term in negative_terms if term in lowered)

    if positive_count > negative_count:
        sentiment = 'positive'
        score = min(0.95, 0.35 + (positive_count - negative_count) * 0.12)
    elif negative_count > positive_count:
        sentiment = 'negative'
        score = max(-0.95, -0.35 - (negative_count - positive_count) * 0.12)
    else:
        sentiment = 'neutral'
        score = 0.0

    confidence = min(0.95, 0.45 + (max(positive_count, negative_count) * 0.10))
    reason = 'The article wording suggests a generally balanced market tone without clear directional conviction.' if sentiment == 'neutral' else (
        'Positive language in the article indicates a constructive outlook.' if sentiment == 'positive' else 'Negative wording in the article indicates a cautious outlook.'
    )

    return SentimentResult(sentiment=sentiment, score=round(score, 2), confidence=round(confidence, 2), reason=reason)


def analyze_sentiment(headline: str, summary: str) -> SentimentResult:
    text = f'{headline} {summary}'.strip()
    if not settings.llm_api_key and not settings.llm_base_url:
        return _heuristic_sentiment(text)

    payload = {
        'model': 'gpt-4o-mini',
        'messages': [
            {'role': 'system', 'content': 'You are a financial news sentiment analyzer.'},
            {'role': 'user', 'content': build_sentiment_prompt(headline, summary)},
        ],
        'temperature': 0.1,
        'response_format': {'type': 'json_object'},
    }

    headers = {'Authorization': f'Bearer {settings.llm_api_key}', 'Content-Type': 'application/json'}
    try:
        response = requests.post(settings.llm_base_url or 'https://api.openai.com/v1/chat/completions', json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        content = data['choices'][0]['message']['content']
        clean = re.sub(r'^```json\s*|```\s*$', '', content, flags=re.IGNORECASE).strip()
        parsed = json.loads(clean)
        return SentimentResult(**parsed)
    except Exception:
        return _heuristic_sentiment(text)
