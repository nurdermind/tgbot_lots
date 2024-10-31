from telegram import Bot
from config import TELEGRAM_TOKEN
import telegram

bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram_message(chat_id, message):
    try:
        await bot.send_message(chat_id=chat_id, text=message, timeout=60)
    except telegram.error.TimedOut:
        print("Ошибка: превышен таймаут при отправке сообщения")
