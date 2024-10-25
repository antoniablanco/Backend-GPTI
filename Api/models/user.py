from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Enum
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)

    queries = relationship("Query", back_populates="user", cascade="all, delete-orphan")
    medal_tables = relationship("MedalTable", back_populates="user", cascade="all, delete-orphan")