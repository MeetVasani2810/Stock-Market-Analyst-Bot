from app.pipeline.fetcher import fetch_market_data
from app.pipeline.processor import process
from app.pipeline.actions import execute
from app.config import WATCHLIST
from app.symbols.parser import normalize_timeframe



async def run_scheduled_analysis(application):
    for item in WATCHLIST:
        symbol = item["symbol"]
        timeframe = normalize_timeframe(item["timeframe"])

        market_data = fetch_market_data(symbol, timeframe)
        signals = process(market_data)
        result = execute(signals, market_data)

        await application.bot.send_photo(
            chat_id=application.bot_data["CHAT_ID"],
            photo=result["chart_image"]
        )

        await application.bot.send_message(
            chat_id=application.bot_data["CHAT_ID"],
            text=result["analysis_text"]
        )
