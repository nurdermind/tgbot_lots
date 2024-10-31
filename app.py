import threading
from bot.handlers import setup_bot
from scheduler import run_scheduler

if __name__ == '__main__':
    application = setup_bot()

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    application.run_polling()
