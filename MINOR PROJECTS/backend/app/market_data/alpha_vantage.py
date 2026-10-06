from __future__ import annotations

import math
import re
from datetime import datetime, timedelta
from typing import Any

import pandas as pd
import requests

from backend.app.config import settings

BASE_URL = 'https://www.alphavantage.co/query'


def validate_symbol(symbol: str) -> str:
    cleaned = symbol.strip().upper()
    if not re.fullmatch(r'[A-Z]{1,10}', cleaned):
        raise ValueError('Invalid stock symbol. Use a valid ticker like AAPL or MSFT.')
    return cleaned


def _generate_demo_price_series(symbol: str, days: int = 120) -> pd.DataFrame:
    start = datetime.today() - timedelta(days=days)
    prices = 100.0 + (hash(symbol) % 50)
    rows = []
    for idx in range(days):
        date = start + timedelta(days=idx)
        drift = idx / 10
        base = prices + drift * 1.5
        close = round(base + math.sin(idx / 3) * 8, 2)
        open_price = round(close - 2.5 + (idx % 4) * 0.7, 2)
        high = round(max(open_price, close) + 1.4, 2)
        low = round(min(open_price, close) - 1.4, 2)
        volume = int(1000000 + (idx * 4500) + (hash(symbol) % 100000))
        rows.append(
            {
                'date': date.strftime('%Y-%m-%d'),
                'open': open_price,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume,
            }
        )
    df = pd.DataFrame(rows)
    df['date'] = pd.to_datetime(df['date'])
    return df.set_index('date')


def fetch_stock_data(symbol: str) -> pd.DataFrame:
    symbol = validate_symbol(symbol)
    api_key = settings.alpha_vantage_api_key.strip()
    if not api_key:
        return _generate_demo_price_series(symbol)

    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'outputsize': 'compact',
        'apikey': api_key,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise RuntimeError(f'Market data request failed: {exc}') from exc

    if 'Error Message' in payload:
        raise ValueError(f'Invalid symbol or malformed request: {payload["Error Message"]}')
    if 'Note' in payload:
        raise RuntimeError('API rate limit reached. Please wait before retrying.')
    if 'Time Series (Daily)' not in payload:
        raise ValueError('Unexpected response from market-data API.')

    time_series = payload['Time Series (Daily)']
    rows = []
    for dt, values in time_series.items():
        rows.append(
            {
                'date': pd.to_datetime(dt),
                'open': float(values['1. open']),
                'high': float(values['2. high']),
                'low': float(values['3. low']),
                'close': float(values['4. close']),
                'volume': int(float(values['5. volume'])),
            }
        )
    df = pd.DataFrame(rows).sort_values('date').set_index('date')
    return df


def get_demo_dataframe(symbol: str) -> pd.DataFrame:
    return _generate_demo_price_series(symbol)
