import asyncio
from telegram import Bot
from app.config import BOT_TOKEN

async def delete_webhook():
    print("🔌 Connecting to Telegram API...")
    bot = Bot(token=BOT_TOKEN)
    
    print("🗑️  Deleting webhook...")
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("✅ Webhook deleted! You can now run polling or deploy new webhook logic.")
    print("ℹ️  'drop_pending_updates=True' was used to skip old accumulated messages.")

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ Error: BOT_TOKEN not found in environment variables/config.")
    else:
        asyncio.run(delete_webhook())
