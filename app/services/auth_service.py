import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.email_utils import send_otp_email, send_password_reset_email
from app.core.security import get_password_hash, generate_random_password, verify_password, create_access_token
from app.models.otp_verification import OTPVerification
from app.models.password_reset import PasswordResetToken
from app.models.user import User
from app.schemas.auth import RegisterRequest, VerifyOtpRequest, ResetPasswordRequest, LoginRequest


def register_user(data: RegisterRequest, db: Session):
    # Check for duplicate email
    if db.query(User).filter(User.email == data.email).first():
        raise ValueError("Email already exists")

    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        phone=data.phone,
        email=data.email,
        password="",
        is_verified=False,
        user_type=data.user_type or "customer"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate and store OTP
    otp = str(random.randint(100000, 999999))
    db.add(OTPVerification(user_id=user.id, otp=otp))
    db.commit()

    send_otp_email(user.email, otp)
    return user


def verify_otp_and_activate(data: VerifyOtpRequest, db: Session):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise ValueError("User not found")
    if user.is_verified:
        raise ValueError("User already verified")

    # Get latest OTP entry
    otp_record = db.query(OTPVerification) \
        .filter(OTPVerification.user_id == user.id) \
        .order_by(OTPVerification.created_at.desc()) \
        .first()

    if not otp_record or otp_record.otp != data.otp:
        raise ValueError("Invalid or expired OTP")

    user.is_verified = True
    user.password = get_password_hash(generate_random_password())
    db.commit()

    # Generate password reset token
    reset_token = generate_random_password(32)
    db.add(PasswordResetToken(user_id=user.id, token=reset_token))
    db.commit()

    send_password_reset_email(user.email, reset_token)
    return {"message": "OTP verified. Please reset your password from your email."}


def reset_password(data: ResetPasswordRequest, db: Session):
    token_record = db.query(PasswordResetToken) \
        .filter(PasswordResetToken.token == data.token) \
        .order_by(PasswordResetToken.created_at.desc()) \
        .first()

    if not token_record:
        raise ValueError("Invalid or expired reset token")

    # Optional: token expiration check
    if token_record.created_at < datetime.utcnow() - timedelta(hours=1):
        raise ValueError("Reset token expired")

    user = token_record.user
    user.password = get_password_hash(data.new_password)
    db.commit()

    # Clean up all old reset tokens for security
    db.query(PasswordResetToken).filter(PasswordResetToken.user_id == user.id).delete()
    db.commit()

    return {"message": "Password updated successfully. You can now log in."}


def login_user(data: LoginRequest, db: Session):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not user.is_verified:
        raise ValueError("Invalid credentials or unverified user")

    if not verify_password(data.password, user.password):
        raise ValueError("Invalid credentials")
    token_data = {
        "sub": user.email,
        "user_type": user.user_type
    }
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer", "user_type": user.user_type}
