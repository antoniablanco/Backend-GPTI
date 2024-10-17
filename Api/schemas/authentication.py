from pydantic import BaseModel, IPvAnyAddress
from typing import Optional, List

# Schema por user login 
class UserLogin(BaseModel):
    username: str
    password: str

# Schema por token data
class TokenData(BaseModel):
    user_id: int