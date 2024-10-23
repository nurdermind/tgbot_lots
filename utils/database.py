from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.lot import Base, Lot
from config import DATABASE_URL

# Set up the database engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    # Initialize the database schema
    Base.metadata.create_all(engine)


def add_lot(name, url, owner_id):
    # Determine the initial price based on the URL (example switch between parsers)
    if "site1.com" in url:
        initial_price = site1_parser.get_price_from_site1(url)
    elif "site2.com" in url:
        initial_price = site2_parser.get_price_from_site2(url)
    else:
        raise ValueError(f"No parser available for URL: {url}")

    # Create a new Lot object
    new_lot = Lot(name=name, url=url, current_price=initial_price, owner_id=owner_id)

    # Add the lot to the session and commit to the database
    session.add(new_lot)
    session.commit()


def get_all_lots():
    return session.query(Lot).all()


def update_lot_price(lot, new_price):
    lot.current_price = new_price
    session.commit()
