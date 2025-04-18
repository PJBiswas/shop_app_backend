from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.installment import InstallmentCreate, InstallmentOut, PayInstallmentRequest
from app.services.installment_service import create_installment_config, pay_installment

from fastapi import HTTPException


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=InstallmentOut)
def create_installment(data: InstallmentCreate, db: Session = Depends(get_db)):
    return create_installment_config(data, db)

@router.post("/pay", tags=["Installments"])
def pay_installment_api(
    data: PayInstallmentRequest,
    db: Session = Depends(get_db)
):
    try:
        return pay_installment(data.schedule_id, data.paid_at, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
