import pandas as pd
from app.indicators.ta import rsi, macd

# dummy close series
close = pd.Series([100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 110, 108, 107, 109, 111])

rsi_val = rsi(close)
macd_line, signal_line, hist = macd(close)

print("RSI (last):", round(rsi_val.iloc[-1], 2))
print("MACD (last):", round(macd_line.iloc[-1], 4))
print("Signal (last):", round(signal_line.iloc[-1], 4))
print("Hist (last):", round(hist.iloc[-1], 4))
