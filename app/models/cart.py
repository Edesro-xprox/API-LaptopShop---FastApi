from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cart(Base):
    __tablename__ = "ddevlaptopshop"

    iShopId = Column(Integer, primary_key=True, index=True)
    iLaptopId = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=True)

