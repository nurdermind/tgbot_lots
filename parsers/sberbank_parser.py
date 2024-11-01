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

COOKIES_PATH = "cookies.pkl"


def save_cookies(driver, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)


def load_cookies(driver, file_path):
    try:
        with open(file_path, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except FileNotFoundError:
        logger.warning("Файл с cookies не найден")

def fetch_page_with_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

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
    driver.refresh()

    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(5)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

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
    html = fetch_page_with_selenium(url)

    if not html:
        return None

    match = re.search(r"<BidLastPriceOffer>([\d,.]+)</BidLastPriceOffer>", html)
    if match:
        price_text = match.group(1).replace(',', '.')
        print(price_text)
        return price_text
    else:
        logger.warning(f'Нет текущей цены для {url}')
        return None
