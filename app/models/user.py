from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer , String 
from app.database import Base

# database table model
class User(Base):
   __tablename__="users"

   id= Column(Integer, primary_key=True, index=True)
   email= Column(String, unique=True, index=True)
   hashed_password= Column(String)

#What we receive when user registers
class UserRegister(BaseModel):
    email: EmailStr
    password: str

#What we recieve when user logs in 
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#what we send back aftrer successful login    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str="bearer"
