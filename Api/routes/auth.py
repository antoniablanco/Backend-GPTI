from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import get_db

from schemas.user import UserUpdate, User
from schemas.authentication import UserLogin, TokenData
from cruds.auth import authenticate_user, get_token, hash_password, get_token_data
from cruds.user import create_user

from dotenv import load_dotenv
import os


router = APIRouter()

@router.post("/signup", response_model=dict)
def sign_up(user: UserUpdate, db: Session = Depends(get_db)):
    if user.username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    elif user.password is None:
        raise HTTPException(status_code=400, detail="Password is required")

    user.password = hash_password(user.password)
    try:
        create_user(db=db, user=user)
        access_token = get_token(user, db)
        return {"message": "Login successful", "token": access_token, "token_type": "bearer"}
    
    except IntegrityError as e:
        db.rollback()  
        error_str = str(e.orig)
        if 'unique constraint' in error_str.lower():
            if 'username' in error_str.lower():
                raise HTTPException(status_code=400, detail="Username already exists")
        raise HTTPException(status_code=400, detail="Database integrity error")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred {e}")

@router.post("/login", response_model=dict)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user)
    if db_user:
        access_token = get_token(user, db)
        return {"message": "Login successful", "token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )