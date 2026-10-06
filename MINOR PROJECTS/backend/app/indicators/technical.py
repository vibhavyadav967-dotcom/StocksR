from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_sma(series: pd.Series, window: int = 20) -> pd.Series:
    return series.rolling(window=window, min_periods=window).mean()


def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50.0)


def calculate_macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    fast_ema = series.ewm(span=fast, adjust=False).mean()
    slow_ema = series.ewm(span=slow, adjust=False).mean()
    macd = fast_ema - slow_ema
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    return macd, macd_signal


def calculate_daily_percentage_change(series: pd.Series) -> pd.Series:
    return series.pct_change().fillna(0.0)


def calculate_volume_change(series: pd.Series) -> pd.Series:
    return series.pct_change().fillna(0.0)


def calculate_price_trend(series: pd.Series) -> pd.Series:
    return series / series.shift(1) - 1


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    if 'close' not in data.columns:
        raise ValueError('Input DataFrame must contain a close column.')

    data['sma_20'] = calculate_sma(data['close'], 20)
    data['sma_50'] = calculate_sma(data['close'], 50)
    data['rsi_14'] = calculate_rsi(data['close'], 14)
    data['macd'], data['macd_signal'] = calculate_macd(data['close'])
    data['daily_return'] = calculate_daily_percentage_change(data['close'])
    data['volume_change'] = calculate_volume_change(data['volume'])
    data['price_trend'] = calculate_price_trend(data['close'])
    return data
