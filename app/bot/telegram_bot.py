from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from app.config import BOT_TOKEN
from app.pipeline.fetcher import fetch_market_data
from app.pipeline.processor import process
from app.pipeline.actions import execute
from app.ai.fundamental import run_fundamental_analysis
from app.bot.utils import smart_split_message, parse_timeframe, SUPPORTED_TIMEFRAMES_MSG
import asyncio
from datetime import date

# --- HELPER FOR BLOCKING CALLS ---
async def run_blocking(func, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args)

# --- TEXT CONSTANTS (Version B: The Accessible Analyst) ---

WELCOME_TEXT = f"""
👋 **Welcome to Vantage**

Your personal AI market analyst — giving you the same insights that Wall Street uses.

✨ **WHAT YOU GET**

📊 **Instant Chart Analysis**
Get RSI, MACD, and trend signals in seconds.
`/technical AAPL 1hour`

📄 **Company Deep Dives**
Understand any stock's fundamentals, fast.
`/fundamental TSLA on NASDAQ 1day`

⏱️ **Any Timeframe**
From 1-minute scalping to monthly investing.

───────────────────────────────────
🛡️ Powered by TwelveData & GPT-4o
📅 Updated: {date.today().strftime('%b %d, %Y')}
⚠️ *Analysis only. Not financial advice. DYOR.*
"""

HELP_TEXT = """
**📚 VANTAGE COMMAND REFERENCE**

**🎯 Core Commands**
`/technical [SYMBOL] [TIMEFRAME]`
`/fundamental [SYMBOL] on [EXCHANGE] [TIMEFRAME]`

**⏱️ Timeframes**
`1min` `5min` `15min` `30min`
`1hour` `4hour` `12hour`
`1day` `1week` `1month`

**💡 Examples**
`/technical BTC 15min`
`/technical AAPL 4hour`
`/fundamental NVDA on NASDAQ 1day`

**ℹ️ Note:** Default timeframe is `1day`.
"""

TIMEFRAME_GUIDE_TEXT = """
**⏱️ TIMEFRAME CHEAT SHEET**

⚡ **Scalping (1-5min)**
Quick entries/exits. High volatility.

🏃 **Day Trading (15min-1hour)**
Intraday trends. Moderate risk.

🚶 **Swing Trading (4hour-1day)**
Multi-day holds. Lower risk.

🐌 **Investing (1week-1month)**
Long-term positions. Fundamental focus.

💡 **Pro Tip:** Combine timeframes for confluence!
"""

# --- TUTORIAL TEXTS ---
TUTORIAL_STEP_0 = """
🎓 **How would you like to learn?**

Choose your path:
"""

TUTORIAL_STEP_1 = """
🚀 **Watch Vantage in Action**

I'm analyzing Bitcoin on a 15-minute chart for you right now...
"""

TUTORIAL_STEP_2 = """
✨ **Your Turn!**

Pick an asset you follow, and I'll analyze it instantly.
"""

TUTORIAL_STEP_3 = """
⏱️ **Pick a Timeframe**

Different strategies need different views:
"""

TUTORIAL_COMPLETE = """
✅ **You're All Set!**

You now know how to:
• Run technical analysis on any asset
• Choose the right timeframe
• Read AI-powered signals

**Quick Reference:**
`/technical [SYMBOL] [TIMEFRAME]`
`/fundamental [SYMBOL] on [EXCHANGE]`

Happy trading! 🚀
"""

# --- KEYBOARDS ---
def get_main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✨ Try It Now (BTC)", callback_data="run_demo_btc")],
        [
            InlineKeyboardButton("🎓 Quick Tutorial", callback_data="tutorial_start"),
            InlineKeyboardButton("📚 All Commands", callback_data="show_help")
        ],
        [
            InlineKeyboardButton("⏱️ Timeframe Guide", callback_data="show_tf_guide"),
            InlineKeyboardButton("⭐ Rate Us", callback_data="rate_us")
        ]
    ])

def get_tutorial_path_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏃 Quick Demo (30s)", callback_data="tutorial_quick")],
        [InlineKeyboardButton("🎓 Full Tutorial", callback_data="tutorial_full")],
        [InlineKeyboardButton("⏭️ Skip — I Know This", callback_data="back_to_start")]
    ])

def get_tutorial_asset_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("BTC", callback_data="try_asset_btc"),
            InlineKeyboardButton("ETH", callback_data="try_asset_eth"),
            InlineKeyboardButton("AAPL", callback_data="try_asset_aapl"),
            InlineKeyboardButton("TSLA", callback_data="try_asset_tsla")
        ],
        [InlineKeyboardButton("🏠 Back to Menu", callback_data="back_to_start")]
    ])

def get_tutorial_timeframe_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚡ 5min", callback_data="try_tf_5min"),
            InlineKeyboardButton("⏰ 1hour", callback_data="try_tf_1hour"),
            InlineKeyboardButton("📅 1day", callback_data="try_tf_1day")
        ],
        [InlineKeyboardButton("✅ Finish Tutorial", callback_data="tutorial_complete")]
    ])

def get_tutorial_complete_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Start Analyzing", callback_data="back_to_start")],
        [InlineKeyboardButton("📚 Full Docs", callback_data="show_help")]
    ])

def get_back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_start")]])


# --- COMMAND HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_TEXT, 
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT, parse_mode="Markdown", reply_markup=get_back_keyboard())


# --- BUTTON HANDLER ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # --- NAVIGATION ---
    if data == "back_to_start":
        await query.message.edit_text(WELCOME_TEXT, parse_mode="Markdown", reply_markup=get_main_keyboard())
    elif data == "show_help":
        await query.message.edit_text(HELP_TEXT, parse_mode="Markdown", reply_markup=get_back_keyboard())
    elif data == "show_tf_guide":
        await query.message.edit_text(TIMEFRAME_GUIDE_TEXT, parse_mode="Markdown", reply_markup=get_back_keyboard())
    elif data == "rate_us":
        await query.message.reply_text("⭐ **Thank you!** Your feedback helps us improve.", parse_mode="Markdown")

    # --- DEMOS ---
    elif data == "run_demo_btc":
        context.args = ["BTC", "15min"]
        await analyze(update, context)

    # --- TUTORIAL FLOW ---
    elif data == "tutorial_start":
        await query.message.edit_text(TUTORIAL_STEP_0, parse_mode="Markdown", reply_markup=get_tutorial_path_keyboard())

    elif data == "tutorial_quick":
        await query.message.edit_text(TUTORIAL_STEP_1, parse_mode="Markdown")
        context.args = ["BTC", "15min"]
        await analyze(update, context)
        await query.message.reply_text(TUTORIAL_STEP_2, parse_mode="Markdown", reply_markup=get_tutorial_asset_keyboard())

    elif data == "tutorial_full":
        await query.message.edit_text(TUTORIAL_STEP_2, parse_mode="Markdown", reply_markup=get_tutorial_asset_keyboard())

    elif data.startswith("try_asset_"):
        asset = data.split("_")[-1].upper()
        await query.message.edit_text(TUTORIAL_STEP_3, parse_mode="Markdown", reply_markup=get_tutorial_timeframe_keyboard())
        context.user_data["tutorial_asset"] = asset

    elif data.startswith("try_tf_"):
        tf = data.split("_")[-1]
        asset = context.user_data.get("tutorial_asset", "BTC")
        context.args = [asset, tf]
        await analyze(update, context)
        await query.message.reply_text("👇 **Continue or finish:**", reply_markup=get_tutorial_timeframe_keyboard())

    elif data == "tutorial_complete":
        await query.message.edit_text(TUTORIAL_COMPLETE, parse_mode="Markdown", reply_markup=get_tutorial_complete_keyboard())


# --- ANALYSIS HANDLERS ---
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_message = update.message if update.message else update.callback_query.message

    if not context.args:
        await target_message.reply_text("Usage: `/technical SYMBOL [TIMEFRAME]`\nExample: `/technical BTC 15min`", parse_mode="Markdown")
        return

    api_timeframe = "1day"
    display_timeframe = "Daily"
    
    potential_timeframe = context.args[-1]
    tf_api, tf_display, is_valid = parse_timeframe(potential_timeframe)
    
    if is_valid:
        api_timeframe = tf_api
        display_timeframe = tf_display
        symbol_args = context.args[:-1]
    else:
        symbol_args = context.args

    if not symbol_args:
         await target_message.reply_text("❌ Please specify a symbol.\nExample: `/technical BTC 15min`", parse_mode="Markdown")
         return

    symbol = symbol_args[0].upper()
    if "/" not in symbol:
        symbol = f"{symbol}/USD"

    await target_message.reply_text(f"🔍 Analyzing **{symbol}** ({display_timeframe})...", parse_mode="Markdown")

    try:
        market_data = await run_blocking(fetch_market_data, symbol, api_timeframe)
        signals = await run_blocking(process, market_data)
        result = await run_blocking(execute, signals, market_data)

        if "Timeframe:" not in result["analysis_text"]:
             result["analysis_text"] = f"**Timeframe:** {display_timeframe}\n" + result["analysis_text"]

        await target_message.reply_photo(photo=result["chart_image"])
        await target_message.reply_text(result["analysis_text"], parse_mode="Markdown")

    except RuntimeError as e:
         if "Invalid data" in str(e):
             await target_message.reply_text(f"❌ Data unavailable for `{symbol}` on {display_timeframe}.\nTry `1day` or `1hour`.", parse_mode="Markdown")
         else:
             await target_message.reply_text(f"❌ Error: {str(e)}")
    except Exception as e:
        await target_message.reply_text(f"❌ Error: {str(e)}")


async def fundamental(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_message = update.message if update.message else update.callback_query.message

    if not context.args or " on " not in " ".join(context.args):
        await target_message.reply_text(
            "Usage:\n`/fundamental STOCK on EXCHANGE [TIMEFRAME]`\nExample: `/fundamental TSLA on NASDAQ 1day`",
            parse_mode="Markdown"
        )
        return

    potential_timeframe = context.args[-1]
    tf_api, tf_display, is_valid = parse_timeframe(potential_timeframe)
    
    args_to_join = context.args
    timeframe_context = "Daily"

    if is_valid:
        timeframe_context = tf_display
        args_to_join = context.args[:-1]
    
    text = " ".join(args_to_join)
    
    try:
        if " on " not in text:
             raise ValueError("Missing ' on ' keyword")

        stock_part, exchange = text.rsplit(" on ", 1)
        
        await target_message.reply_text(f"📊 Analyzing **{stock_part}** on {exchange}...", parse_mode="Markdown")
        
        analysis = await run_blocking(run_fundamental_analysis, stock_part, exchange, timeframe_context)
        
        chunks = smart_split_message(analysis)
        for i, chunk in enumerate(chunks):
            if len(chunks) > 1:
                prefix = f"🔹 **Part {i+1}/{len(chunks)}**\n\n"
                await target_message.reply_text(prefix + chunk, parse_mode="Markdown")
            else:
                await target_message.reply_text(chunk, parse_mode="Markdown")

    except ValueError:
        await target_message.reply_text("Invalid format. Use: `STOCK on EXCHANGE`", parse_mode="Markdown")
    except Exception as e:
        await target_message.reply_text(f"❌ Error: {str(e)}")


# --- BOT STARTUP ---
def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyze", analyze))
    app.add_handler(CommandHandler("technical", analyze))
    app.add_handler(CommandHandler("fundamental", fundamental))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Vantage bot started")
    
    from app.config import ENV, WEBHOOK_URL, PORT

    if ENV == "production" or WEBHOOK_URL:
        if not WEBHOOK_URL:
             raise RuntimeError("WEBHOOK_URL is required for production/webhook mode")
        
        print(f"🚀 Starting Webhook on port {PORT}")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
        )
    else:
        print("🔁 Starting Polling (Dev Mode)")
        app.run_polling()
