from pathlib import Path
import textwrap
import zipfile

root = Path("/mnt/data/AI_Stock_Recommendation_Project")
(root / "python-service").mkdir(parents=True, exist_ok=True)
(root / "sql").mkdir(exist_ok=True)
(root / "n8n" / "workflows").mkdir(parents=True, exist_ok=True)

files = {
    root / "python-service" / "market_data.py": '''
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"


def get_stock_data(symbol: str) -> dict:
    """Fetch daily stock data from Alpha Vantage."""
    if not API_KEY:
        raise RuntimeError(
            "ALPHA_VANTAGE_API_KEY is missing. "
            "Create a .env file and add your API key."
        )

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol.upper(),
        "outputsize": "compact",
        "apikey": API_KEY,
    }

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if "Note" in data:
        raise RuntimeError(
            "The API returned a rate-limit message. "
            "Wait and try again later."
        )

    if "Time Series (Daily)" not in data:
        raise ValueError(f"Unexpected API response: {data}")

    return data


def convert_to_dataframe(data: dict) -> pd.DataFrame:
    """Convert Alpha Vantage daily data to a clean DataFrame."""
    time_series = data["Time Series (Daily)"]

    df = pd.DataFrame.from_dict(time_series, orient="index")

    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    df.columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    df = df.astype(float)

    return df


if __name__ == "__main__":
    symbol = input("Enter stock symbol (example: IBM): ").strip()

    raw_data = get_stock_data(symbol)
    df = convert_to_dataframe(raw_data)

    print("\\nLatest 10 trading days:\\n")
    print(df.tail(10))
''',

    root / "python-service" / "requirements.txt": '''
pandas
requests
python-dotenv
''',

    root / ".env.example": '''
# Copy this file to .env and replace the value with your real API key.
ALPHA_VANTAGE_API_KEY=YOUR_ALPHA_VANTAGE_API_KEY
''',

    root / ".gitignore": '''
.env
__pycache__/
*.pyc
.venv/
venv/
.vscode/
.idea/
''',

    root / "README.md": '''
# AI-Powered Stock Market Recommendation Workflow

This project will be built in stages:

1. Market-data collection with Python
2. Technical indicators: SMA, RSI, MACD
3. Recommendation engine: BUY / HOLD / AVOID
4. Financial-news collection
5. LLM-based news sentiment
6. Combined recommendation score
7. PostgreSQL database
8. FastAPI backend
9. n8n workflow automation
10. Telegram notifications
11. Email reports
12. Dashboard
13. Backtesting and evaluation
14. Docker deployment

## Step 1: Market Data

### Requirements

- Python 3.10+
- An Alpha Vantage API key

### Setup on Windows

Open PowerShell in this folder:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r python-service\\requirements.txt
```

Copy `.env.example` to `.env` and add your API key.

Then:

```powershell
cd python-service
python market_data.py
```

Enter a symbol such as:

```text
IBM
```

The program should print the latest 10 trading days.

## Important

Do not upload `.env` or API keys to GitHub.
''',

    root / "sql" / "schema.sql": '''
-- Database schema will be expanded in later steps.
-- Do not run this yet.
''',

    root / "n8n" / "workflows" / "README.md": '''
n8n workflows will be added after the Python analysis API is working.
'''
}

for path, content in files.items():
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")

zip_path = Path("/mnt/data/AI_Stock_Recommendation_Project_Step1.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for path in root.rglob("*"):
        if path.is_file():
            z.write(path, path.relative_to(root.parent))

print(f"Created starter project: {zip_path}")
