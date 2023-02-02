from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,Float, String, text,DateTime
from sqlalchemy.orm import relationship

from src.db.database import Base

class Billing(Base):
    __tablename__ = 'billing'
    
    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    date = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    
    patient = relationship("Patient", back_populates="billing")
