from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.purchase_order import PurchaseOrder
from app.services.report_generator import generate_excel_report, generate_pdf_report

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/reports/excel")
def download_excel_report(db: Session = Depends(get_db)):
    purchases = db.query(PurchaseOrder).all()
    return generate_excel_report(purchases)

@router.get("/reports/pdf")
def download_pdf_report(db: Session = Depends(get_db)):
    purchases = db.query(PurchaseOrder).all()
    return generate_pdf_report(purchases)
