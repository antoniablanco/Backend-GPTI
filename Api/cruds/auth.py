from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Header
from database import get_db
from cruds.user import get_user_by_username, create_user

from schemas.authentication import UserLogin, TokenData

from datetime import datetime, timedelta
from typing import Optional
import jwt
import bcrypt

from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 600))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, user: UserLogin):
    user_db = get_user_by_username(db, user.username)
    if not user_db or not verify_password(user.password, user_db.password):
        return False
    return user_db

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt() 
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def get_token(user: UserLogin, db: Session = Depends(get_db)):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_username": user.username}, 
        expires_delta=access_token_expires
    )

    return access_token

def get_token_data(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_username: str = payload.get("user_username")
        if user_username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = get_user_by_username(db, user_username)
        return TokenData(user_id=user.id)
    except jwt.PyJWTError as e:
        print("jst.PyJWTError", e)  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_token_from_header(authorization: Optional[str] = Header(None)) -> str:
    if authorization:
        token = authorization.split(" ")[1]
        return token
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")