from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schema Coordinate
class CoordinateBase(BaseModel):
    latitude: float
    longitude: float

class CoordinateCreate(CoordinateBase):
    name: Optional[str] = None
    query_id: int

class CoordinateUpdate(CoordinateBase):
    name: Optional[str] = None

class Coordinate(CoordinateBase):
    name: Optional[str] = None
    query_id: int
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True