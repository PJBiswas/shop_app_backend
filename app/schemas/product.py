from decimal import Decimal
from typing import Optional, List
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

    model_config = {
        "from_attributes": True
    }


class PaginatedProduct(BaseModel):
    total: int
    items: List[ProductOut]

    model_config = {
        "from_attributes": True
    }
