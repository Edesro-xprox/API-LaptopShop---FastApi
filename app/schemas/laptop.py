from pydantic import BaseModel

class LaptopType(BaseModel):
    iLaptopId: int
    name: str
    image: str
    description: str
    price: float

    class Config:
        from_attributes = True
