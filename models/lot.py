from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.ext.declarative import declarative_base

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
