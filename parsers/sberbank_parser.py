import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth

from logger_config import logger

PRICE_PATH_PATTERN = "//*[@id='tblBidsbody']/tr[%s]//td[contains(text(), 'Последнее предложение о цене')]/following::span"


def fetch_page_with_selenium(url, lot_number=1):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
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

    try:
        price_path = PRICE_PATH_PATTERN % lot_number
        print(price_path)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, price_path))
        )
        # time.sleep(2)  # ждем пока страница загрузится полностью
        return driver.find_element(By.XPATH, price_path).text
    except Exception as e:
        logger.error(f'Ошибка при получении текущей цены: {e}')
        return None
    finally:
        driver.quit()


def clean_price(price_text):
    price_text = re.sub(r'[^0-9.]', '', price_text)
    if price_text.endswith('.'):
        price_text = price_text[:-1]
    return price_text


async def get_current_price(url):
    try:
        lot_number = int(url.split('#')[-1])
    except Exception as e:
        logger.error(f"Ошибка при получении позиции лота из URL {url}: {e}")
        return None
    price_text = fetch_page_with_selenium(url, lot_number)

    if not price_text:
        logger.warning(f'Нет текущей цены для {url}')
        return None

    return clean_price(price_text)
