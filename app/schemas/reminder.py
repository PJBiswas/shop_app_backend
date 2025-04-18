from pydantic import BaseModel
from datetime import datetime

class ReminderOut(BaseModel):
    sent_at: datetime
    schedule_id: int

    class Config:
        from_attributes = True
