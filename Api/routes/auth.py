from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import get_db

from schemas.user import UserUpdate, User
from schemas.authentication import UserLogin, TokenData
from cruds.auth import authenticate_user, get_token, hash_password, get_token_data, get_token_from_header
from cruds.user import create_user

from dotenv import load_dotenv
import os


router = APIRouter()

@router.post("/signup", response_model=dict)
def sign_up(user: UserUpdate, db: Session = Depends(get_db)):
    if user.username is None:
        raise HTTPException(status_code=400, detail="El nombre de usuario es requerido")
    elif user.password is None:
        raise HTTPException(status_code=400, detail="La clave es requerida")

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
                raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ha ocurrido un error no esperado: {e}")

@router.post("/login", response_model=dict)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user)
    if db_user:
        access_token = get_token(user, db)
        return {"message": "Login successful", "token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o clave incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.get("/active_token", response_model=dict)
def active_token(db: Session = Depends(get_db), token: str = Depends(get_token_from_header)):
    token_data = get_token_data(token=token, db=db)
    if token_data:
        return {"message": "Token is active", "token_data": token_data}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La token es invalida",
            headers={"WWW-Authenticate": "Bearer"}
        )