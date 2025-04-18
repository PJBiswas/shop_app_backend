from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.customer import PaginatedCustomer
from app.services.customer_service import get_all_customers

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=PaginatedCustomer)
def read_all_customers(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, le=100),
        db: Session = Depends(get_db)
):
    return get_all_customers(db=db, skip=skip, limit=limit)
