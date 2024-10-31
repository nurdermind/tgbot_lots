import time
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from logger_config import logger
import re


def fetch_page_with_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

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
        time.sleep(10)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "td[aria-describedby='jqgLots_BestApplicationQuotationStr']"))
        )

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

    soup = BeautifulSoup(html, 'html.parser')

    try:
        price_element = soup.find('td', {'aria-describedby': 'jqgLots_BestApplicationQuotationStr'})

        if price_element and price_element.get('title'):
            price_text = price_element['title'].strip().replace(' ', '').replace(',', '.')
            price_text = clean_price(price_text)
        else:
            logger.warning(f'Нет текущей цены для {url}')
            return None

        return price_text if price_text else None
    except Exception as e:
        logger.error(f"Произошла ошибка при парсинге цены с {url}: {e}")
        return None
