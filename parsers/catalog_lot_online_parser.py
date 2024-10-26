import random
import aiohttp
from bs4 import BeautifulSoup
import re
from logger_config import logger

async def fetch_page(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()

                return html
    except Exception as e:
        logger.error(f"Произошла ошибка при парсинге сайта {url}: {e}")

async def get_current_price(url):
    html = await fetch_page(url)

    if not html:
        return None

    soup = BeautifulSoup(html, 'html.parser')

    try:
        price = 0
        try:
            price_element = soup.find('label', text="Начальная цена").find_next('span')
            if price_element:
                price = price_element.text.strip().replace(' ', '').replace(',', '.')
        except Exception as e:
            logger.warn(f'Нет начальной цены для {url}')
        try:
            price_element = soup.find('label', text="Текущая цена лота").find_next('span')
            if price_element:
                price = price_element.text.strip().replace(' ', '').replace(',', '.')
        except Exception as e:
            logger.warn(f'Нет текущей цены для {url}')

        result = re.sub(r'[^0-9.]', '', price)

        return float(random.uniform(100, 200))
    except Exception as e:
        logger.error(f"Произошла ошибка при парсинге сайта {url}: {e}")
        return None
