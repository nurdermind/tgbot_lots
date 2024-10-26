from bot.handlers import setup_bot
from scheduler import run_scheduler

if __name__ == '__main__':
    run_scheduler()
    application = setup_bot()
    application.run_polling()
