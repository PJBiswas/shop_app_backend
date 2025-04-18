from pydantic import BaseModel, EmailStr
from typing import List


class CustomerOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    is_verified: bool

    class Config:
        from_attributes = True


class PaginatedCustomer(BaseModel):
    total: int
    items: List[CustomerOut]

    class Config:
        from_attributes = True
