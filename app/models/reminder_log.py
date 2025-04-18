from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class ReminderLog(Base):
    __tablename__ = "reminder_logs"

    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey("installment_schedules.id"), nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
