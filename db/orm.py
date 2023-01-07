from sqlalchemy import Column, String, Integer, SmallInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(SmallInteger)
