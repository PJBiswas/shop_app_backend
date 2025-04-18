from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(data: ProductCreate, db: Session):
    new_product = Product(**data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_all_products(db: Session, skip: int = 0, limit: int = 10):
    total = db.query(Product).count()
    items = db.query(Product).offset(skip).limit(limit).all()
    return {"total": total, "items": items}


def update_product(product_id: int, data: ProductUpdate, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ValueError("Product not found")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product
