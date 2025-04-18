from sqlalchemy import Column, Integer, ForeignKey, Date, Numeric, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class InstallmentSchedule(Base):
    __tablename__ = "installment_schedules"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    due_date = Column(Date, nullable=False)
    amount_due = Column(Numeric(10, 2), nullable=False)
    is_paid = Column(Boolean, default=False)

    purchase_order = relationship("PurchaseOrder", back_populates="installments_schedule")
