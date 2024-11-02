from telegram.ext import Application, CommandHandler
from bot.commands import start, create_lot, delete_lot
from config import TELEGRAM_TOKEN

lots = {}

def setup_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("create", create_lot))
    application.add_handler(CommandHandler("delete", delete_lot))

    return application
