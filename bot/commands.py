from telegram import Update
from telegram.ext import CallbackContext
from utils.database import add_lot, delete_lot_from_db
from scheduler import lots_cache
from models.lot import Lot
from utils.database import SessionLocal

async def create_lot(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("Используйте: /create_lot <url> <название>")
        return

    url = context.args[0]
    name = context.args[1]
    owner_id = str(update.message.chat_id)

    try:
        lot_id  = await add_lot(name, url, owner_id)

        with SessionLocal() as session:
            new_lot = session.query(Lot).get(lot_id)
            lots_cache[lot_id] = new_lot

        await update.message.reply_text(f'Лот "{name}" с URL "{url}" создан и добавлен в базу данных.')
    except Exception as e:
        await update.message.reply_text(f'Ошибка при добавлении лота в базу данных: {e}')
        raise Exception(f'Ошибка при добавлении лота в базу данных: {e}')


async def delete_lot(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Используйте: /delete <ID лота>")
        return

    lot_id = context.args[0]
    if delete_lot_from_db(lot_id):
        await update.message.reply_text(f'Лот с ID {lot_id} успешно удален.')
    else:
        await update.message.reply_text(f'Лот с ID {lot_id} не найден.')


async def start(update: Update, _: CallbackContext):
    await update.message.reply_text('Привет! Используйте /create_lot <url> <название>, чтобы создать лот.')
