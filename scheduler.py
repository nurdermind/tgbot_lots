import aiohttp
from sqlalchemy.orm import sessionmaker
from utils.database import get_all_lots, update_lot_price_async, engine
from parsers.parsers_manager import ParsersManager
from logger_config import logger
import asyncio
from utils.notifier import send_telegram_message
from utils.caller import send_sms
from config import TELEGRAM_IDS, TLY_API

manager = ParsersManager()
SessionLocal = sessionmaker(bind=engine)

lots_cache = {}

def load_lots_to_cache():
    global lots_cache
    lots = get_all_lots()
    lots_cache = {lot.id: lot for lot in lots}

async def parse_lot(session, lot_id):
    try:
        lot = session.query(type(lots_cache[lot_id])).get(lot_id)
        new_price = await manager.get_price(lot.url)

        if new_price is not None and new_price != lot.current_price:
            url = await shorten_link_tly(lot.url)

            tg_message = f"Цена лота {lot.url} изменилась! Старая цена: {lot.current_price}, новая цена: {new_price}"
            sms_message = f"'{url}' Б:{lot.current_price}.С:{new_price}"

            if len(sms_message) >= 70:
                sms_message = url

            await update_lot_price_async(lot, new_price)

            lots_cache[lot.id].current_price = new_price
            await send_sms(sms_message)

            for chat_id in TELEGRAM_IDS.split(","):
                await send_telegram_message(chat_id, tg_message)
        else:
            logger.info(f"Цена не изменилась для лота '{lot.id}'.")
    except Exception as e:
        logger.error(f"Ошибка при парсинге лота '{lot_id}': {e}")
        session.rollback()
    finally:
        session.commit()

async def scheduled_task():
    while True:
        load_lots_to_cache()

        with SessionLocal() as session:
            tasks = [parse_lot(session, lot_id) for lot_id in lots_cache.keys()]
            await asyncio.gather(*tasks)

        await asyncio.sleep(5)

async def shorten_link_tly(long_url):
    api_url = "https://t.ly/api/v1/link/shorten"
    headers = {"Content-Type": "application/json"}
    data = {
        "long_url": long_url,
        "domain": "https://t.ly",
        "api_token": TLY_API
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json=data, headers=headers) as response:
            if response.status == 200:
                short_url = await response.json()
                return short_url.get("short_url")
            else:
                logger.error("Ошибка:", await response.text())
                return None

def run_scheduler():
    load_lots_to_cache()
    asyncio.run(scheduled_task())
    manager.shutdown()