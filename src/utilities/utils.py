from fastapi import Depends
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from src.db.database import get_db,engine
from sqlalchemy.orm import Session
from sqlalchemy import insert,select

load_dotenv()  

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    #hash the password - password
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

