from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.installment import InstallmentScheduleOut
from app.schemas.product import ProductOut


class PurchaseRequest(BaseModel):
    product_id: int


class InstallmentOut(BaseModel):
    due_date: datetime
    amount_due: float
    is_paid: bool

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    email: str

    class Config:
        orm_mode = True


class PurchaseOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    total_amount: float
    created_at: datetime
    is_completed: bool
    installments_schedule: List[InstallmentOut]
    user: UserOut
    product: ProductOut

    class Config:
        orm_mode = True


class PaginatedPurchaseOut(BaseModel):
    total: int
    items: List[PurchaseOut]

class PurchaseWithInstallmentsOut(BaseModel):
    id: int
    product_id: int
    total_amount: float
    created_at: datetime
    is_completed: bool
    installments_schedule: List[InstallmentScheduleOut]

    class Config:
        orm_mode = True
