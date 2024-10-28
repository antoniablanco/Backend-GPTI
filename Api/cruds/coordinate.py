from sqlalchemy.orm import Session
from models.coordinate import Coordinate as CoordinateModel
from schemas.coordinate import CoordinateCreate, CoordinateUpdate

# Create a new coordinate
def create_coordinate(db: Session, coordinate: CoordinateCreate):
    db_coordinate = CoordinateModel(**coordinate.dict())
    db.add(db_coordinate)
    db.commit()
    db.refresh(db_coordinate)
    return db_coordinate

# Retrieve a coordinate by ID
def get_coordinate(db: Session, coordinate_id: int):
    return db.query(CoordinateModel).filter(CoordinateModel.id == coordinate_id).first()

# Retrieve all coordinates
def get_coordinates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CoordinateModel).offset(skip).limit(limit).all()

# Update an existing coordinate
def update_coordinate(db: Session, coordinate_id: int, coordinate: CoordinateUpdate):
    db_coordinate = db.query(CoordinateModel).filter(CoordinateModel.id == coordinate_id).first()
    if db_coordinate:
        for key, value in coordinate.dict(exclude_unset=True).items():
            setattr(db_coordinate, key, value)
        db.commit()
        db.refresh(db_coordinate)
    return db_coordinate

# Delete a coordinate
def delete_coordinate(db: Session, coordinate_id: int):
    db_coordinate = db.query(CoordinateModel).filter(CoordinateModel.id == coordinate_id).first()
    if db_coordinate:
        db.delete(db_coordinate)
        db.commit()
    return db_coordinate