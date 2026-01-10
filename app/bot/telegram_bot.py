from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from app.config import BOT_TOKEN
from app.pipeline.fetcher import fetch_market_data
from app.pipeline.processor import process
from app.pipeline.actions import execute

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot ready\n\n"
        "Usage:\n"
        "/analyze BTC\n"
        "/analyze ETH"
    )

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /analyze SYMBOL")
        return

    symbol = context.args[0].upper()
    if "/" not in symbol:
        symbol = f"{symbol}/USD"

    await update.message.reply_text(f"🔍 Analyzing {symbol} (weekly)...")

    market_data = fetch_market_data(symbol)
    signals = process(market_data)
    result = execute(signals, market_data)

    await update.message.reply_photo(photo=result["chart_image"])
    await update.message.reply_text(result["analysis_text"])

def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analyze", analyze))
    print("🤖 Telegram bot started")
    app.run_polling()
