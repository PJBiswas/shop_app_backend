from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class InstallmentConfig(Base):
    __tablename__ = "installment_configs"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    installments = Column(Integer, nullable=False)

    product = relationship("Product", backref="installment_configs")
