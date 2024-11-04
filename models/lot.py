from sqlalchemy import Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
metadata = MetaData()

lots_table = Table(
    'lots', metadata,
    Column('id', Integer, primary_key=True),
    Column('url', String, nullable=False),
    Column('current_price', String),
    Column('owner_id', Integer),
)

metadata.create_all(engine)

Base = declarative_base()

class Lot(Base):
    __tablename__ = 'lots'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, unique=True)
    current_price = Column(String, nullable=False)
    owner_id = Column(String, nullable=False)

    __table_args__ = (
        Index('ix_lot_url', 'url'),
        Index('ix_lot_owner_id', 'owner_id'),
    )
