from datetime import datetime

from sqlalchemy.orm import Session

from app.models import InstallmentSchedule, InstallmentPayment, PurchaseOrder
from app.models.installment_config import InstallmentConfig
from app.schemas.installment import InstallmentCreate


def create_installment_config(data: InstallmentCreate, db: Session):
    config = InstallmentConfig(**data.dict())
    db.add(config)
    db.commit()
    db.refresh(config)
    return config


def pay_installment(schedule_id: int, paid_at: datetime, db: Session):
    schedule = db.query(InstallmentSchedule).filter_by(id=schedule_id).first()
    if not schedule:
        raise ValueError("Installment schedule not found.")
    if schedule.is_paid:
        raise ValueError("Installment already paid.")

    # 1. Record payment with the provided timestamp
    payment = InstallmentPayment(
        schedule_id=schedule_id,
        amount_paid=schedule.amount_due,
        paid_at=paid_at  # This is the timestamp passed from the request
    )
    db.add(payment)

    # 2. Mark this installment as paid
    schedule.is_paid = True

    # 3. Check if all installments are now paid
    all_schedules = db.query(InstallmentSchedule).filter_by(order_id=schedule.order_id).all()
    if all(s.is_paid for s in all_schedules):
        order = db.query(PurchaseOrder).filter_by(id=schedule.order_id).first()
        order.is_completed = True

    db.commit()
    return {"message": "Installment paid successfully"}
