from telegram import Bot
from config import TELEGRAM_TOKEN
import telegram
from logger_config import logger

bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram_message(chat_id, message):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except telegram.error.TimedOut:
        logger.error("Ошибка: превышен таймаут при отправке сообщения")
        