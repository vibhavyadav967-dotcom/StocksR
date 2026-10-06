from __future__ import annotations

import requests

from backend.app.config import settings


def send_telegram_message(text: str) -> bool:
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return False

    url = f'https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage'
    payload = {'chat_id': settings.telegram_chat_id, 'text': text, 'parse_mode': 'HTML'}
    try:
        response = requests.post(url, data=payload, timeout=20)
        response.raise_for_status()
        return True
    except Exception:
        return False
