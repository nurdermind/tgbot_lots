from telegram import Update
from telegram.ext import CallbackContext
from utils.database import add_lot

async def create_lot(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("Используйте: /create_lot <url> <название>")
        return

    url = context.args[0]
    name = context.args[1]

    owner_id = str(update.message.chat_id)

    try:
        await add_lot(name, url, owner_id)
        await update.message.reply_text(f'Лот "{name}" с URL "{url}" создан и добавлен в базу данных.')
    except Exception as e:
        await update.message.reply_text(f'Ошибка при добавлении лота в базу данных: {e}')


# Async command to handle /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Привет! Используйте /create_lot <url> <название>, чтобы создать лот.')
