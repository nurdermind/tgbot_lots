from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.lot import Base, Lot
from config import DATABASE_URL
from parsers.parsers_manager import ParsersManager

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    Base.metadata.create_all(engine)


async def add_lot(name, url, owner_id):
    manager = ParsersManager()

    try:
        initial_price = await manager.get_price(url)
    except ValueError as e:
        raise ValueError(f"Error determining price for URL '{url}': {e}")

    new_lot = Lot(name=name, url=url, current_price=initial_price, owner_id=owner_id)

    session.add(new_lot)
    session.commit()
    return new_lot


def get_all_lots():
    return session.query(Lot).all()


def update_lot_price(lot, new_price):
    lot.current_price = new_price
    session.commit()
