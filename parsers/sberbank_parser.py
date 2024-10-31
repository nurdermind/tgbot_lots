import time
import pickle
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from logger_config import logger

# Путь к файлу для сохранения cookies
COOKIES_PATH = "cookies.pkl"


def save_cookies(driver, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
        logger.info("Cookies сохранены")


def load_cookies(driver, file_path):
    try:
        with open(file_path, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
            logger.info("Cookies загружены")
    except FileNotFoundError:
        logger.warning("Файл с cookies не найден")


def fetch_page_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        html = fetch_page_with_selenium(url)
        if html and "Challenge" not in html:
            return html
        time.sleep(3)  # Пауза перед повторной попыткой
        logger.warning(f"Повторная попытка загрузки страницы: {attempt + 1}")
    logger.error("Challenge не найден после всех попыток.")
    return None


def fetch_page_with_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Отключаем ненужные элементы для оптимизации
    prefs = {"profile.managed_default_content_settings.images": 2,
             "profile.managed_default_content_settings.stylesheets": 2,
             "profile.managed_default_content_settings.javascript": 1}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    driver.get(url)
    load_cookies(driver, COOKIES_PATH)
    driver.refresh()  # Обновляем страницу для применения cookies

    try:
        # Делаем паузу для загрузки всех скриптов
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        time.sleep(5)  # Дополнительная задержка

        # Проверяем наличие Challenge и обходим, если он есть
        if driver.execute_script("return typeof Challenge !== 'undefined';"):
            challenge = driver.execute_script("return Challenge;")
            challenge_id = driver.execute_script("return ChallengeId;")
            y = driver.execute_script("return test(arguments[0]);", challenge)

            driver.execute_script("""
                var client = new XMLHttpRequest();
                client.open("POST", window.location, false);
                client.setRequestHeader('X-AA-Challenge-ID', arguments[0]);
                client.setRequestHeader('X-AA-Challenge-Result', arguments[1]);
                client.setRequestHeader('X-AA-Challenge', arguments[2]);
                client.setRequestHeader('Content-Type', 'text/plain');
                client.send();
            """, challenge_id, y, challenge)

            time.sleep(2)
            driver.refresh()

        else:
            logger.error("Challenge не найден на странице.")
            return None

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Сохраняем cookies для последующих посещений
        save_cookies(driver, COOKIES_PATH)

        html = driver.page_source
    finally:
        driver.quit()

    return html


def clean_price(price_text):
    price_text = re.sub(r'[^0-9.]', '', price_text)
    if price_text.endswith('.'):
        price_text = price_text[:-1]
    return price_text


async def get_current_price(url):
    html = fetch_page_with_retry(url)

    if not html:
        return None

    # Ищем нужную цену с помощью регулярного выражения
    match = re.search(r"<BidLastPriceOffer>([\d,.]+)</BidLastPriceOffer>", html)
    if match:
        price_text = match.group(1).replace(',', '.')
        return price_text
    else:
        logger.warning(f'Нет текущей цены для {url}')
        return None
