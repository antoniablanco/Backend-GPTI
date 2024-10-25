from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from cruds.medal_table import create_medal_table, get_medal_table, get_medal_tables, update_medal_table, delete_medal_table, get_medal_table_by_user_id
from cruds.auth import authenticate_user, get_token, hash_password, get_token_data, get_token_from_header
from cruds.user import get_user
from schemas.medal_table import MedalTableCreate, MedalTableUpdate, MedalTable
from typing import List

router = APIRouter()

# Update MedalTable for authenticated user
@router.post("/update", response_model=MedalTable)
def update_medal_table_endpoint(medal_table: MedalTableUpdate, db: Session = Depends(get_db), token: str = Depends(get_token_from_header)):
    token_data = get_token_data(token=token, db=db)
    user_db = get_user(db, user_id=token_data.user_id)
    db_medal = get_medal_table_by_user_id(db, user_id=user_db.id)

    if db_medal is None:
        raise HTTPException(status_code=404, detail="Medallero no encontrada")

    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario del token no encontrado")


    db_medal_table = update_medal_table(db=db, medal_table_id=db_medal.id, medal_table=medal_table)
    if db_medal_table is None:
        raise HTTPException(status_code=404, detail="Medallero no encontrado")
    return db_medal_table

# Create basic MedalTable for other user
@router.post("/basic/{user_id}", response_model=MedalTable)
def create_basic_medal_table_endpoint(user_id: int, db: Session = Depends(get_db), token: str = Depends(get_token_from_header)):
    token_data = get_token_data(token=token, db=db)
    user_db = get_user(db, user_id=token_data.user_id)
    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario del token no encontrado")
    other_user = get_user(db, user_id=user_id)
    if other_user is None:
        raise HTTPException(status_code=404, detail=f"Usuario {user_id} no encontrado")
    exist_medal_table = get_medal_table_by_user_id(db, user_id=other_user.id)
    if exist_medal_table is not None:
        raise HTTPException(status_code=400, detail=f"Usuario {other_user.id} ya posee un medallero")
    try:
        medal_table_info = MedalTableCreate(user_id=user_id, africa=False, americas=False, asia=False, europe=False, oceania=False, antartica=False)
        return create_medal_table(db=db, medal_table=medal_table_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear medallero: {e}")

# Create MedalTable for authenticated user
@router.post("/", response_model=MedalTable)
def create_medal_table_endpoint(medal_table: MedalTableUpdate, db: Session = Depends(get_db), token: str = Depends(get_token_from_header)):
    token_data = get_token_data(token=token, db=db)
    user_db = get_user(db, user_id=token_data.user_id)
    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario del token no encontrado")
    exist_medal_table = get_medal_table_by_user_id(db, user_id=user_db.id)
    if exist_medal_table is not None:
        raise HTTPException(status_code=400, detail=f"Usuario {user_db.id} ya posee un medallero")
    try:
        medal_table_info = MedalTableCreate(user_id=user_db.id, africa=medal_table.africa, americas=medal_table.americas, asia=medal_table.asia, europe=medal_table.europe, oceania=medal_table.oceania, antartica=medal_table.antartica)
        return create_medal_table(db=db, medal_table=medal_table_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear medallero: {e}")

# Get MedalTable of authenticated user
@router.get("/my_medal_table", response_model=MedalTable)
def read_my_medal_table_endpoint(token: str = Depends(get_token_from_header), db: Session = Depends(get_db)):
    token_data = get_token_data(token=token, db=db)
    user_db = get_user(db, user_id=token_data.user_id)
    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario del token no encontrado")
    
    db_medal_table = get_medal_table_by_user_id(db, user_id=user_db.id)

    if db_medal_table is None:
        raise HTTPException(status_code=404, detail="Medallero no encontrado")
    return db_medal_table

# Get MedalTable by ID
@router.get("/{medal_table_id}", response_model=MedalTable)
def read_medal_table_endpoint(medal_table_id: int, db: Session = Depends(get_db)):
    db_medal_table = get_medal_table(db, medal_table_id=medal_table_id)
    if db_medal_table is None:
        raise HTTPException(status_code=404, detail="Medallero no encontrado")
    return db_medal_table

# Get MedalTables
@router.get("/", response_model=List[MedalTable])
def read_medal_tables_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    medal_tables = get_medal_tables(db, skip=skip, limit=limit)
    return medal_tables

# Update MedalTable
@router.put("/{medal_table_id}", response_model=MedalTable)
def update_medal_table_endpoint(medal_table_id: int, medal_table: MedalTableUpdate, db: Session = Depends(get_db), token: str = Depends(get_token_from_header)):
    token_data = get_token_data(token=token, db=db)
    user_db = get_user(db, user_id=token_data.user_id)
    db_medal = get_medal_table(db, medal_table_id=medal_table_id)

    if db_medal is None:
        raise HTTPException(status_code=404, detail="Medalla no encontrada")

    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario del token no encontrado")
    
    if user_db.id != db_medal.user_id:
        raise HTTPException(status_code=403, detail="Solo puedes modificar tus propias medallas")

    db_medal_table = update_medal_table(db=db, medal_table_id=medal_table_id, medal_table=medal_table)
    if db_medal_table is None:
        raise HTTPException(status_code=404, detail="Medallero no encontrado")
    return db_medal_table

# Delete MedalTable
@router.delete("/{medal_table_id}", response_model=MedalTable)
def delete_medal_table_endpoint(medal_table_id: int, db: Session = Depends(get_db), token: str = Depends(get_token_from_header)):
    token_data = get_token_data(token=token, db=db)
    user_db = get_user(db, user_id=token_data.user_id)
    db_medal = get_medal_table(db, medal_table_id=medal_table_id)

    if db_medal is None:
        raise HTTPException(status_code=404, detail="Medallero no encontrada")

    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario del token no encontrado")
    
    if user_db.id != db_medal.user_id:
        raise HTTPException(status_code=403, detail="Solo puedes eliminar tus propias medallas")

    db_medal_table = get_medal_table(db, medal_table_id=medal_table_id)
    if db_medal_table is None:
        raise HTTPException(status_code=404, detail="Medallero no encontrado")
    db_medal_table = delete_medal_table(db=db, medal_table_id=medal_table_id)
    return db_medal_table