from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,Float, String, text,DateTime
from sqlalchemy.orm import relationship

from src.db.database import Base

class Patient(Base):
    __tablename__ = 'patients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    medical_history = Column(String(500), nullable=False)
    
    appointments = relationship("Appointment", back_populates="patient")
    billing = relationship("Billing", back_populates="patient")
