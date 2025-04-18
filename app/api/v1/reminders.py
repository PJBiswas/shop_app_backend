from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.reminder_log import ReminderLog
from app.core.deps import get_current_user
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.reminder import ReminderOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ReminderOut])
def list_reminders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(ReminderLog).join(ReminderLog.schedule).join(ReminderLog.schedule.order)\
        .filter(ReminderLog.schedule.order.user_id == current_user.id).all()
