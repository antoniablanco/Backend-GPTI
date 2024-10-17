from sqlalchemy.orm import Session
from models.user import User as UserModel
from schemas.user import UserCreate, UserUpdate

# Create a new user
def create_user(db: Session, user: UserCreate):
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Retrieve a user by ID
def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

# Retrieve a user by username
def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()

# Retrieve all users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()

# Update an existing user
def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

# Delete a user
def delete_user(db: Session, user_id: int):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user