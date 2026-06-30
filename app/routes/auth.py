from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import UserRegister, UserLogin, TokenResponse
from app.services.auth import register_user, login_user
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    result = register_user(db, user.email, user.password)
    return result

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    result = login_user(db, user.email, user.password)
    return result