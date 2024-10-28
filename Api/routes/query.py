from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from cruds.query import create_query, get_query, get_queries, update_query, delete_query, get_queries_by_user_id
from cruds.coordinate import update_coordinate, get_coordinate, get_coordinates, create_coordinate, delete_coordinate
from cruds.auth import authenticate_user, get_token, hash_password, get_token_data, get_token_from_header
from cruds.user import get_user
from schemas.query import QueryCreate, QueryUpdate, Query
from schemas.coordinate import CoordinateCreate, CoordinateUpdate, Coordinate, Grade
from typing import List
from datetime import datetime

router = APIRouter()

# Grade a coordinate of a query
@router.post("/grade_coordinate", response_model=Coordinate)
def grade_coordinate_endpoint(grade: Grade, db: Session = Depends(get_db), token: str = Depends(get_token_from_header)):
    token_data = get_token_data(token=token, db=db)
    user_db = get_user(db, user_id=token_data.user_id)
    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db_coordinate = get_coordinate(db, coordinate_id=grade.coordinate_id)

    if db_coordinate is None:
        raise HTTPException(status_code=404, detail="Coordenada no encontrada")
    
    if grade.stars < 0 or grade.stars > 5:
        raise HTTPException(status_code=400, detail="La calificación debe ser un número entre 0 y 5")
    
    return update_coordinate(db=db, coordinate_id=grade.coordinate_id, coordinate=CoordinateUpdate(stars=grade.stars))
    

# Get all Querys
@router.get("/all", response_model=List[Query])
def read_querys_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_queries(db, skip=skip, limit=limit)

# Get Query by ID
@router.get("/{query_id}", response_model=Query)
def read_query_endpoint(query_id: int, db: Session = Depends(get_db), token: str = Depends(get_token_from_header)):
    db_query = get_query(db, query_id=query_id)
    if db_query is None:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    
    token_data = get_token_data(token=token, db=db)
    user_db = get_user(db, user_id=token_data.user_id)
    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user_db.id != db_query.user_id:
        raise HTTPException(status_code=404, detail="Solo puedes ver tus propias consultas")


    return db_query

# Get all Querys of the user
@router.get("/", response_model=List[Query])
def read_querys_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: str = Depends(get_token_from_header)):
    token_data = get_token_data(token=token, db=db)
    user_db = get_user(db, user_id=token_data.user_id)
    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return get_queries_by_user_id(db, user_id=user_db.id)

# Update Query
@router.put("/{query_id}", response_model=Query)
def update_query_endpoint(query_id: int, query: QueryUpdate, db: Session = Depends(get_db), token: str = Depends(get_token_from_header)):
    token_data = get_token_data(token=token, db=db)
    user_db = get_user(db, user_id=token_data.user_id)
    db_query = get_query(db, query_id=query_id)

    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user_db.id != db_query.user_id:
        raise HTTPException(status_code=404, detail="Solo puedes actualizar tus propias consultas")

    db_query = update_query(db=db, query_id=query_id, query=query)
    if db_query is None:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    return db_query

# Delete Query
@router.delete("/{query_id}", response_model=Query)
def delete_query_endpoint(query_id: int, db: Session = Depends(get_db), token: str = Depends(get_token_from_header)):
    token_data = get_token_data(token=token, db=db)
    user_db = get_user(db, user_id=token_data.user_id)
    db_query = get_query(db, query_id=query_id)

    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user_db.id != db_query.user_id:
        raise HTTPException(status_code=404, detail="Solo puedes eliminar tus propias consultas")


    if db_query is None:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    db_query = delete_query(db=db, query_id=query_id)
    return db_query