import time
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from logger_config import logger

def fetch_page_with_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
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
        WebDriverWait(driver, 40).until(
            lambda driver: driver.find_element(By.ID, "currentOffer").text.strip() != ""
        )

        html = driver.page_source
    finally:
        driver.quit()

    return html

def clean_price(price_text):
    return re.sub(r'[^0-9.]', '', price_text)

async def get_current_price(url):
    html = fetch_page_with_selenium(url)

    if not html:
        logger.error("Не удалось загрузить страницу.")
        return None

    soup = BeautifulSoup(html, 'html.parser')

    try:
        offer_element = soup.find('strong', {'id': 'currentOffer'})
        print(offer_element)
        if offer_element and offer_element.text.strip():  # Проверяем, что текст непустой
            offer_text = offer_element.text.strip().replace(' ', '').replace('RUB', '').replace(',', '.')
            return clean_price(offer_text)
        else:
            logger.warning(f'Нет информации о текущем предложении для {url}')
            return None
    except Exception as e:
        logger.error(f"Произошла ошибка при парсинге сайта {url}: {e}")
        return None
