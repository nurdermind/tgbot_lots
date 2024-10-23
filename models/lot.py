from sqlalchemy import Column, Integer, String, Float, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Lot(Base):
    __tablename__ = 'lots'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    current_price = Column(Float, nullable=False)
    owner_id = Column(String, nullable=False)

    # Indexes to improve performance on specific queries
    __table_args__ = (
        Index('ix_lot_url', 'url'),  # Index on URL for fast lookup
        Index('ix_lot_owner_id', 'owner_id'),  # Index on owner_id for quick search by owner
    )
