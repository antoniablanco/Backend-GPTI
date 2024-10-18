from sqlalchemy.orm import Session
from models.query import Query as QueryModel
from schemas.query import QueryCreate, QueryUpdate

# Create a new query
def create_query(db: Session, query: QueryCreate):
    db_query = QueryModel(**query.dict())
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query

# Retrieve a query by ID
def get_query(db: Session, query_id: int):
    return db.query(QueryModel).filter(QueryModel.id == query_id).first()

# Retrieve a query by user_id
def get_queries_by_user_id(db: Session, user_id: int):
    return db.query(QueryModel).filter(QueryModel.user_id == user_id).all()

# Retrieve all querys
def get_queries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(QueryModel).offset(skip).limit(limit).all()

# Update an existing query
def update_query(db: Session, query_id: int, query: QueryUpdate):
    db_query = db.query(QueryModel).filter(QueryModel.id == query_id).first()
    if db_query:
        for key, value in query.dict(exclude_unset=True).items():
            setattr(db_query, key, value)
        db.commit()
        db.refresh(db_query)
    return db_query

# Delete a query
def delete_query(db: Session, query_id: int):
    db_query = db.query(QueryModel).filter(QueryModel.id == query_id).first()
    if db_query:
        db.delete(db_query)
        db.commit()
    return db_query