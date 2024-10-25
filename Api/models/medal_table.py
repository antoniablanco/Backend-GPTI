from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base

class MedalTable(Base):
    __tablename__ = "medal_tables"
    id = Column(Integer, primary_key=True, index=True)
    africa = Column(Boolean, index=True)
    americas = Column(Boolean, index=True)
    asia = Column(Boolean, index=True)
    europe = Column(Boolean, index=True)
    oceania = Column(Boolean, index=True)
    antartica = Column(Boolean, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), index=True, unique=True)
    user = relationship("User", back_populates="medal_tables")