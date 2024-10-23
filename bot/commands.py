import threading
from telegram import Update
from telegram.ext import CallbackContext
from utils.tracker import track_price
from bot.handlers import lots

# Async command for creating a lot
async def create_lot(update: Update, context: CallbackContext):
    url = context.args[0]
    name = context.args[1]
    lots[name] = url

    await update.message.reply_text(f'Лот "{name}" с URL "{url}" создан.')
    threading.Thread(target=track_price, args=(url, update.message.chat_id)).start()

# Async command to handle /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Привет! Используйте /create_lot <url> <название>, чтобы создать лот.')
