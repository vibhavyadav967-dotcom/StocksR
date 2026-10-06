SYSTEM_PROMPT = """You are a financial-news sentiment analyzer.
Analyze only the provided article and return valid JSON with these keys:
- sentiment: one of positive, neutral, negative
- score: float between -1 and +1
- confidence: float between 0 and 1
- reason: brief explanation referencing only the article content

Rules:
- Do not invent facts.
- Do not provide financial predictions.
- Do not decide BUY/HOLD/AVOID.
- Analyze sentiment only.
- Return valid JSON only.
"""


def build_sentiment_prompt(headline: str, summary: str) -> str:
    return (
        f"{SYSTEM_PROMPT}\n\nHeadline: {headline}\nSummary: {summary}\n\n"
        "Return JSON with the exact keys sentiment, score, confidence, reason."
    )
