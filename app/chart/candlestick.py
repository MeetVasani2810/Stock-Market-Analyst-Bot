import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO


def render_candlestick_chart(symbol, interval, ohlcv, indicators):
    # ---------- DATA ----------
    df = pd.DataFrame(ohlcv)
    df[["open", "high", "low", "close"]] = df[
        ["open", "high", "low", "close"]
    ].astype(float)

    ind = pd.DataFrame(indicators)

    # --- ALIGN LENGTHS (PRE-C1 BEHAVIOR) ---
    df = df.iloc[-len(ind):].reset_index(drop=True)
    x = range(len(ind))

    # ---------- FIGURE ----------
    fig, (ax1, ax2, ax3) = plt.subplots(
        3,
        1,
        figsize=(14, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1, 1]},
    )

    # ---------- CANDLESTICKS ----------
    for i in x:
        o, h, l, c = df.iloc[i][["open", "high", "low", "close"]]
        color = "green" if c >= o else "red"

        ax1.plot([i, i], [l, h], color=color)
        ax1.bar(
            i,
            abs(c - o),
            bottom=min(o, c),
            color=color,
            width=0.6,
        )

    ax1.set_title(f"{symbol} — {interval.upper()}")
    ax1.grid(True)

    # ---------- RSI ----------
    ax2.plot(x, ind["rsi"], color="black")
    ax2.axhline(70, linestyle="--", color="gray")
    ax2.axhline(30, linestyle="--", color="gray")
    ax2.set_ylim(0, 100)
    ax2.grid(True)

    # ---------- MACD ----------
    ax3.plot(x, ind["macd"], color="black")
    ax3.plot(x, ind["macd_signal"], color="gray")
    ax3.bar(
        x,
        ind["macd_hist"],
        color=["green" if v >= 0 else "red" for v in ind["macd_hist"]],
        alpha=0.4,
    )
    ax3.grid(True)

    # ---------- OUTPUT ----------
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=120)
    buf.seek(0)
    plt.close(fig)

    return buf
