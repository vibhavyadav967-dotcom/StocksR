import pandas as pd
import numpy as np

from backend.app.indicators.technical import calculate_indicators, calculate_rsi, calculate_macd, calculate_sma
from backend.app.recommendation.rules import technical_score, classify_recommendation


def test_sma_calculation():
    df = pd.DataFrame({"close": [10, 20, 30, 40, 50, 60]})
    sma = calculate_sma(df["close"], 3)
    assert not sma.isna().all()
    assert round(float(sma.iloc[-1]), 2) == 50.0


def test_rsi_calculation():
    closes = pd.Series([10, 11, 12, 11, 13, 15, 14, 16, 18, 17])
    rsi = calculate_rsi(closes, 14)
    assert rsi.notna().any()
    assert 0 <= float(rsi.iloc[-1]) <= 100


def test_macd_calculation():
    closes = pd.Series([10, 12, 11, 13, 15, 17, 16, 18, 20, 22, 23])
    macd, signal = calculate_macd(closes)
    assert len(macd) == len(closes)
    assert len(signal) == len(closes)


def test_technical_score_rules():
    sample = {
        "sma_20": 110.0,
        "sma_50": 100.0,
        "price": 115.0,
        "rsi": 25.0,
        "macd": 1.5,
        "macd_signal": 0.8,
    }
    score = technical_score(sample)
    assert score > 0
    assert classify_recommendation(score) in {"BUY", "HOLD", "AVOID"}


def test_final_recommendation_thresholds():
    rec = classify_recommendation(6)
    assert rec == "BUY"
    rec2 = classify_recommendation(0)
    assert rec2 == "HOLD"
