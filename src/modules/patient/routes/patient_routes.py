from typing import List
from fastapi import APIRouter, Depends,status,HTTPException,Response
from sqlalchemy.orm import Session

from src.modules.patient.models.patient import Patient
from src.modules.patient.schemas.patient_schemas import Patient_create,Patient_dto
from src.db.database import get_db
from src.auth.token_schemas import Token
from src.auth.oauth2 import create_access_token
from src.utilities import utils
router= APIRouter(tags=["patient"])

@router.get("/",response_model=List[Patient_dto])
async def get_patients(db: Session = Depends(get_db)):

    patients=db.query(Patient).all()
    return patients

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=Patient_dto)
def create_patient(patient:Patient_create,db: Session = Depends(get_db)):

    new_patient=Patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient

@router.get('/{id}',response_model=Patient_dto)
def get_patient(id:int,db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == id ).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with id: {id} does not exist")
    
    return patient

@router.put("/{id}",response_model=Patient_dto)
async def update_patient(id:int,patient_payload:Patient_create,db: Session = Depends(get_db)):
    
    patient_query= db.query(Patient).filter(Patient.id == id)
    patient=patient_query.first()

    if patient== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"patient {id} was not found")
    
    patient_query.update(patient_payload.dict(),synchronize_session=False)
    db.commit()

    return patient_query.first()


@router.delete("/{id}")
async def delete_patient(id:int,db: Session = Depends(get_db)):

    patient_query=db.query(Patient).filter(Patient.id==id)
    patient=patient_query.first()

    if patient == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Patient {id} was not found")
    
    patient_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
