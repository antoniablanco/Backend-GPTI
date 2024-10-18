from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from schemas.coordinate import Coordinate, CoordinateUpdate


# Schema Answer
class Answer(BaseModel):
    answer: str
    latitude: float
    longitude: float
    name: str

# Schema Query
class QueryBase(BaseModel):
    travel_type: Optional[str] = None
    budget: Optional[int] = None
    destination: Optional[str] = None
    weather: Optional[str] = None
    duration: Optional[int] = None

# Schema for creating a new Query
class QueryCreate(QueryBase):
    time_stamp: datetime
    user_id: int
    ia_answer: Optional[str] = None

# Schema for updating a Query 
class QueryUpdate(QueryBase):
    pass

# Schema for getting a Query 
class Query(QueryBase):
    id: int
    user_id: int
    time_stamp: datetime
    ia_answer: Optional[str] = None
    coordinates: List[Coordinate] = []
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
