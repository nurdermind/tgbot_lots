from sqlalchemy.orm import sessionmaker
from utils.database import get_all_lots, update_lot_price_async, engine
from parsers.parsers_manager import ParsersManager
from logger_config import logger
import asyncio
from utils.notifier import send_telegram_message
from utils.caller import make_call

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
            message = f"Цена лота, который находится по ссылке '{lot.url}' изменилась! Старая цена: {lot.current_price}, новая цена: {new_price}"

            await update_lot_price_async(lot, new_price)

            lots_cache[lot.id].current_price = new_price
            await make_call()
            await send_telegram_message(lot.owner_id, message)
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

def run_scheduler():
    load_lots_to_cache()
    asyncio.run(scheduled_task())
    manager.shutdown()