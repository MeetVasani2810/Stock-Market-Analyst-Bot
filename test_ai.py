from app.pipeline.fetcher import fetch_market_data
from app.pipeline.processor import process
from app.ai.analyzer import generate_analysis

data = fetch_market_data("BTC/USD")
signals = process(data)

# Adapt process() output to analyzer expectations
summary = {
    "symbol": data["symbol"],
    "interval": data["interval"],
    "trend": signals["trend"],
    "rsi": {"state": signals["rsi_text"], "value": "N/A"},
    "macd": {"state": signals["macd_text"]},
    "bias": signals["trend"]
}

text = generate_analysis(summary)
print(text)
