import os
import smtplib
from email.mime.text import MIMEText

from jinja2 import Template
from pydantic import EmailStr


def send_otp_email(email: EmailStr, otp: str):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    subject = "Your OTP Code"
    with open("app/core/templates/otp_email.html") as f:
        html_template = Template(f.read())
        html_body = html_template.render(otp=otp)

    msg = MIMEText(html_body, "html")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = email

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, email, msg.as_string())


def send_password_reset_email(email: EmailStr, reset_token: str):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    subject = "Set Your Password"
    with open("app/core/templates/reset_password.html") as f:
        html_template = Template(f.read())
        reset_url = f"http://localhost:3000/reset-password?token={reset_token}"  # customize your frontend
        html_body = html_template.render(reset_url=reset_url)

    msg = MIMEText(html_body, "html")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = email

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, email, msg.as_string())


def send_email(to: str, subject: str, html_body: str):
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")  # your email
    smtp_pass = os.getenv("SMTP_PASS")  # app password

    msg = MIMEText(html_body, "html")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to, msg.as_string())
