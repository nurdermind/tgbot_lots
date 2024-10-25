from logger_config import logger
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from models.lot import Base, Lot
from config import DATABASE_URL
from parsers.parsers_manager import ParsersManager

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

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
    session = Session()
else:
    logger.error("Не удалось подключиться к базе данных.")

def init_db():
    Base.metadata.create_all(engine)
    logger.info("Схема базы данных инициализирована.")

async def add_lot(name, url, owner_id):
    manager = ParsersManager()
    try:
        initial_price = await manager.get_price(url)
    except ValueError as e:
        logger.error(f"Error determining price for URL '{url}': {e}")
        raise

    new_lot = Lot(name=name, url=url, current_price=initial_price, owner_id=owner_id)
    session.add(new_lot)
    session.commit()

    logger.info(f"Лот '{name}' с URL '{url}' успешно добавлен в базу данных.")

    return new_lot

def get_all_lots():
    lots = session.query(Lot).all()

    logger.info(f"Получено {len(lots)} лотов из базы данных.")

    return lots

def update_lot_price(lot, new_price):
    lot.current_price = new_price

    session.commit()

    logger.info(f"Цена лота '{lot.name}' обновлена до {new_price}.")
