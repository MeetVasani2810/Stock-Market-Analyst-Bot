import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ENV = os.getenv("ENV", "development")

def validate_config():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN missing")
    if not TWELVE_DATA_API_KEY:
        raise RuntimeError("TWELVE_DATA_API_KEY missing")
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY missing")
