from typing import List
from fastapi import APIRouter, Depends,status,HTTPException,Response
from sqlalchemy.orm import Session

from src.modules.doctor.schemas.doctor_schemas import Doctor_create, Doctor_dto
from src.db.database import get_db
from src.auth.token_schemas import Token
from src.auth.oauth2 import create_access_token
from src.modules.doctor.models.doctor import Doctor
from src.utilities import utils
router= APIRouter(tags=["doctor"])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=Doctor_dto)
def create_doctor(doctor:Doctor_create,db: Session = Depends(get_db)):

    new_doctor=Doctor(**doctor.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor

@router.get("/",response_model=List[Doctor_dto])
async def get_doctors(db: Session = Depends(get_db)):

    doctors=db.query(Doctor).all()
    return doctors

@router.get('/{id}',response_model=Doctor_dto)
def get_doctor(id:int,db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == id ).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Doctor with id: {id} does not exist")
    
    return doctor

@router.put("/{id}",response_model=Doctor_dto)
async def update_doctor(id:int,doctor_payload:Doctor_create,db: Session = Depends(get_db)):
    
    doctor_query= db.query(Doctor).filter(Doctor.id == id)
    doctor=doctor_query.first()

    if doctor== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"doctor {id} was not found")
    
    doctor_query.update(doctor_payload.dict(),synchronize_session=False)
    db.commit()

    return doctor_query.first()

@router.delete("/{id}")
async def delete_doctor(id:int,db: Session = Depends(get_db)):

    doctor_query=db.query(Doctor).filter(Doctor.id==id)
    doctor=doctor_query.first()

    if doctor == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Doctor {id} was not found")
    
    doctor_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
