import pandas as pd


# ---------- INTERPRETATION HELPERS ----------

def interpret_rsi(value: float) -> str:
    if value >= 70:
        return "overbought (possible pullback)"
    if value <= 30:
        return "oversold (possible bounce)"
    return "neutral (balanced market)"


def interpret_macd(macd: float, signal: float) -> str:
    if macd > signal:
        return "bullish momentum"
    return "bearish momentum"


# ---------- MAIN PROCESSOR ----------

def process(market_data):
    df = pd.DataFrame(market_data["ohlcv"])
    df["close"] = df["close"].astype(float)

    # ---- RSI ----
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    rs = gain.rolling(14).mean() / loss.rolling(14).mean()
    df["rsi"] = 100 - (100 / (1 + rs))

    # ---- MACD ----
    ema12 = df["close"].ewm(span=12).mean()
    ema26 = df["close"].ewm(span=26).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]

    # Remove warm-up rows
    df = df.dropna()

    latest = df.iloc[-1]

    # ---- INTERPRETATION ----
    trend = "bullish" if latest["close"] > df["close"].iloc[-20] else "bearish"
    rsi_state = interpret_rsi(float(latest["rsi"]))
    macd_state = interpret_macd(
        float(latest["macd"]),
        float(latest["macd_signal"])
    )

    indicators = df[
        ["datetime", "rsi", "macd", "macd_signal", "macd_hist"]
    ].to_dict(orient="records")

    return {
        "trend": trend,
        "rsi_text": rsi_state,
        "macd_text": macd_state,
        "indicators": indicators,
    }
