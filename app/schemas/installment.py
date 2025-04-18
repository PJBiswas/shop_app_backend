from datetime import datetime, date

from pydantic import BaseModel


class InstallmentCreate(BaseModel):
    product_id: int
    installments: int


class InstallmentOut(InstallmentCreate):
    id: int
    paid_at: datetime

    class Config:
        orm_mode = True


class PayInstallmentRequest(BaseModel):
    schedule_id: int
    paid_at: datetime


class InstallmentScheduleOut(BaseModel):
    id: int
    due_date: date
    amount_due: float
    is_paid: bool

    class Config:
        orm_mode = True