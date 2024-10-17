from pydantic import BaseModel, IPvAnyAddress
from typing import Optional, List

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

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
