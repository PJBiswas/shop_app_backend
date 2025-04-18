from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Query
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload

from app.core.deps import get_current_user
from app.db.session import SessionLocal
from app.models.purchase_order import PurchaseOrder
from app.models.user import User
from app.schemas.purchase import PaginatedPurchaseOut
from app.schemas.purchase import PurchaseRequest, PurchaseOut, PurchaseWithInstallmentsOut
from app.services.purchase_service import create_purchase

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PurchaseOut)
def purchase_product(
        data: PurchaseRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    try:
        create_purchase(data, current_user.id, db)
        order = db.query(PurchaseOrder) \
            .options(selectinload(PurchaseOrder.installments_schedule)) \
            .filter_by(user_id=current_user.id) \
            .order_by(PurchaseOrder.created_at.desc()) \
            .first()
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/admin/all", response_model=PaginatedPurchaseOut)
def get_all_orders(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, le=100),
        db: Session = Depends(get_db)
):
    total = db.query(PurchaseOrder).count()
    orders = db.query(PurchaseOrder) \
        .options(
        selectinload(PurchaseOrder.user),
        selectinload(PurchaseOrder.installments_schedule),
        selectinload(PurchaseOrder.product)  # ✅ Load product data
    ) \
        .offset(skip) \
        .limit(limit) \
        .all()

    return {"total": total, "items": orders}


@router.get("/my-purchases", response_model=List[PurchaseWithInstallmentsOut])
def get_my_purchases(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    purchases = db.query(PurchaseOrder) \
        .options(selectinload(PurchaseOrder.installments_schedule)) \
        .filter(PurchaseOrder.user_id == current_user.id) \
        .order_by(PurchaseOrder.created_at.desc()) \
        .all()

    return purchases
