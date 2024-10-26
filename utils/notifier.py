from telegram import Bot
from config import TELEGRAM_TOKEN

bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram_message(chat_id, message):
    await bot.send_message(chat_id=chat_id, text=message)
