from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from bot.commands import start, create_lot, delete_lot, all_lots, button_handler
from config import TELEGRAM_TOKEN

lots = {}

def setup_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("create", create_lot))
    application.add_handler(CommandHandler("delete", delete_lot))
    application.add_handler(CommandHandler("all", all_lots))

    application.add_handler(CallbackQueryHandler(button_handler))

    return application
