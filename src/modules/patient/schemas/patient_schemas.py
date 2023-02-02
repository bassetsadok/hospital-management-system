from pydantic import BaseModel, EmailStr


class Patient_create(BaseModel):
    name:str
    address:str
    date_of_birth:str
    medical_history:str
    
class Patient_dto(Patient_create):

    id:int
    class Config: 
        orm_mode=True

