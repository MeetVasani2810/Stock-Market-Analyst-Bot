from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from app.config import BOT_TOKEN
from app.pipeline.fetcher import fetch_market_data
from app.pipeline.processor import process
from app.pipeline.actions import execute
from app.ai.fundamental import run_fundamental_analysis
from app.bot.utils import smart_split_message
import asyncio
from datetime import date

# --- HELPER FOR BLOCKING CALLS ---
async def run_blocking(func, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args)

# --- TEXT CONSTANTS ---
WELCOME_TEXT = f"""
👋 **Welcome to your Market Copilot.**

Stop trading blind. Get institutional-grade market analysis in seconds.

**🚀 CORE CAPABILITIES**

📈 **Technical Scanner**
Trend reversal detection, RSI/MACD signals, and price action setups.
`Try: /technical BTC`

🏢 **Fundamental Deep Dives**
Balance sheets, earnings growth, and competitive moat analysis.
`Try: /fundamental GOOGL on NASDAQ`

⚡ **Quick Signals**
Instant support/resistance levels and market bias.

───────────────────────

**⚙️ SYSTEM STATUS**
• **Source:** TwelveData (Real-time)
• **Analysis:** OpenAI GPT-4o
• **Updated:** {date.today().strftime('%b %d, %Y')}

⚠️ *Disclaimer: Information for educational purposes only. Not financial advice. Always do your own research.*
"""

HELP_TEXT = """
**🤖 COMMAND CENTER**

**1️⃣ Market Analysis**
`/technical [SYMBOL]`
→ Get charts, trends, and indicators (RSI, MACD).
*Try: `/technical ETH`*

`/fundamental [SYMBOL] on [EXCHANGE]`
→ Get valuation, growth, and risk reports.
*Try: `/fundamental TCS on NSE`*

**2️⃣ System**
`/start` → Reboot & Welcome Menu
`/help` → Show this guide

**💡 Pro Tip:**
Use the **buttons** below for a faster experience!
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📈 Analyze Crypto", callback_data="help_technical"),
            InlineKeyboardButton("🏢 Analyze Stock", callback_data="help_fundamental"),
        ],
        [
            InlineKeyboardButton("📚 Complete Guide", callback_data="help_main"),
            InlineKeyboardButton("⭐ Rate Bot", callback_data="rate_us"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        WELCOME_TEXT, 
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "help_technical":
        await query.message.reply_text("👇 **Try it now!**\nType: `/technical BTC`", parse_mode="Markdown")
    elif query.data == "help_fundamental":
        await query.message.reply_text("👇 **Try it now!**\nType: `/fundamental APPLE on NASDAQ`", parse_mode="Markdown")
    elif query.data == "help_main":
        await query.message.reply_text(HELP_TEXT, parse_mode="Markdown")
    elif query.data == "rate_us":
        await query.message.reply_text("⭐ **Thank you for rating us!**\nWe appreciate your feedback.", parse_mode="Markdown")

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: `/technical SYMBOL`\nExample: `/technical BTC`", parse_mode="Markdown")
        return

    symbol = context.args[0].upper()
    if "/" not in symbol:
        symbol = f"{symbol}/USD"

    await update.message.reply_text(f"🔍 Analyzing {symbol} (weekly)...")

    try:
        # Run blocking fetch/process in thread pool to avoid freezing bot
        market_data = await run_blocking(fetch_market_data, symbol)
        signals = await run_blocking(process, market_data)
        result = await run_blocking(execute, signals, market_data)

        await update.message.reply_photo(photo=result["chart_image"])
        await update.message.reply_text(result["analysis_text"], parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def fundamental(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or " on " not in " ".join(context.args):
        await update.message.reply_text(
            "Usage:\n"
            "`/fundamental STOCK on EXCHANGE`\n"
            "Example: `/fundamental TCS on NSE`",
            parse_mode="Markdown"
        )
        return

    text = " ".join(context.args)
    
    try:
        stock_part, exchange = text.rsplit(" on ", 1)
        
        await update.message.reply_text(f"📊 Running fundamental analysis for {stock_part} ({exchange})...")
        
        # Blocking AI call
        analysis = await run_blocking(run_fundamental_analysis, stock_part, exchange)
        
        # Split message if too long
        chunks = smart_split_message(analysis)
        for i, chunk in enumerate(chunks):
            # Optional: Add continuity text if multiple chunks
            if len(chunks) > 1:
                prefix = f"🔹 **Part {i+1}/{len(chunks)}**\n\n"
                await update.message.reply_text(prefix + chunk, parse_mode="Markdown")
            else:
                await update.message.reply_text(chunk, parse_mode="Markdown")

    except ValueError:
        await update.message.reply_text("Invalid format. Use: STOCK on EXCHANGE")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Core Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    # Analysis Commands
    app.add_handler(CommandHandler("analyze", analyze))
    app.add_handler(CommandHandler("technical", analyze)) # Alias
    app.add_handler(CommandHandler("fundamental", fundamental))
    
    # Check for callback queries (buttons)
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Telegram bot started")
    app.run_polling()



