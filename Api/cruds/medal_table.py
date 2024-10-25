from sqlalchemy.orm import Session
from models.medal_table import MedalTable as MedalTableModel
from schemas.medal_table import MedalTableCreate, MedalTableUpdate

# Create a new medal_tables for a user
def create_medal_table(db: Session, medal_table: MedalTableCreate):
    db_medal_table = MedalTableModel(**medal_table.dict())
    db.add(db_medal_table)
    db.commit()
    db.refresh(db_medal_table)
    return db_medal_table

# Retrieve a medal_table by ID
def get_medal_table(db: Session, medal_table_id: int):
    return db.query(MedalTableModel).filter(MedalTableModel.id == medal_table_id).first()

# Retrieve all medal_tables by the user_id at who the medal_table is aimed
def get_medal_table_by_user_id(db: Session, user_id: str):
    return db.query(MedalTableModel).filter(MedalTableModel.user_id == user_id).first()

# Retrieve all medal_tables of all users
def get_medal_tables(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MedalTableModel).offset(skip).limit(limit).all()

# Update medal_tables from a user
def update_medal_table(db: Session, medal_table_id: int, medal_table: MedalTableUpdate):
    db_medal_table = db.query(MedalTableModel).filter(MedalTableModel.id == medal_table_id).first()
    if db_medal_table:
        for key, value in medal_table.dict(exclude_unset=True).items():
            setattr(db_medal_table, key, value)
        db.commit()
        db.refresh(db_medal_table)
    return db_medal_table

# Delete medal_tables from a user
def delete_medal_table(db: Session, medal_table_id: int):
    db_medal_table = db.query(MedalTableModel).filter(MedalTableModel.id == medal_table_id).first()
    if db_medal_table:
        db.delete(db_medal_table)
        db.commit()
    return db_medal_table