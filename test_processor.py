from app.pipeline.fetcher import fetch_market_data
from app.pipeline.processor import process

data = fetch_market_data("BTC/USD", "weekly")
signals = process(data)

print(signals)
