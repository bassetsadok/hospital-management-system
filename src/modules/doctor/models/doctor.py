from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,Float, String, text
from sqlalchemy.orm import relationship

from src.db.database import Base

class Doctor(Base):
    __tablename__ = 'doctors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    specialty = Column(String(50), nullable=False)
    schedule = Column(String(100), nullable=False)
    
    appointments = relationship("Appointment", back_populates="doctor")
