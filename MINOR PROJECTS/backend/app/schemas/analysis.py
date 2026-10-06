from typing import Any, Literal

from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=10)


class NewsArticle(BaseModel):
    headline: str
    summary: str
    source: str
    url: str
    published_at: str


class FinalRecommendation(BaseModel):
    symbol: str
    price: float
    technical_score: float
    sentiment_score: float
    final_score: float
    recommendation: Literal['BUY', 'HOLD', 'AVOID']
    confidence: float
    explanation: str | None = None


class StockAnalysisResult(BaseModel):
    symbol: str
    price: float
    technical_score: float
    sentiment_score: float
    final_score: float
    recommendation: str
    confidence: float
    reason: str
    news: list[NewsArticle] = []
    technical_summary: dict[str, Any] = {}
