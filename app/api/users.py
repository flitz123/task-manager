from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schema.auth import LoginRequest
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.api.deps import get_current_user

router = APIRouter()

# REGISTER USER


@router.post("/register", status_code=201)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered", )

    new_user = User(email=user_in.email, hashed_password=hash_password(
        user_in.password), role="user", )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# LOGIN USER


@router.post("/login", response_model=Token)
def login_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", )

    token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role,
        }
    )

    return {"access_token": token, "token_type": "bearer"}

# GET CURRENT USER


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

# LIST ALL USERS (ADMIN ONLY)


@router.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), ):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Admin access required", )

    users = db.query(User).all()
    return users
