from utils.database import add_lot, delete_lot_from_db, get_all_lots_ids_and_urls
from models.lot import Lot
from utils.database import SessionLocal
from logger_config import logger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import telegram

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("Создать лот", callback_data="create")],
        [InlineKeyboardButton("Удалить лот", callback_data="delete")],
        [InlineKeyboardButton("Показать все лоты", callback_data="all")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, _: CallbackContext):
    await update.message.reply_text(
        'Выберите действие:',
        reply_markup=get_main_keyboard()
    )

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    try:
        if query.data == "create":
            await prompt_create_lot(query, context)
        elif query.data == "delete":
            await prompt_delete_lot(query, context)
        elif query.data == "all":
            await show_all_lots(query, context)
    except telegram.error.BadRequest as e:
        if str(e) == "Message is not modified":
            logger.info("Сообщение не изменено, обновление не требуется.")
        else:
            logger.error(f"Ошибка при обновлении сообщения: {e}")

async def prompt_create_lot(query, context):
    await query.edit_message_text(
        "Для создания лота введите команду /create <url> или нажмите кнопку ниже для возврата в меню.",
        reply_markup=get_main_keyboard()
    )

async def prompt_delete_lot(query, context):
    await query.edit_message_text(
        "Для удаления лота введите команду /delete <ID лота> или нажмите кнопку ниже для возврата в меню.",
        reply_markup=get_main_keyboard()
    )

async def show_all_lots(query, context):
    lots = get_all_lots_ids_and_urls()
    if not lots:
        await query.edit_message_text("Нет доступных лотов.")
        return

    message = "\n".join([f"ID: `{lot.id}`, URL: {lot.url}" for lot in lots])
    await query.edit_message_text(message, reply_markup=get_main_keyboard())

async def create_lot(update: Update, context: CallbackContext):
    from scheduler import lots_cache

    if len(context.args) < 1:
        await update.message.reply_text("Используйте: /create <url>")
        return

    url = context.args[0]
    owner_id = str(update.message.chat_id)

    try:
        lot_id = await add_lot(url, owner_id)

        if lot_id is None:
            await update.message.reply_text(
                f'Не удалось добавить лот с URL "{url}". Возможно, он уже существует или данные некорректны.')
            return

        with SessionLocal() as session:
            new_lot = session.query(Lot).get(lot_id)
            if new_lot is None:
                await update.message.reply_text(f'Ошибка: не удалось найти лот после добавления.')
                return

            lots_cache[lot_id] = new_lot

        await update.message.reply_text(f'Лот "{new_lot.id}" с URL "{url}" создан и добавлен в базу данных.', reply_markup=get_main_keyboard())
    except Exception as e:
        logger.error("Ошибка при добавлении лота в базу данных", e)
        await update.message.reply_text(
            "Не удалось добавить лот из-за ошибки. Попробуйте снова или обратитесь за поддержкой.", reply_markup=get_main_keyboard())

async def delete_lot(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Используйте: /delete <ID лота>")
        return

    lot_id = context.args[0]
    if delete_lot_from_db(lot_id):
        await update.message.reply_text(f'Лот с ID {lot_id} успешно удален.', reply_markup=get_main_keyboard())
    else:
        await update.message.reply_text(f'Лот с ID {lot_id} не найден.', reply_markup=get_main_keyboard())

async def all_lots(update: Update, _: CallbackContext):
    lots = get_all_lots_ids_and_urls()
    if not lots:
        await update.message.reply_text("Нет доступных лотов.")
        return

    message = "\n".join([f"ID: `{lot.id}`, URL: {lot.url}" for lot in lots])
    await update.message.reply_text(message, reply_markup=get_main_keyboard())
