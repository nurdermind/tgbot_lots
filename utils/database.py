from logger_config import logger
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from models.lot import Base, Lot
from config import DATABASE_URL
from parsers.parsers_manager import ParsersManager
import asyncio
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation, NotNullViolation

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def check_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("Подключение к базе данных установлено успешно.")
    except OperationalError as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        return False
    return True

if check_db_connection():
    logger.info("Подключение к базе данных успешно установлено.")
else:
    logger.error("Не удалось подключиться к базе данных.")

def init_db():
    Base.metadata.create_all(engine)
    logger.info("Схема базы данных инициализирована.")

async def add_lot(url, owner_id):
    with SessionLocal() as session:
        manager = ParsersManager()
        initial_price = await manager.get_price(url)
        new_lot = Lot(url=url, current_price=initial_price, owner_id=owner_id)
        try:
            session.add(new_lot)
            session.commit()
            logger.info(f"Лот с URL {url} успешно добавлен в базу данных.")
            return new_lot.id
        except IntegrityError as e:
            session.rollback()

            if isinstance(e.orig, (UniqueViolation, NotNullViolation)):
                return None
            else:
                raise e
        finally:
            session.close()

def delete_lot_from_db(lot_id):
    from scheduler import lots_cache
    
    with SessionLocal() as session:
        lot = session.query(Lot).get(lot_id)
        if lot:
            session.delete(lot)
            session.commit()
            lots_cache.pop(lot_id, None)
            logger.info(f"Лот с ID {lot_id} успешно удален.")
            return True
        else:
            logger.warning(f"Лот с ID {lot_id} не найден в базе данных.")
            return False

def get_all_lots_ids_and_urls():
    with SessionLocal() as session:
        lots = session.query(Lot.id, Lot.url).all()
    return lots

def get_all_lots():
    with SessionLocal() as session:
        lots = session.query(Lot).all()
    return lots

async def update_lot_price_async(lot, new_price):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, update_lot_price, lot, new_price)

def update_lot_price(lot, new_price):
    with SessionLocal() as session:
        lot = session.query(Lot).get(lot.id)
        if lot:
            lot.current_price = new_price
            session.add(lot)
            session.commit()
            logger.info(f"Цена лота '{lot.id}' обновлена до {new_price}.")
        else:
            logger.error(f"Лот с ID {lot.id} не найден для обновления.")
