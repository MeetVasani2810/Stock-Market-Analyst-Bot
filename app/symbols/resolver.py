import re

CRYPTO_MAP = {
    "BTC": "BTC/USD",
    "ETH": "ETH/USD",
    "SOL": "SOL/USD",
}

INDIAN_STOCK_MAP = {
    "TATA MOTORS": "TATAMOTORS:NSE",
    "RELIANCE": "RELIANCE:NSE",
}

def normalize_symbol(raw: str) -> dict:
    s = raw.strip().upper()
    s = re.sub(r"\s+", " ", s)

    if s in CRYPTO_MAP:
        return {"symbol": CRYPTO_MAP[s], "asset_type": "crypto"}

    if "/" in s and s.endswith("USD"):
        return {"symbol": s, "asset_type": "crypto"}

    if s in INDIAN_STOCK_MAP:
        return {"symbol": INDIAN_STOCK_MAP[s], "asset_type": "indian_stock"}

    if s.endswith(":NSE"):
        return {"symbol": s, "asset_type": "indian_stock"}

    return {"symbol": s, "asset_type": "us_stock"}
