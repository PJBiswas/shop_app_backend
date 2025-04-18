from decimal import Decimal
from typing import Optional
from typing import List
from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: Decimal


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]


class ProductOut(ProductCreate):
    id: int

    class Config:
        orm_mode = True




class PaginatedProduct(BaseModel):
    total: int
    items: List[ProductOut]

    class Config:
        from_attributes = True
