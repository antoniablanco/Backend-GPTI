from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Query(Base):
    __tablename__ = "queries"
    id = Column(Integer, primary_key=True, index=True)
    time_stamp = Column(DateTime(timezone=True), index=True)
    travel_type = Column(String(100), index=True)
    budget = Column(Integer, index=True) # in dollars
    destination = Column(String(100), index=True)
    weather = Column(String(100), index=True)
    duration = Column(Integer, index=True) # in days
    ia_answer = Column(String(500), index=True) 
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="queries")

    coordinates = relationship("Coordinate", back_populates="query", cascade="all, delete-orphan")

