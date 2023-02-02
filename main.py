from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from src.db import  database
import os
from dotenv import load_dotenv

from src.modules.appointement.models import appointement
from src.modules.billing.models import billing
from src.modules.doctor.models import doctor
from src.modules.patient.models import patient

from src.modules.appointement.routes import appointement_routes
from src.modules.doctor.routes import doctor_routes
from src.modules.billing.routes import billing_routes
from src.modules.patient.routes import patient_routes

load_dotenv()  

appointement.Base.metadata.create_all(bind=database.engine)
billing.Base.metadata.create_all(bind=database.engine)
doctor.Base.metadata.create_all(bind=database.engine)
patient.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

while True:
    try:
        conn=psycopg2.connect(host=os.getenv("HOST"),database=os.getenv("DATABASE"),user=os.getenv("USER"),password=os.getenv("PASSWORD"),cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("database connection was successfull ✅")
        break
    except Exception as error:
        print("connection to database was failed")
        print("error was ",error)
        time.sleep(3)

app.include_router(patient_routes.router)
app.include_router(billing_routes.router)
app.include_router(doctor_routes.router)
app.include_router(appointement_routes.router)

@app.get("/")
async def root():
    print(os.getenv("DOMAIN"))
    return {"message":"hello basset" }
