from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.installment_payment import InstallmentPayment
from app.models.installment_schedule import InstallmentSchedule
from app.models.product import Product
from app.models.purchase_order import PurchaseOrder
from app.models.user import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/overview")
def dashboard_overview(db: Session = Depends(get_db)):
    today = datetime.utcnow().date()

    # --- SUMMARY CARD DATA ---
    total_customers = db.query(User).count()
    total_products = db.query(Product).count()
    total_purchases = db.query(PurchaseOrder).count()

    total_paid = db.query(func.coalesce(func.sum(InstallmentPayment.amount_paid), 0)).scalar()
    total_due = db.query(func.coalesce(func.sum(InstallmentSchedule.amount_due), 0)).scalar() - total_paid

    # --- WEEKLY REPORT ---
    start_date = today - timedelta(weeks=5)
    weekly_report = []
    for i in range(5):
        week_start = start_date + timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)

        paid = db.query(func.coalesce(func.sum(InstallmentPayment.amount_paid), 0)) \
            .filter(func.date(InstallmentPayment.paid_at).between(week_start, week_end)) \
            .scalar()

        due = db.query(func.coalesce(func.sum(InstallmentSchedule.amount_due), 0)) \
            .filter(InstallmentSchedule.due_date.between(week_start, week_end)) \
            .scalar()

        weekly_report.append({
            "week": f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d')}",
            "paid": float(paid or 0),
            "due": float(due or 0)
        })

    # --- MONTHLY REPORT ---
    monthly_report = []
    for month in range(1, 13):
        month_paid = db.query(func.coalesce(func.sum(InstallmentPayment.amount_paid), 0)) \
            .filter(func.extract("month", InstallmentPayment.paid_at) == month) \
            .scalar()

        month_due = db.query(func.coalesce(func.sum(InstallmentSchedule.amount_due), 0)) \
            .filter(func.extract("month", InstallmentSchedule.due_date) == month) \
            .scalar()

        monthly_report.append({
            "month": datetime(2025, month, 1).strftime("%B"),
            "paid": float(month_paid or 0),
            "due": float(month_due or 0)
        })

    subquery_paid = db.query(
        InstallmentSchedule.order_id,
        func.sum(InstallmentPayment.amount_paid).label("total_paid")
    ).join(InstallmentPayment, InstallmentPayment.schedule_id == InstallmentSchedule.id) \
        .group_by(InstallmentSchedule.order_id) \
        .subquery()

    customer_aggregates = db.query(
        User.first_name,
        User.last_name,
        func.coalesce(func.sum(InstallmentPayment.amount_paid), 0).label("total_paid"),
        (func.coalesce(func.sum(InstallmentSchedule.amount_due), 0) - func.coalesce(
            func.sum(InstallmentPayment.amount_paid), 0)).label("total_due")
    ).join(PurchaseOrder, PurchaseOrder.user_id == User.id) \
        .join(InstallmentSchedule, InstallmentSchedule.order_id == PurchaseOrder.id) \
        .outerjoin(InstallmentPayment, InstallmentPayment.schedule_id == InstallmentSchedule.id) \
        .group_by(User.id) \
        .order_by(func.sum(InstallmentPayment.amount_paid).desc()) \
        .limit(5).all()

    top_customers = [
        {
            "name": f"{c.first_name} {c.last_name}",
            "total_paid": float(c.total_paid),
            "total_due": float(c.total_due)
        }
        for c in customer_aggregates
    ]

    overdue = db.query(
        User.first_name,
        User.last_name,
        Product.name.label("product"),
        InstallmentSchedule.due_date,
        InstallmentSchedule.amount_due
    ).join(PurchaseOrder, PurchaseOrder.user_id == User.id) \
        .join(Product, Product.id == PurchaseOrder.product_id) \
        .join(InstallmentSchedule, InstallmentSchedule.order_id == PurchaseOrder.id) \
        .filter(InstallmentSchedule.due_date < today) \
        .filter(InstallmentSchedule.is_paid == False) \
        .all()

    overdue_installments = [
        {
            "customer": f"{o.first_name} {o.last_name}",
            "product": o.product,
            "due_date": o.due_date.strftime("%Y-%m-%d"),
            "amount": float(o.amount_due)
        }
        for o in overdue
    ]

    return {
        "summary": {
            "total_customers": total_customers,
            "total_products": total_products,
            "total_purchases": total_purchases,
            "total_paid_amount": float(total_paid),
            "total_due_amount": float(total_due)
        },
        "weekly_report": weekly_report,
        "monthly_report": monthly_report,
        "top_customers": top_customers,
        "overdue_installments": overdue_installments
    }
