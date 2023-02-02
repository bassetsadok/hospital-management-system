from typing import List
from fastapi import APIRouter, Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from src.modules.appointement.models.appointement import Appointment
from src.modules.appointement.schemas.appointement_schemas import Appointement_create, Appointement_dto
from src.db.database import get_db
from src.auth.token_schemas import Token
from src.auth.oauth2 import create_access_token
from src.utilities import utils
router= APIRouter(tags=["appointement"])

@router.get("/",response_model=List[Appointement_dto])
async def get_appointements(db: Session = Depends(get_db)):

    appointements=db.query(Appointment).all()
    return appointements

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=Appointement_dto)
def create_appointement(appointement:Appointement_create,db: Session = Depends(get_db)):

    new_appointement=Appointment(**appointement.dict())
    db.add(new_appointement)
    db.commit()
    db.refresh(new_appointement)

    return new_appointement

@router.get('/{id}',response_model=Appointement_dto)
def get_appointement(id:int,db: Session = Depends(get_db)):
    appointement = db.query(Appointment).filter(Appointment.id == id ).first()
    if not appointement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Appointement with id: {id} does not exist")
    
    return appointement

@router.put("/{id}",response_model=Appointement_dto)
async def update_appointement(id:int,appointement_payload:Appointement_create,db: Session = Depends(get_db)):
    
    appointement_query= db.query(Appointment).filter(Appointment.id == id)
    appointement=appointement_query.first()

    if appointement== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Appointement {id} was not found")
    
    appointement_query.update(appointement_payload.dict(),synchronize_session=False)
    db.commit()

    return appointement_query.first()


@router.delete("/{id}")
async def delete_appointement(id:int,db: Session = Depends(get_db)):

    appointement_query=db.query(Appointment).filter(Appointment.id==id)
    appointement=appointement_query.first()

    if appointement == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Appointement {id} was not found")
    
    appointement_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
