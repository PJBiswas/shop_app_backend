# from typing import List, Optional
#
# from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session, selectinload
# from sqlalchemy import desc
#
# from app.core.deps import get_current_user
# from app.db.session import SessionLocal
# from app.models.purchase_order import PurchaseOrder
# from app.models.user import User
# from app.schemas.purchase_response import (
#     PaginatedPurchaseOut,
#     PurchaseOut,
#     PurchaseWithInstallmentsOut
# )
# from app.schemas.purchase_base import PurchaseRequest
# from app.services.purchase_service import create_purchase
# from app.services.purchase_query_service import get_admin_filtered_purchases
#
# router = APIRouter()
#
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# @router.post("/", response_model=PurchaseOut)
# def purchase_product(
#     data: PurchaseRequest,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     try:
#         create_purchase(data, current_user.id, db)
#         order = db.query(PurchaseOrder) \
#             .options(selectinload(PurchaseOrder.installments_schedule)) \
#             .filter_by(user_id=current_user.id) \
#             .order_by(desc(PurchaseOrder.created_at)) \
#             .first()
#         return order
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#
# @router.get("/admin/all", response_model=PaginatedPurchaseOut)
# def get_all_orders(
#     skip: int = Query(0, ge=0),
#     limit: int = Query(10, le=100),
#     sort_by: Optional[str] = Query("created_at", enum=["created_at", "total_amount", "is_completed"]),
#     order: Optional[str] = Query("desc", enum=["asc", "desc"]),
#     search: Optional[str] = Query(None, description="Search by customer name or product name"),
#     db: Session = Depends(get_db)
# ):
#     return get_admin_filtered_purchases(
#         db=db,
#         skip=skip,
#         limit=limit,
#         sort_by=sort_by,
#         order=order,
#         search=search
#     )
#
#
# @router.get("/my-purchases", response_model=List[PurchaseWithInstallmentsOut])
# def get_my_purchases(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     purchases = db.query(PurchaseOrder) \
#         .options(selectinload(PurchaseOrder.installments_schedule)) \
#         .filter(PurchaseOrder.user_id == current_user.id) \
#         .order_by(PurchaseOrder.created_at.desc()) \
#         .all()
#
#     return purchases
