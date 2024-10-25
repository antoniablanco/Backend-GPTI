from pydantic import BaseModel
from typing import Optional, List
from schemas.query import Query
from schemas.medal_table import MedalTable

# Schema user interests
class UserInterests(BaseModel):
    interests: str
    
# Schema User
class UserBase(BaseModel):
    pass

# Schema for creating a new User
class UserCreate(UserBase):
    username: str
    password: str

# Schema for updating a User 
class UserUpdate(UserBase):
    username: Optional[str] = None
    password: Optional[str] = None

# Schema for getting a User without password
class UserNotPassword(UserBase):
    id: int
    username: str
    queries: List[Query] = []
    medal_tables: List[MedalTable] = []

# Schema for getting a User without password
class User(UserBase):
    id: int
    username: str
    password: str
    queries: List[Query] = []
    medal_tables: List[MedalTable] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
