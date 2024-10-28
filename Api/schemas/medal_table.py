from pydantic import BaseModel
from typing import Optional, List

# Schema MedalTable
class MedalTableBase(BaseModel):
    africa: Optional[bool] = False
    north_america: Optional[bool] = False
    south_america: Optional[bool] = False
    asia: Optional[bool] = False
    europe: Optional[bool] = False
    oceania : Optional[bool] = False
    antartica: Optional[bool] = False

class MedalTableCreate(MedalTableBase):
    user_id: int

class MedalTableUpdate(MedalTableBase):
    pass

class MedalTable(MedalTableBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True