from pydantic import BaseModel, EmailStr


class Billing_create(BaseModel):
    amount:int
    patient_id:int
    
class Billing_dto(Billing_create):

    id:int
    class Config: 
        orm_mode=True

