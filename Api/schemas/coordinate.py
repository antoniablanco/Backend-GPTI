from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schema Grade
class Grade(BaseModel): 
    coordinate_id: int
    stars: int

# Schema Coordinate
class CoordinateBase(BaseModel):
    latitude: float
    longitude: float
    answer: Optional[str] = None

class CoordinateCreate(CoordinateBase):
    name: Optional[str] = None
    query_id: int

class CoordinateUpdate(CoordinateBase):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    name: Optional[str] = None
    stars: Optional[int] = None

class Coordinate(CoordinateBase):
    id: int
    name: Optional[str] = None
    query_id: int
    stars: Optional[int] = None
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True