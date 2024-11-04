import threading
from bot.handlers import setup_bot
from scheduler import run_scheduler
from config import TELEGRAM_TOKEN, APP_URL

if __name__ == '__main__':
    application = setup_bot()

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    application.run_webhook(
        listen="0.0.0.0",
        port=8443,
        url_path=TELEGRAM_TOKEN,
        webhook_url=f"{APP_URL}/{TELEGRAM_TOKEN}"
    )
