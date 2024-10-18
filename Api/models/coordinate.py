from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Enum, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base

class Coordinate(Base):
    __tablename__ = "coordinates"
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    name = Column(String(100), index=True)

    query_id = Column(Integer, ForeignKey("queries.id"))
    query = relationship("Query", back_populates="coordinates")
