from typing import Literal

from pydantic import BaseModel, Field


class SentimentResult(BaseModel):
    sentiment: Literal['positive', 'neutral', 'negative']
    score: float = Field(..., ge=-1.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str
