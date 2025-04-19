from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.schemas.product import ProductOut
from app.schemas.installment import InstallmentScheduleOut


class InstallmentOut(BaseModel):
    due_date: datetime
    amount_due: float
    is_paid: bool

    model_config = {
        "from_attributes": True
    }


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    email: str

    model_config = {
        "from_attributes": True
    }


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

    model_config = {
        "from_attributes": True
    }


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

    model_config = {
        "from_attributes": True
    }
