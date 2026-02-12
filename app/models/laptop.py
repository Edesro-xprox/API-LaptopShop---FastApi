from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Laptop(Base):
    __tablename__ = "mdevlaptop"

    iLaptopId = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    image = Column(String(255), nullable=True)
    description = Column(String(1024), nullable=True)
    price = Column(Float, nullable=False)

