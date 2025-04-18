from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class InstallmentPayment(Base):
    __tablename__ = "installment_payments"

    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey("installment_schedules.id"), nullable=False)
    amount_paid = Column(Numeric(10, 2), nullable=False)
    paid_at = Column(DateTime(timezone=True), server_default=func.now())

    schedule = relationship("InstallmentSchedule", backref="payments")
