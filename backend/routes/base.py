from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine, get_db
from sqlalchemy.orm import Session
from models.users import User, UserRegisterSchemma, UserLoginSchemma
from models.contact_book import (
    ContactBook,
    ContactBookRegisterSchemma,
    ContactBookUpdatesSchemma,
    ContactBookPartialUpdateSchemma,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

@app.get("/")
async def index():
    return {"message": "ok", "title": "contactbook"}


@app.post("/register", tags=["Authentication"])
def register_user(form_data: UserRegisterSchemma, db: Session = Depends(get_db)):
    user = User(name=form_data.name, email=form_data.email, password=form_data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/login", tags=["Authentication"])
def login(form_data: UserLoginSchemma, db: Session = Depends(get_db)):
    exist = db.query(User).filter(User.email == str(form_data.email)).first()

    if exist is None:
        return {"message": "login fail: user not found"}

    if exist.password == form_data.password:
        return {"message": "ok", "user": exist}

    return {"message": "login fail invalid password"}


@app.post("/register-contact", tags=["Contact Book"])
def register_contact(
    form_data: ContactBookRegisterSchemma, db: Session = Depends(get_db)
):
    contactbook = ContactBook(
        name=form_data.name,
        country_name=form_data.country_name,
        phone_number=form_data.phone_number,
        address=form_data.address,
    )
    db.add(contactbook)
    db.commit()
    db.refresh(contactbook)
    return contactbook


@app.put("/update-contact/{id}", tags=["Contact Book"])
def update_contact(
    id: int, form_data: ContactBookUpdatesSchemma, db: Session = Depends(get_db)
):
    exist = db.query(ContactBook).filter(ContactBook.id == id).first()

    if exist is None:
        return {"message": "contact not found"}

    exist.name = form_data.name
    exist.country_name = form_data.country_name
    exist.phone_number = form_data.phone_number
    exist.address = form_data.address

    db.commit()
    return {"message": "updated successsfulluy"}


@app.patch("/update-contact/{id}", tags=["Contact Book"])
def partial_update_contact(
    id: int, form_data: ContactBookPartialUpdateSchemma, db: Session = Depends(get_db)
):
    exist = db.query(ContactBook).filter(ContactBook.id == id).first()

    if exist is None:
        return {"message": "contact not found"}

    if form_data.name:
        exist.name = form_data.name

    if form_data.country_name:
        exist.country_name = form_data.country_name

    if form_data.phone_number:
        exist.phone_number = form_data.phone_number

    if form_data.address:
        exist.address = form_data.address

    db.commit()
    return {"message": "updated successsfulluy"}


@app.delete("/delete-contact/{id}", tags=["Contact Book"])
def delete_contact(id: int, db: Session = Depends(get_db)):
    exist = db.query(ContactBook).filter(ContactBook.id == id).first()

    if exist is None:
        return {"message": "contact not found"}

    db.delete(exist)
    db.commit()

    return {"message": "deleted successsfulluy"}


@app.get("/get-contact/{id}", tags=["Contact Book"])
def get_contact(id: int, db: Session = Depends(get_db)):
    exist = db.query(ContactBook).filter(ContactBook.id == id).first()

    if exist is None:
        return {"message": "contact not found"}

    return {"message": "OK", "contact": exist}


@app.get("/get-contacts", tags=["Contact Book"])
def get_contacts(db: Session = Depends(get_db)):
    return db.query(ContactBook).all()
