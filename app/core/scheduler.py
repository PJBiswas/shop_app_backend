from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.core.email_utils import send_email
from app.db.session import SessionLocal
from app.models.installment_schedule import InstallmentSchedule
from app.models.reminder_log import ReminderLog


def send_due_reminders():
    db: Session = SessionLocal()

    upcoming_due = db.query(InstallmentSchedule).filter(
        InstallmentSchedule.due_date == datetime.utcnow().date() + timedelta(days=3),
        InstallmentSchedule.is_paid == False
    ).all()

    for schedule in upcoming_due:
        user = schedule.order.user
        email = user.email

        # Send email
        send_email(
            to=email,
            subject="Installment Due Reminder",
            html_body=f"<p>Hello {user.first_name}, your next installment of {schedule.amount_due} is due on {schedule.due_date}</p>"
        )

        # Log reminder
        db.add(ReminderLog(schedule_id=schedule.id))
        db.commit()

    db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_due_reminders, trigger="cron", hour=8)  # every day at 8AM
    scheduler.start()
