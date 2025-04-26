from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, EmailStr
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)


class UserRegisterSchemma(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLoginSchemma(BaseModel):
    email: EmailStr
    password: str
