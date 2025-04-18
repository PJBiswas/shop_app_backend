from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.services.product_service import create_product, get_all_products, update_product

router = APIRouter()


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProductOut)
def create(data: ProductCreate, db: Session = Depends(get_db)):
    return create_product(data, db)


from app.schemas.product import PaginatedProduct


@router.get("/", response_model=PaginatedProduct)
def read_all(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, le=100),
        db: Session = Depends(get_db)
):
    return get_all_products(db=db, skip=skip, limit=limit)


@router.put("/{product_id}", response_model=ProductOut)
def update(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    try:
        return update_product(product_id, data, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
