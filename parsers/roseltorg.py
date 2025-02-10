import json
import re
import time

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
from seleniumwire import webdriver

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
    driver = webdriver.Chrome(options=options,
                              seleniumwire_options={
                                  'enable_har': True,
                                  'disable_encoding': True
                              })

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
        procedure_requests = [r for r in driver.requests if 'action=Procedure.load' in r.url]
        logger.info(procedure_requests)
        if not procedure_requests:
            logger.error(f"Произошла ошибка при запросе лотов {url}: {procedure_requests=}")
            return None
        headers = json.loads(procedure_requests[0].body)['headers']
        token = json.loads(procedure_requests[0].body)['token']
        logger.info(f"Procedure request {token}, {headers}")
        response_data = json.loads(procedure_requests[0].response.body)
        lots_data = response_data['result']['procedure']['lots']
        logger.info(lots_data)
        return lots_data, token, headers
    except Exception as e:
        logger.error(f"Произошла ошибка при парсинге цены с {url}: {e}")
        return None
    finally:
        driver.quit()


def clean_price(price_text):
    price_text = re.sub(r'[^0-9.,]', '', price_text)
    return price_text


async def get_current_price(url):
    result = fetch_page_with_selenium(url)
    if result is None:
        return None
    lots_data, token, headers = result
    try:
        lot_position = int(url.split('#')[-1])
    except Exception as e:
        logger.error(f"Ошибка при получении позиции лота из URL {url}: {e}")
        return None

    lot_data = lots_data[lot_position-1]
    request_data = {
        "action": "Applic",
        "method": "loadForTrade",
        "data": [
            {
                "procedure_id": lot_data['procedure_id'],
                "lot_id": lot_data['id']
            }
        ],
        "type": "rpc",
        "tid": 3,
        "token": token
    }
    r = requests.post(
        url='https://178fz.roseltorg.ru/index.php?rpctype=direct&module=default&action=Applic.loadForTrade',
        headers=headers,
        json=request_data,
        timeout=10,
        allow_redirects=True,
    )
    r.raise_for_status()
    data = r.json()['result']
    return data['last_offer']['price']
