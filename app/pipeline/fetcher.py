import requests
from datetime import datetime, timezone
from app.config import TWELVE_DATA_API_KEY

BASE_URL = "https://api.twelvedata.com"

def fetch_market_data(symbol: str):
    params = {
        "symbol": symbol,
        "interval": "1week",
        "outputsize": 150,
        "apikey": TWELVE_DATA_API_KEY,
    }

    r = requests.get(f"{BASE_URL}/time_series", params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    if "values" not in data:
        raise RuntimeError(f"Invalid data for {symbol}")

    return {
        "symbol": symbol,
        "interval": "1week",
        "ohlcv": list(reversed(data["values"])),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }
