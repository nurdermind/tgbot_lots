import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth

from logger_config import logger

URL_PATTERN = 'https://178fz.roseltorg.ru/#com/applic/trade/lot/%s/procedure/%s'
EXPLAIN_PATH = "//*[contains(@href, '/#com/applic/create/lot/')]"
PRICE_PATH = "//*[text()='Последнее ценовое предложение:']/../div/div"


def fetch_page_with_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
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
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, EXPLAIN_PATH))
        )
        explain_url = driver.find_element(By.XPATH, EXPLAIN_PATH).get_attribute('href')
        explain_url = explain_url.split('/#com/applic/create/lot/')[-1]
        lot_url = URL_PATTERN % (explain_url.split('/')[0], explain_url.split('/')[2])
        driver.get(lot_url)
        logger.info(lot_url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, PRICE_PATH))
        )
        time.sleep(3)
        return driver.find_element(By.XPATH, PRICE_PATH).text
    except Exception as e:
        logger.error(f"Произошла ошибка при парсинге цены с {url}: {e}")
        return None
    finally:
        driver.quit()


def clean_price(price_text):
    price_text = re.sub(r'[^0-9.,]', '', price_text)
    return price_text


async def get_current_price(url):
    raw_price_text = fetch_page_with_selenium(url)
    logger.info(raw_price_text)
    if not raw_price_text:
        return None

    price = clean_price(raw_price_text)

    if price:
        return price
    else:
        logger.warning(f'Нет текущей цены для {url}')
        return None
