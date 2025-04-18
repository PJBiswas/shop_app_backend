from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.auth import RegisterRequest, RegisterResponse, VerifyOtpRequest, VerifyOtpResponse, \
    ResetPasswordRequest, TokenResponse, LoginRequest
from app.services.auth_service import register_user, verify_otp_and_activate, reset_password, login_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=RegisterResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = register_user(data, db)
        return {"message": "OTP sent to your email", "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/verify-otp", response_model=VerifyOtpResponse)
def verify_otp(data: VerifyOtpRequest, db: Session = Depends(get_db)):
    try:
        return verify_otp_and_activate(data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reset-password")
def reset_password_endpoint(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        return reset_password(data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        return login_user(data, db)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name
    }
