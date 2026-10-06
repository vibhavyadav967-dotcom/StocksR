from __future__ import annotations

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from backend.app.config import settings


def build_html_report(report: dict) -> str:
    return f"""
    <html>
      <body>
        <h2>📊 AI Stock Market Report</h2>
        <p><strong>Date:</strong> {report.get('date', 'N/A')}</p>
        <p><strong>Symbol:</strong> {report.get('symbol', 'N/A')}</p>
        <p><strong>Price:</strong> ${report.get('price', 0):.2f}</p>
        <p><strong>Recommendation:</strong> {report.get('recommendation', 'N/A')}</p>
        <p><strong>Confidence:</strong> {report.get('confidence', 0) * 100:.0f}%</p>
        <p><strong>RSI:</strong> {report.get('rsi', 'N/A')}</p>
        <p><strong>SMA20:</strong> ${report.get('sma_20', 0):.2f}</p>
        <p><strong>SMA50:</strong> ${report.get('sma_50', 0):.2f}</p>
        <p><strong>MACD:</strong> {report.get('macd', 'N/A')}</p>
        <p><strong>News Sentiment:</strong> {report.get('news_sentiment', 'N/A')}</p>
        <p><strong>Final Score:</strong> {report.get('final_score', 0):.2f}</p>
        <p><strong>Explanation:</strong> {report.get('explanation', 'No explanation available.')}</p>
        <p><em>Educational and research use only. Not financial advice.</em></p>
      </body>
    </html>
    """


def send_email_report(report: dict) -> bool:
    if not settings.smtp_host or not settings.smtp_user or not settings.smtp_password:
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"AI Stock Report - {report.get('symbol', 'N/A')}"
    msg['From'] = settings.smtp_from
    msg['To'] = settings.alert_email
    msg.attach(MIMEText(build_html_report(report), 'html'))

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg)
    return True
