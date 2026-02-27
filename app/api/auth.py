from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.schemas.auth import Token
from app.core.dependencies import get_db
from app.services.auth_service import register_user
from app.core.security import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth"), tags = ["auth"]


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user.email, user.password)


@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400)

    access = create_access_token({"sub": db.user_email})
    refresh = create_refresh_token({"sub": db.user_email})
    return {"access_token": access, "refresh_token": refresh}
