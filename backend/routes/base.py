from fastapi import FastAPI, Depends
from db import Base, engine, get_db
from sqlalchemy.orm import Session
from models.users import User

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "ok", "title": "contactbook"}


from pydantic import BaseModel, EmailStr


class UserRegisterSchemma(BaseModel):
    name: str
    email: EmailStr
    password: str


@app.post("/register")
def register_user(form_data: UserRegisterSchemma, db: Session = Depends(get_db)):
    user = User(name=form_data.name, email=form_data.email, password=form_data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


class UserLoginSchemma(BaseModel):
    email: EmailStr
    password: str


@app.post("/login")
def login(form_data: UserLoginSchemma, db: Session = Depends(get_db)):
    exist = db.query(User).filter(User.email == str(form_data.email)).first()

    if exist is None:
        return {"message": "login fail: user not found"}

    if exist.password == form_data.password:
        return {"message": "ok", "user": exist}

    return {"message": "login fail invalid password"}
