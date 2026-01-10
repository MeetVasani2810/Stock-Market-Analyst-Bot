# from app.pipeline.fetcher import fetch_market_data

# data = fetch_market_data("BTC/USD", "weekly")

# print("Keys:", data.keys())
# print("OHLCV sample:", data["ohlcv"][:2])
# print("RSI latest:", data["rsi"][0])
# print("MACD latest:", data["macd"][0])

from app.pipeline.fetcher import fetch_market_data
import json

data = fetch_market_data("BTC/USD", "weekly")

print(json.dumps(data["macd"][0], indent=2))
