from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from cruds.user import create_user, get_user, get_users, update_user, delete_user
from cruds.auth import authenticate_user, get_token, hash_password, get_token_data, get_token_from_header
from schemas.user import UserCreate, UserUpdate, User, UserNotPassword
from typing import List

router = APIRouter()

# Get User by ID
@router.get("/{user_id}", response_model=UserNotPassword)
def read_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

# Get all Users
@router.get("/", response_model=List[UserNotPassword])
def read_users_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)

# Update User
@router.put("/{user_id}", response_model=UserNotPassword)
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    
    db_user = update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

# Delete User
@router.delete("/{user_id}", response_model=UserNotPassword)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_user = delete_user(db=db, user_id=user_id)
    return db_user