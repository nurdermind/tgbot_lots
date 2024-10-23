import aiohttp
from bs4 import BeautifulSoup
import re

async def fetch_page(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                print(html)
                return html
    except Exception as e:
        print(f"Error: {e}")

async def get_current_price(url):
    html = await fetch_page(url)

    if not html:
        print("none")
        return None

    soup = BeautifulSoup(html, 'html.parser')

    try:
        price_element = soup.find('label', text="Начальная цена").find_next('span')
        price_text = price_element.text.strip().replace(' ', '').replace(',', '.')

        result = re.sub(r'[^0-9.]', '', price_text)
        print("eroe", result)
        return float(result)
    except Exception as e:
        print(f"Error parsing price from {url}: {e}")
        return None
