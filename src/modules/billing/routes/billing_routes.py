from typing import List
from fastapi import APIRouter, Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.modules.billing.schemas.billing_schemas import Billing_create, Billing_dto
from src.db.database import get_db
from src.auth.token_schemas import Token
from src.auth.oauth2 import create_access_token
from src.modules.billing.models.billing import Billing
from src.utilities import utils
router= APIRouter(tags=["billing"])

@router.get("/",response_model=List[Billing_dto])
async def get_billings(db: Session = Depends(get_db)):

    billings=db.query(Billing).all()
    return billings

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=Billing_dto)
def create_billing(billing:Billing_create,db: Session = Depends(get_db)):

    new_billing=Billing(**billing.dict())
    db.add(new_billing)
    db.commit()
    db.refresh(new_billing)

    return new_billing

@router.get('/{id}',response_model=Billing_dto)
def get_billing(id:int,db: Session = Depends(get_db)):
    billing = db.query(Billing).filter(Billing.id == id ).first()
    if not billing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Billing with id: {id} does not exist")
    
    return billing

@router.put("/{id}",response_model=Billing_dto)
async def update_billing(id:int,billing_payload:Billing_create,db: Session = Depends(get_db)):
    
    billing_query= db.query(Billing).filter(Billing.id == id)
    billing=billing_query.first()

    if billing== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"billing {id} was not found")
    
    billing_query.update(billing_payload.dict(),synchronize_session=False)
    db.commit()

    return billing_query.first()

@router.delete("/{id}")
async def delete_billing(id:int,db: Session = Depends(get_db)):

    billing_query=db.query(Billing).filter(Billing.id==id)
    billing=billing_query.first()

    if billing == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Billing {id} was not found")
    
    billing_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
