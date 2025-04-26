from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, EmailStr

from db import Base


class ContactBook(Base):
    __tablename__ = "contact_book"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    country_name = Column(String)
    phone_number = Column(String)
    address = Column(String)


class ContactBookRegisterSchemma(BaseModel):
    name: str
    country_name: str
    phone_number: str
    address: str


class ContactBookUpdatesSchemma(ContactBookRegisterSchemma):
    pass
