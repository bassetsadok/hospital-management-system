from pydantic import BaseModel, EmailStr


class Appointement_create(BaseModel):
    date:str
    time:str
    patient_id:int
    doctor_id:int
    
class Appointement_dto(Appointement_create):

    id:int
    class Config: 
        orm_mode=True

