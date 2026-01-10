from app.pipeline.fetcher import fetch_market_data
from app.pipeline.processor import process
from app.ai.analyzer import generate_analysis

data = fetch_market_data("BTC/USD", "weekly")
signals = process(data)

text = generate_analysis(signals)
print(text)
