from sqlalchemy.orm import Session

from app.models.user import User


def get_all_customers(db: Session, skip: int = 0, limit: int = 10):
    total = db.query(User).count()
    items = db.query(User).offset(skip).limit(limit).all()
    return {"total": total, "items": items}
