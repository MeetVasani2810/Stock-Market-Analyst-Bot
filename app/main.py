from app.config import validate_config, ENV
from app.db.database import init_db
from app.bot.telegram_bot import start_bot
from app.scheduler import start_scheduler

def main():
    validate_config()
    init_db()

    print(f"Automation system started in [{ENV}] mode")

    start_scheduler()   # automatic runs
    start_bot()         # manual control

if __name__ == "__main__":
    main()
