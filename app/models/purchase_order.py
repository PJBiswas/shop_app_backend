from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    installments_schedule = relationship("InstallmentSchedule", back_populates="purchase_order")
    user = relationship("User", backref="purchases")
    is_completed = Column(Boolean, default=False)
    product = relationship("Product", backref="purchases")
