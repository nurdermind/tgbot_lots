import time
import threading
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, CallbackContext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

lots = {}

# Функция для получения текущей цены с веб-сайта с помощью Selenium
def get_current_price_selenium(url):
        # Настройка опций для браузера (например, чтобы он был безголовый - без графического интерфейса)
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        # Укажите путь к вашему драйверу Chrome
        service = Service(
            executable_path='C:\\Users\\RobotComp.ru\\Documents\\webDrivers\\chromedriver-win64\\chromedriver.exe')

        # Инициализация драйвера
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Переход на веб-страницу
        driver.get(url)

        # Поиск основного элемента, содержащего цену
        try:
            # Используем XPath для поиска метки с текстом "Начальная цена" и соседнего элемента span
            price_element = driver.find_element(By.XPATH,
                                                '//label[contains(text(), "Начальная цена")]/following-sibling::span//span')

            # Извлечение текста цены
            price_text = price_element.text.strip().replace(' ', '').replace(',', '.')

            print(f"Цена: {price_text} ₽")

        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
        finally:
            driver.quit()

        # Попытка преобразовать текст в число
        try:
            return float(price_text)
        except ValueError:
            return None

# Функция для отправки сообщения в Telegram
def send_telegram_message(token, chat_id, message):
    bot = Bot(token)
    bot.send_message(chat_id=chat_id, text=message)

# Функция для отслеживания цен
def track_price(url, chat_id):
    last_price = None
    while True:
        current_price = get_current_price_selenium(url)
        if current_price is not None and current_price != last_price:
            message = f'Цена изменилась на {url}! Новая цена: {current_price}'
            send_telegram_message(telegram_token, chat_id, message)
            last_price = current_price
        time.sleep(5)

# Асинхронная команда для создания лота
async def create_lot(update: Update, context: CallbackContext):
    url = context.args[0]
    name = context.args[1]
    lots[name] = url

    await update.message.reply_text(f'Лот "{name}" с URL "{url}" создан.')
    threading.Thread(target=track_price, args=(url, update.message.chat_id)).start()

# Асинхронная функция для обработки команды start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Привет! Используйте /create_lot <url> <название>, чтобы создать лот.')

telegram_token = '7640225313:AAEop_kBDFsw3BlFN1o8hBq9u95vMaeBZcw'  # Замените на свой токен

application = Application.builder().token(telegram_token).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("create_lot", create_lot))

application.run_polling()
