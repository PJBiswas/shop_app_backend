from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import asc, desc, func
from app.models.purchase_order import PurchaseOrder
from app.models.user import User
from app.models.product import Product
from app.schemas.purchase_response import PaginatedPurchaseOut


def get_admin_filtered_purchases(
        db: Session,
        skip: int,
        limit: int,
        sort_by: str = "created_at",
        order: str = "desc",
        customer_name: Optional[str] = None,
        product_name: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
) -> PaginatedPurchaseOut:
    order_fn = asc if order == "asc" else desc
    sort_column = getattr(PurchaseOrder, sort_by, PurchaseOrder.created_at)

    query = db.query(PurchaseOrder) \
        .join(PurchaseOrder.user) \
        .join(PurchaseOrder.product) \
        .options(
        selectinload(PurchaseOrder.user),
        selectinload(PurchaseOrder.installments_schedule),
        selectinload(PurchaseOrder.product)
    )

    if customer_name:
        search = f"%{customer_name.lower()}%"
        query = query.filter(
            (func.lower(User.first_name).ilike(search)) |
            (func.lower(User.last_name).ilike(search))
        )

    if product_name:
        search = f"%{product_name.lower()}%"
        query = query.filter(func.lower(Product.name).ilike(search))

    if start_date:
        query = query.filter(PurchaseOrder.created_at >= datetime.fromisoformat(start_date))

    if end_date:
        query = query.filter(PurchaseOrder.created_at <= datetime.fromisoformat(end_date))

    # safer count
    total = query.count()

    orders = query.order_by(order_fn(sort_column)) \
        .offset(skip) \
        .limit(limit) \
        .all()

    return PaginatedPurchaseOut(total=total, items=orders)
