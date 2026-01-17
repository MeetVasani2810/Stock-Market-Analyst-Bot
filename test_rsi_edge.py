import pandas as pd
from app.pipeline.processor import process

def test_rsi_div_zero():
    # Create market data where price NEVER drops (only goes up or stays flat)
    # This causes 'loss' to be 0 for all windows, leading to division by zero
    closes = [100 + i for i in range(200)] # 100, 101, 102...
    
    market_data = {
        "symbol": "BTC/USD",
        "interval": "1week",
        "ohlcv": [
            {"datetime": f"2023-01-{i%30+1}", "open": c, "high": c, "low": c, "close": c}
            for i, c in enumerate(closes)
        ]
    }
    
    try:
        result = process(market_data)
        print("✅ Processed successfully")
        # Check if RSI is NaN or Inf
        rsi = result["indicators"][-1]["rsi"]
        print(f"RSI Value: {rsi}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_rsi_div_zero()
