from telegram import Update
from telegram.ext import CallbackContext
from utils.database import add_lot, delete_lot_from_db, get_all_lots_ids_and_urls
from scheduler import lots_cache
from models.lot import Lot
from utils.database import SessionLocal

async def create_lot(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        await update.message.reply_text("Используйте: /create <url>")
        return

    url = context.args[0]
    owner_id = str(update.message.chat_id)

    try:
        lot_id  = await add_lot(url, owner_id)

        with SessionLocal() as session:
            new_lot = session.query(Lot).get(lot_id)
            lots_cache[lot_id] = new_lot

        await update.message.reply_text(f'Лот "{new_lot.id}" с URL "{url}" создан и добавлен в базу данных.')
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

async def all_lots(update: Update, _: CallbackContext):
    lots = get_all_lots_ids_and_urls()
    if not lots:
        await update.message.reply_text("Нет доступных лотов.")
        return
    
    message = "\n".join([f"ID: `{lot.id}`, URL: {lot.url}" for lot in lots])
    await update.message.reply_text(message)


async def start(update: Update, _: CallbackContext):
    await update.message.reply_text(
        'Привет! Вот доступные команды:\n'
        '/create <url> - Создать лот\n'
        '/all - Показать все лоты\n'
        '/delete <id> - Удалить лот по ID'
    )
