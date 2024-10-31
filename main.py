# import time
# import threading
# from telegram import Update, Bot
# from telegram.ext import Application, CommandHandler, CallbackContext
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from logger_config import logger
#
# lots = {}
#
# def get_current_price_selenium(url):
#         chrome_options = Options()
#         chrome_options.add_argument('--headless')
#
#         service = Service(
#             executable_path='C:\\Users\\RobotComp.ru\\Documents\\webDrivers\\chromedriver-win64\\chromedriver.exe')
#
#         driver = webdriver.Chrome(service=service, options=chrome_options)
#
#         driver.get(url)
#
#         try:
#             price_element = driver.find_element(By.XPATH,
#                                                 '//label[contains(text(), "Начальная цена")]/following-sibling::span//span')
#
#             price_text = price_element.text.strip().replace(' ', '').replace(',', '.')
#
#         except Exception as e:
#             logger.error(f"Ошибка при получении данных: {e}")
#         finally:
#             driver.quit()
#
#         try:
#             return float(price_text)
#         except ValueError:
#             return None
#
# def send_telegram_message(token, chat_id, message):
#     bot = Bot(token)
#     bot.send_message(chat_id=chat_id, text=message)
#
# def track_price(url, chat_id):
#     last_price = None
#     while True:
#         current_price = get_current_price_selenium(url)
#         if current_price is not None and current_price != last_price:
#             message = f'Цена изменилась на {url}! Новая цена: {current_price}'
#             send_telegram_message(telegram_token, chat_id, message)
#             last_price = current_price
#         time.sleep(5)
#
# async def create_lot(update: Update, context: CallbackContext):
#     url = context.args[0]
#     name = context.args[1]
#     lots[name] = url
#
#     await update.message.reply_text(f'Лот "{name}" с URL "{url}" создан.')
#     threading.Thread(target=track_price, args=(url, update.message.chat_id)).start()
#
# async def start(update: Update, context: CallbackContext):
#     await update.message.reply_text('Привет! Используйте /create_lot <url> <название>, чтобы создать лот.')
#
# telegram_token = '7640225313:AAEop_kBDFsw3BlFN1o8hBq9u95vMaeBZcw'  # Замените на свой токен
#
# application = Application.builder().token(telegram_token).build()
#
# application.add_handler(CommandHandler("start", start))
# application.add_handler(CommandHandler("create_lot", create_lot))
#
# application.run_polling()
