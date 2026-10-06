from __future__ import annotations

import math

import pandas as pd

from backend.app.indicators.technical import calculate_indicators
from backend.app.market_data.alpha_vantage import fetch_stock_data
from backend.app.recommendation.rules import technical_score


def calculate_forward_return(prices: pd.Series, future_horizon: int = 5) -> float:
    if len(prices) <= future_horizon:
        return 0.0
    return float((prices.iloc[-1] / prices.iloc[-future_horizon]) - 1.0)


def run_backtest(symbol: str, lookback_days: int = 250) -> dict:
    df = fetch_stock_data(symbol)
    if len(df) > lookback_days:
        df = df.tail(lookback_days)
    enriched = calculate_indicators(df)
    enriched['signal'] = 'HOLD'

    for idx in range(20, len(enriched)):
        current = enriched.iloc[idx]
        tech = technical_score({
            'sma_20': float(current['sma_20']),
            'sma_50': float(current['sma_50']),
            'price': float(current['close']),
            'rsi': float(current['rsi_14']),
            'macd': float(current['macd']),
            'macd_signal': float(current['macd_signal']),
        })
        if tech >= 5:
            enriched.at[current.name, 'signal'] = 'BUY'
        elif tech <= 0:
            enriched.at[current.name, 'signal'] = 'AVOID'
        else:
            enriched.at[current.name, 'signal'] = 'HOLD'

    signal_returns = []
    signal_counts = {'BUY': 0, 'HOLD': 0, 'AVOID': 0}
    for idx in range(20, len(enriched) - 5):
        signal = enriched.iloc[idx]['signal']
        signal_counts[signal] += 1
        future_prices = enriched['close'].iloc[idx + 1: idx + 6]
        if not future_prices.empty:
            signal_returns.append((signal, calculate_forward_return(future_prices)))

    wins = sum(1 for _, ret in signal_returns if ret > 0)
    avg_return = sum(ret for _, ret in signal_returns) / len(signal_returns) if signal_returns else 0.0
    cumulative_return = math.prod([1 + ret for _, ret in signal_returns]) - 1 if signal_returns else 0.0

    drawdown_values = []
    running_peak = 0.0
    for _, ret in signal_returns:
        running_peak = max(running_peak, ret)
        drawdown_values.append((running_peak - ret) if ret < running_peak else 0.0)
    max_drawdown = max(drawdown_values) if drawdown_values else 0.0

    return {
        'symbol': symbol.upper(),
        'signals': len(signal_returns),
        'BUY signals': signal_counts['BUY'],
        'HOLD signals': signal_counts['HOLD'],
        'AVOID signals': signal_counts['AVOID'],
        'win_rate': round(wins / len(signal_returns), 4) if signal_returns else 0.0,
        'average_forward_return': round(avg_return, 4),
        'cumulative_return': round(cumulative_return, 4),
        'maximum_drawdown': round(max_drawdown, 4),
    }
