from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=False,
    )

    app_name: str = 'AI Stock Recommendation Workflow'
    environment: str = 'development'
    alpha_vantage_api_key: str = ''
    news_api_key: str = ''
    llm_api_key: str = ''
    llm_base_url: str = ''
    database_url: str = 'sqlite:///./stock_recommendation.db'
    postgres_db: str = 'stockdb'
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'
    postgres_host: str = 'localhost'
    postgres_port: int = 5432
    stock_symbols: str = 'AAPL,MSFT,NVDA,GOOGL,AMZN'
    technical_weight: float = 0.60
    sentiment_weight: float = 0.40
    buy_threshold: float = 0.65
    hold_threshold: float = 0.40
    telegram_bot_token: str = ''
    telegram_chat_id: str = ''
    smtp_host: str = ''
    smtp_port: int = 587
    smtp_user: str = ''
    smtp_password: str = ''
    smtp_from: str = 'alerts@example.com'
    alert_email: str = 'demo@example.com'


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
