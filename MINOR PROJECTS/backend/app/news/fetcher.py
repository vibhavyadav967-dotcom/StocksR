from __future__ import annotations

from datetime import datetime
from typing import Any

import requests

from backend.app.config import settings


def _demo_news(symbol: str) -> list[dict[str, str]]:
    return [
        {
            'headline': f'{symbol} shows strong technical momentum in latest trading session',
            'summary': 'Analysts note improved price action and healthy volume trends supporting a constructive market view.',
            'source': 'Market Pulse',
            'url': f'https://example.com/news/{symbol.lower()}/1',
            'published_at': datetime.utcnow().isoformat(),
        },
        {
            'headline': f'{symbol} remains under watch as investors assess near-term risks',
            'summary': 'Mixed sentiment and steady trading suggest a cautious but not negative outlook.',
            'source': 'Financial Briefing',
            'url': f'https://example.com/news/{symbol.lower()}/2',
            'published_at': datetime.utcnow().isoformat(),
        },
    ]


def fetch_news(symbol: str) -> list[dict[str, str]]:
    symbol = symbol.upper()
    if not settings.news_api_key:
        return _demo_news(symbol)

    url = 'https://www.alphavantage.co/query'
    params = {'function': 'NEWS_SENTIMENT', 'tickers': symbol, 'apikey': settings.news_api_key, 'limit': 10}
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()
    except Exception:
        return _demo_news(symbol)

    feed = payload.get('feed', [])
    articles: list[dict[str, str]] = []
    seen = set()
    for item in feed:
        headline = item.get('headline', '').strip()
        summary = item.get('summary', '').strip()
        url_value = item.get('url', '').strip()
        if not headline and not summary:
            continue
        key = (headline or summary, url_value)
        if key in seen:
            continue
        seen.add(key)
        articles.append(
            {
                'headline': headline,
                'summary': summary,
                'source': item.get('source', 'Unknown'),
                'url': url_value,
                'published_at': item.get('time_published', datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')),
            }
        )
    return articles[:5]
