import time
from sqlalchemy.orm import sessionmaker
from utils.database import get_all_lots, update_lot_price, engine
from parsers.parsers_manager import ParsersManager
from logger_config import logger
import asyncio

manager = ParsersManager()
SessionLocal = sessionmaker(bind=engine)

async def parse_lot(lot):
    session = SessionLocal()

    try:
        new_price = await manager.get_price(lot.url)
        if new_price is not None and new_price != lot.current_price:
            update_lot_price(session, lot, new_price)
            logger.info(f"Updated price for {lot.name} to {new_price}.")
        else:
            logger.info(f"No price change for {lot.name}.")
    except Exception as e:
        logger.error(f"Error parsing lot {lot.name}: {e}")
        session.rollback()
    finally:
        session.close()

async def scheduled_task():
    lots = get_all_lots()
    tasks = [parse_lot(lot) for lot in lots]
    await asyncio.gather(*tasks)

def run_scheduler():
    while True:
        asyncio.run(scheduled_task())
        time.sleep(1)
