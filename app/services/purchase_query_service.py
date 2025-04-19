from typing import Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import asc, desc
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
    search: Optional[str] = None
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

    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            (User.first_name.ilike(search_term)) |
            (User.last_name.ilike(search_term)) |
            (Product.name.ilike(search_term))
        )

    total = query.count()

    orders = query.order_by(order_fn(sort_column)) \
        .offset(skip) \
        .limit(limit) \
        .all()

    return PaginatedPurchaseOut(total=total, items=orders)
