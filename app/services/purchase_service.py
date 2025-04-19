from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.installment_schedule import InstallmentSchedule
from app.models.product import Product
from app.models.purchase_order import PurchaseOrder
from app.schemas.purchase_base import PurchaseRequest


def create_purchase(data: PurchaseRequest, user_id: int, db: Session):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise ValueError("Invalid product")

    order = PurchaseOrder(
        user_id=user_id,
        product_id=product.id,
        total_amount=product.price
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    per_month_amount = product.price / 5
    today = datetime.utcnow().date()

    installments = []
    for i in range(5):
        due_date = today + timedelta(days=30 * (i + 1))
        installments.append(InstallmentSchedule(
            order_id=order.id,
            due_date=due_date,
            amount_due=per_month_amount,
            is_paid=False
        ))

    db.add_all(installments)
    db.commit()

    return order
