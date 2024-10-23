from bot.handlers import setup_bot

if __name__ == '__main__':
    application = setup_bot()
    application.run_polling()
