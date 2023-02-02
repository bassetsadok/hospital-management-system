from pydantic import BaseModel, EmailStr


class Doctor_create(BaseModel):
    name:str
    specialty:str
    schedule:str
    
class Doctor_dto(Doctor_create):

    id:int
    class Config: 
        orm_mode=True

