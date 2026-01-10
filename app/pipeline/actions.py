from app.chart.candlestick import render_candlestick_chart

def execute(signals, market_data):
    chart_image = render_candlestick_chart(
        market_data["symbol"],
        market_data["interval"],
        market_data["ohlcv"],
        signals["indicators"],
    )

    # --- Candlestick / Trend ---
    if signals["trend"] == "bullish":
        candle_text = (
            "There is a prevailing bullish structure.\n"
            "Recent candles suggest buyers are still defending higher levels, "
            "though momentum may be slowing."
        )
    else:
        candle_text = (
            "Price is in a bearish or corrective phase.\n"
            "Recent candles show selling pressure with difficulty sustaining higher prices."
        )

    # --- MACD ---
    if "bullish" in signals["macd_text"]:
        macd_text = (
            "A bullish MACD structure is present.\n"
            "Momentum is improving, indicating buyers are gaining strength."
        )
    else:
        macd_text = (
            "A bearish MACD crossover is visible.\n"
            "The MACD line remains below the signal line, suggesting weakening momentum."
        )

    # --- RSI ---
    if "overbought" in signals["rsi_text"]:
        rsi_text = (
            "RSI is in the overbought zone.\n"
            "This often precedes a pullback or consolidation."
        )
    elif "oversold" in signals["rsi_text"]:
        rsi_text = (
            "RSI is in the oversold zone.\n"
            "This may hint at a potential short-term bounce."
        )
    else:
        rsi_text = (
            "RSI is in a neutral range.\n"
            "The market is balanced, with no extreme momentum on either side."
        )

    # --- Simple S/R (derived from recent range) ---
    prices = [float(c["close"]) for c in market_data["ohlcv"][-20:]]
    support = round(min(prices), 2)
    resistance = round(max(prices), 2)

    sr_text = (
        f"Support is observed near **{support}**, "
        f"while resistance is located around **{resistance}**."
    )

    # --- Actionable Insight ---
    if signals["trend"] == "bullish" and "bullish" in signals["macd_text"]:
        insight = (
            "Market Implication: Trend and momentum are aligned.\n"
            "Pullbacks may offer better risk-managed entries."
        )
    elif signals["trend"] == "bearish" and "bearish" in signals["macd_text"]:
        insight = (
            "Market Implication: Downtrend remains dominant.\n"
            "Rallies may face selling pressure; caution is advised."
        )
    else:
        insight = (
            "Market Implication: Mixed signals.\n"
            "Price may remain range-bound; patience is recommended."
        )

    analysis_text = f"""
### {market_data['symbol']} Technical Analysis ({market_data['interval'].upper()})

**1. Candlestick Analysis**
- {candle_text}

**2. MACD Analysis**
- {macd_text}

**3. RSI (Relative Strength Index) Examination**
- {rsi_text}

**4. Support and Resistance Levels**
- {sr_text}

### Actionable Insight
- {insight}
""".strip()

    return {
        "chart_image": chart_image,
        "analysis_text": analysis_text,
    }

def resolve_sentiment(trend, rsi_text, macd_text):
    if trend == "bearish" and "bearish" in macd_text:
        if "oversold" in rsi_text:
            return "Panic-driven selling pressure is present."
        return "Market sentiment is fearful with persistent distribution."

    if trend == "bullish" and "bullish" in macd_text:
        if "overbought" in rsi_text:
            return "Optimism is high, though short-term exhaustion is possible."
        return "Market sentiment is confident with steady accumulation."

    return "Market sentiment is uncertain, reflecting indecision among participants."

