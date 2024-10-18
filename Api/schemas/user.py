from pydantic import BaseModel
from typing import Optional, List
from schemas.query import Query

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

# Schema for getting a User without password
class User(UserBase):
    id: int
    username: str
    password: str
    queries: List[Query] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
